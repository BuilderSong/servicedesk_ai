

def id_index(records_list: list[dict[int, str]]) -> dict[int, str]:
    id_index_dict = {}
    # if records_list is None: # type: ignore
    #     raise TypeError("Input cannot be None")
    if records_list == []:
        return id_index_dict # type: ignore
    
    for record in records_list:
        for record_id, record_vale in record.items():
            if record_id in id_index_dict:
                raise ValueError(f"Duplicate ID found: {record_id}") # type: ignore
            id_index_dict[record_id] = record_vale
    return id_index_dict # type: ignore
    

