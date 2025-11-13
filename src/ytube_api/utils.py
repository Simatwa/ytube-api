import re

compiled_illegal_characters_pattern = re.compile(r"[^\w\-_\.,\s()&|\[\]]")

def sanitize_filename(filename: str) -> str:
    """Remove illegal characters from a filename"""
    return re.sub(compiled_illegal_characters_pattern, "", filename)
