import os
from typing import Type, Any
from google import genai
from google.genai.types import GenerateContentConfig, SafetySetting, HarmCategory, HarmBlockThreshold
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import msgspec
from app.domain.campaigns.models import RSAAsset
from app.lib.ai.schema_bridge import prepare_schema_for_gemini
from app.lib.ai.validators import validate_rsa_assets, calculate_display_width


class GeminiService:
    """
    Service for Google Gemini 1.5 Flash integration.
    Handles structured content generation with retry logic.
    """
    
    def __init__(self, api_key: str | None = None):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Gemini API key. If None, uses GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.client = genai.Client(api_key=self.api_key)
        # Use explicit stable version
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-001")
        
        # Safety settings for ad content (allow marketing language)
        self.safety_settings = [
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH
            )
        ]
    
    async def generate_structured(
        self,
        prompt: str,
        response_schema: dict[str, Any],
        system_instruction: str | None = None
    ) -> dict[str, Any]:
        """
        Generate structured content using Gemini with schema validation.
        
        Args:
            prompt: User prompt
            response_schema: JSON Schema for structured output
            system_instruction: Optional system instruction
            
        Returns:
            Parsed JSON response matching schema
        """
        config = GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
            safety_settings=self.safety_settings,
            temperature=0.7
        )
        
        # Use synchronous client (google-genai doesn't have stable async yet)
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config
        )
        
        # Parse JSON response
        return msgspec.json.decode(response.text)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ValueError, msgspec.DecodeError))
    )
    async def generate_with_retry(
        self,
        prompt: str,
        response_schema: dict[str, Any],
        system_instruction: str | None = None
    ) -> dict[str, Any]:
        """
        Generate structured content with automatic retry on failure.
        """
        return await self.generate_structured(prompt, response_schema, system_instruction)
    
    async def generate_rsa_assets(
        self,
        landing_page_url: str,
        target_keywords: list[str],
        brand_voice: str | None = None,
        language: str = "de"
    ) -> dict[str, Any]:
        """
        Generate Responsive Search Ad assets using Gemini 1.5 Flash.
        
        Uses Chain-of-Thought prompting to ensure diverse, high-quality assets
        that meet Google Ads constraints.
        
        Args:
            landing_page_url: URL of the landing page
            target_keywords: List of target keywords
            brand_voice: Optional brand voice (e.g., "professional", "playful")
            language: ISO 639-1 language code
            
        Returns:
            Dict with 'headlines' and 'descriptions' lists
        """
        from app.lib.ai.schema_bridge import prepare_schema_for_gemini
        from app.domain.campaigns.models import RSAAsset
        from app.lib.ai.validators import validate_rsa_assets
        
        # Build Chain-of-Thought prompt
        prompt = self._build_rsa_prompt(
            landing_page_url,
            target_keywords,
            brand_voice,
            language
        )
        
        # Generate schema for RSAAsset
        schema = prepare_schema_for_gemini(RSAAsset)
        
        print(f"DEBUG: Requesting generation with model {self.model}...")
        # Generate with retry
        response = await self.generate_with_retry(prompt, schema)
        print("DEBUG: Received response from Gemini API")
        
        # DEBUG: Write raw response to file UNCONDITIONALLY
        try:
            with open("debug_gemini_response.log", "w", encoding="utf-8") as f:
                import json
                f.write(json.dumps(response, indent=2, ensure_ascii=False))
            print("DEBUG: Wrote response to debug_gemini_response.log")
        except Exception as e:
            print(f"Failed to write debug log: {e}")

        # Validate response
        errors = validate_rsa_assets(response)

        if errors:
            print(f"Validation WARNING: {errors}")
            
            # DEBUG: Write raw response to file
            try:
                with open("debug_gemini_response.log", "w", encoding="utf-8") as f:
                    import json
                    f.write(json.dumps(response, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Failed to write debug log: {e}")

            # Auto-correct length issues by truncation
            # Auto-correct length issues by truncation
            # We iterate through the raw dict before converting to struct if needed, 
            # but here response is a dict from msgspec
            
            # Helper to strict truncate
            def enforce_limit(text: str, limit: int) -> str:
                if calculate_display_width(text) <= limit:
                    return text
                # Truncate char by char until it fits
                while calculate_display_width(text) > limit:
                    text = text[:-1]
                return text.strip()

            if "headlines" in response:
                response["headlines"] = [
                    enforce_limit(h, 30) for h in response["headlines"]
                ]
            
            if "descriptions" in response:
                response["descriptions"] = [
                    enforce_limit(d, 90) for d in response["descriptions"]
                ]
            
            # Re-validate after fixing
            remaining_errors = validate_rsa_assets(response)
            if remaining_errors:
                print(f"CRITICAL Validation errors: {remaining_errors}")
                # Only raise if still invalid (e.g. empty list)
                # But even then, try to return what we have
                if not response.get("headlines") or not response.get("descriptions"):
                     raise ValueError(f"Generation failed: {remaining_errors}")

        return response
    
    def _build_rsa_prompt(
        self,
        landing_page_url: str,
        target_keywords: list[str],
        brand_voice: str | None,
        language: str
    ) -> str:
        """
        Build Chain-of-Thought prompt for RSA generation.
        """
        keywords_str = ", ".join(target_keywords)
        voice_instruction = f"Brand voice: {brand_voice}. " if brand_voice else ""
        
        return f"""You are an expert Google Ads copywriter specializing in Responsive Search Ads (RSA).

**Task:** Generate high-performing RSA assets for the following landing page.

**Landing Page:** {landing_page_url}
**Target Keywords:** {keywords_str}
{voice_instruction}**Language:** {language}

**Requirements:**
1. **Headlines:** Generate exactly 15 unique headlines
   - Each headline MUST be maximum 30 characters (count characters, not words!)
   - Create diversity:
     * 5 headlines that incorporate the target keywords naturally
     * 5 headlines that focus on benefits and value propositions
     * 5 headlines with strong calls-to-action (CTA)

2. **Descriptions:** Generate exactly 4 unique descriptions
   - Each description MUST be maximum 90 characters
   - Create variety:
     * 2 descriptions explaining key benefits
     * 2 descriptions with compelling CTAs

**CRITICAL CONSTRAINTS:**
- Count CHARACTERS, not words. "Außergewöhnlich" = 15 characters.
- For CJK characters (Chinese/Japanese/Korean), each character counts as 2 units.
- Do NOT exceed character limits under any circumstances.
- Ensure all text is in {language}.

**Chain-of-Thought Process:**
1. First, analyze the landing page URL and identify 3-5 unique selling points (USPs)
2. Then, create keyword-focused headlines that naturally incorporate the target keywords
3. Next, create benefit-focused headlines highlighting the USPs
4. Finally, create action-oriented headlines and descriptions

Generate the assets now, ensuring strict adherence to character limits."""
    
    async def health_check(self) -> dict[str, str]:
        """
        Check Gemini API connectivity.
        
        Returns:
            Status dict with model and connection info
        """
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents="Respond with 'OK'"
            )
            return {
                "status": "healthy",
                "model": self.model,
                "response": response.text
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }

