def normalize_text(text:str) -> str:
    """
    Normalize the input text by converting it to lowercase and stripping leading/trailing whitespace.

    Args:
        text (str): The input text to normalize.

    Returns:
        str: The normalized text.
    """
    if not isinstance(text, str): # type: ignore
        raise ValueError("Input must be a string.")
    if text.isspace() or text == "":
        raise ValueError("Input string cannot be empty.")
    return text.strip().lower()
