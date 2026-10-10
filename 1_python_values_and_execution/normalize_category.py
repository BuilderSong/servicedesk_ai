from normalize_text import normalize_text as nt

def normalize_category(text: str, limit: int = 40) -> str:
    """
    Normalize the input category text by converting it to lowercase, stripping leading/trailing whitespace,
    and truncating it to a specified character limit.

    Args:
        text (str): The input category text to normalize.
        limit (int): The maximum length of the normalized text. Default is 40 characters.

    Returns:
        str: The normalized and truncated category text.
    """
    normalized_text = nt(text)
    if len(normalized_text) > limit:
        raise ValueError(f"Normalized text exceeds the limit of {limit} characters.")
    return normalized_text


