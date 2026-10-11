def positive_id(num: int) -> int: # type: ignore
    if isinstance(num, int) and num > 0 and num != True: # type: ignore
        return num
    raise ValueError("Input must be a positive integer") # type: ignore


