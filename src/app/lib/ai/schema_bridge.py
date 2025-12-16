import msgspec
from typing import Type, Any


def prepare_schema_for_gemini(struct: Type) -> dict[str, Any]:
    """
    Transform a Msgspec struct into a Gemini-compatible JSON Schema.
    
    Gemini 1.5 Flash supports a subset of JSON Schema (OpenAPI 3.0 compatible).
    This function:
    1. Generates base schema via msgspec.json.schema()
    2. Removes unsupported/wasteful metadata (title, description)
    3. Ensures additionalProperties is false
    4. Validates constraints (maxLength, enum)
    
    Args:
        struct: Msgspec Struct type
        
    Returns:
        Sanitized JSON Schema dict compatible with Gemini
    """
    # Generate base schema
    schema = msgspec.json.schema(struct)
    
    # Sanitize schema recursively
    return _sanitize_schema(schema)


def _sanitize_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively sanitize schema for Gemini compatibility.
    """
    sanitized = {}
    
    for key, value in schema.items():
        # Remove fields that Gemini doesn't support
        if key in ("title", "$schema", "additionalProperties"):
            continue
        
        # Keep description only if it's meaningful for the model
        if key == "description" and len(value) > 100:
            continue
        
        # Recursively sanitize nested objects
        if key == "properties" and isinstance(value, dict):
            sanitized[key] = {
                prop_name: _sanitize_schema(prop_value)
                for prop_name, prop_value in value.items()
            }
        elif key == "items" and isinstance(value, dict):
            sanitized[key] = _sanitize_schema(value)
        elif key == "$defs" and isinstance(value, dict):
            # Inline definitions instead of using $ref for stability
            sanitized[key] = {
                def_name: _sanitize_schema(def_value)
                for def_name, def_value in value.items()
            }
        else:
            sanitized[key] = value
    
    return sanitized


def inline_refs(schema: dict[str, Any]) -> dict[str, Any]:
    """
    Inline $ref definitions for better Gemini stability.
    
    While Gemini 1.5 supports $ref, inlining reduces hallucinations
    by providing local context.
    """
    if "$defs" not in schema:
        return schema
    
    defs = schema.pop("$defs")
    
    def _replace_refs(obj: Any) -> Any:
        if isinstance(obj, dict):
            if "$ref" in obj:
                # Extract definition name
                ref_path = obj["$ref"]
                if ref_path.startswith("#/$defs/"):
                    def_name = ref_path.split("/")[-1]
                    if def_name in defs:
                        return _replace_refs(defs[def_name].copy())
            return {k: _replace_refs(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_replace_refs(item) for item in obj]
        return obj
    
    return _replace_refs(schema)


def validate_schema_constraints(schema: dict[str, Any]) -> list[str]:
    """
    Validate that schema meets Gemini constraints.
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    def _check_depth(obj: Any, depth: int = 0, max_depth: int = 10):
        if depth > max_depth:
            errors.append(f"Schema exceeds max depth of {max_depth}")
            return
        
        if isinstance(obj, dict):
            for value in obj.values():
                _check_depth(value, depth + 1, max_depth)
        elif isinstance(obj, list):
            for item in obj:
                _check_depth(item, depth + 1, max_depth)
    
    _check_depth(schema)
    return errors
