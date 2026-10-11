def positive_id(num: int) -> int: # type: ignore
    if isinstance(num, int) and num != True and num > 0: # type: ignore
        return num
    raise ValueError("Input must be a positive integer") # type: ignore


