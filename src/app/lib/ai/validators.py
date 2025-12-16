import unicodedata
from typing import Annotated


def calculate_display_width(text: str) -> int:
    """
    Calculate display width of text, accounting for CJK double-width characters.
    
    Google Ads counts characters based on display width:
    - ASCII characters: 1 unit
    - CJK characters (Chinese, Japanese, Korean): 2 units
    
    Args:
        text: Input string
        
    Returns:
        Display width in character units
    """
    width = 0
    for char in text:
        # Check if character is East Asian Wide or Fullwidth
        if unicodedata.east_asian_width(char) in ('F', 'W'):
            width += 2
        else:
            width += 1
    return width


def validate_headline(headline: str) -> list[str]:
    """
    Validate a single headline against Google Ads constraints.
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    if not headline:
        errors.append("Headline cannot be empty")
        return errors
    
    width = calculate_display_width(headline)
    if width > 30:
        errors.append(f"Headline exceeds 30 characters (actual: {width})")
    
    return errors


def validate_description(description: str) -> list[str]:
    """
    Validate a single description against Google Ads constraints.
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    if not description:
        errors.append("Description cannot be empty")
        return errors
    
    width = calculate_display_width(description)
    if width > 90:
        errors.append(f"Description exceeds 90 characters (actual: {width})")
    
    return errors


def validate_rsa_assets(assets: dict) -> list[str]:
    """
    Validate complete RSA asset structure.
    
    Args:
        assets: Dict with 'headlines' and 'descriptions' keys
        
    Returns:
        List of all validation errors
    """
    errors = []
    
    headlines = assets.get("headlines", [])
    descriptions = assets.get("descriptions", [])
    
    # Count validation
    if len(headlines) < 3:
        errors.append(f"Minimum 3 headlines required (got {len(headlines)})")
    if len(headlines) > 15:
        errors.append(f"Maximum 15 headlines allowed (got {len(headlines)})")
    
    if len(descriptions) < 2:
        errors.append(f"Minimum 2 descriptions required (got {len(descriptions)})")
    if len(descriptions) > 4:
        errors.append(f"Maximum 4 descriptions allowed (got {len(descriptions)})")
    
    # Individual validation
    for i, headline in enumerate(headlines):
        headline_errors = validate_headline(headline)
        for error in headline_errors:
            errors.append(f"Headline {i+1}: {error}")
    
    for i, description in enumerate(descriptions):
        desc_errors = validate_description(description)
        for error in desc_errors:
            errors.append(f"Description {i+1}: {error}")
    
    # Path validation (optional fields)
    if "path1" in assets and assets["path1"]:
        if len(assets["path1"]) > 15:
            errors.append(f"Path1 exceeds 15 characters")
    
    if "path2" in assets and assets["path2"]:
        if len(assets["path2"]) > 15:
            errors.append(f"Path2 exceeds 15 characters")
    
    return errors


def truncate_to_limit(text: str, max_width: int) -> str:
    """
    Truncate text to fit within display width limit.
    
    Args:
        text: Input text
        max_width: Maximum display width
        
    Returns:
        Truncated text
    """
    current_width = 0
    result = []
    
    for char in text:
        char_width = 2 if unicodedata.east_asian_width(char) in ('F', 'W') else 1
        if current_width + char_width > max_width:
            break
        result.append(char)
        current_width += char_width
    
    return ''.join(result)
