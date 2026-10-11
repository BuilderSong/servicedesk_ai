from normalize_text import normalize_text as nt


fixed_categories = {"appliances","blinds","cabinets","cleaning","concrete","deck_vinyl","drywall","insulation","texture","painting_interior","painting_exterior","eavestroughing",
                    "electrical","fireplace","flooring_lvp","flooring_tile","flooring_carpet","foundation","framing","garage_doors","hvac","landscaping","lighting","masonry","plumbing","roofing","siding",
                    "windows","interior_doors","interior_trim",}

def count_categories(categories:list[str]) -> dict[str,int]:
    count_dict = {}
    for category in categories: 
        normalized_category = nt(category)
        if normalized_category in fixed_categories:
            count_dict[normalized_category] = count_dict.get(normalized_category, 0) + 1 # type: ignore
    return count_dict # type: ignore

