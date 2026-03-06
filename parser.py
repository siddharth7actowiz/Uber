import json
from pydantic import ValidationError
from validation import Restaurant


def prser(data: dict):
    res = {}
    base_path = data.get("data") or {}

    res["Restaurant_Name"] = base_path.get("title")

    if not res["Restaurant_Name"]:
        return None
    res["Res_Id"]=base_path.get("uuid")

    res["Phone_No"] = base_path.get("phoneNumber")

    location = base_path.get("location") or {}

    res["Full_Address"] = location.get("address")
    res["Street_address"] = location.get("streetAddress")
    res["City"] = location.get("city")
    res["Country"] = location.get("country")
    res["Region"] = location.get("region")
    res["Pincode"] = str(location.get("postalCode"))

    sections = base_path.get("sections") or []

    res["Timing"] = None
    if sections and isinstance(sections[0], dict):
        res["Timing"] = sections[0].get("subtitle")

    res["ETA"] = (base_path.get("etaRange") or {}).get("text")

    icons = base_path.get("indicatorIcons") or []

    res["Map"] = None
    if icons and isinstance(icons[0], dict):
        res["Map"] = icons[0].get("moreInfoSheet", {}).get("url")

    dining_modes = []

    for d in base_path.get("supportedDiningModes") or []:

        dining_modes.append({
            "Mode": d.get("mode"),
            "isAvailable": d.get("isAvailable")
        })

    res["Dining_Modes"] = json.dumps(dining_modes)

    cuisines = base_path.get("cuisineList") or []

    res["Cuisions"] = json.dumps(cuisines)

    catalog_sections = base_path.get("catalogSectionsMap") or {}

    cat_list = []
    for v in catalog_sections.values():
        if isinstance(v, list):
            cat_list.extend(v)

    category_data = []

    for items_dict in cat_list:
        payload = items_dict.get("payload") or {}
        std_payload = payload.get("standardItemsPayload") or {}

        cat_name = (std_payload.get("title") or {}).get("text")
        cat_id = items_dict.get("catalogSectionUUID")

        cat_data = {"cat_id": cat_id, "cat_name": cat_name}
        menu_items = []

        for item in std_payload.get("catalogItems") or []:
            price_info = item.get("priceTagline") or {}
            menu_items.append({
                "item_name": item.get("title"),
                "item_id": item.get("uuid"),
                "url": item.get("imageUrl"),
                "price": price_info.get("text"),
                "description": item.get("itemDescription"),
                "is_sold_out": item.get("isSoldOut")
            })

        cat_data["Menu"] = menu_items
        category_data.append(cat_data)

    res["Category"] = json.dumps(category_data)

    featured_sections = base_path.get("featuredItemsSections") or {}

    featured_cat_list = []
    for v in featured_sections.values():
        if isinstance(v, list):
            featured_cat_list.extend(v)

    featured_category_data = []

    for items_dict in featured_cat_list:
        payload = items_dict.get("payload") or {}
        std_payload = payload.get("standardItemsPayload") or {}

        cat_name = (std_payload.get("title") or {}).get("text")
        cat_id = items_dict.get("catalogSectionUUID")

        cat_data = {"cat_id": cat_id, "cat_name": cat_name}
        menu_items = []

        for item in std_payload.get("catalogItems") or []:
            price_info = item.get("priceTagline") or {}
            menu_items.append({
                "item_name": item.get("title"),
                "item_id": item.get("uuid"),
                "url": item.get("imageUrl"),
                "price": price_info.get("text"),
                "description": item.get("itemDescription"),
                "is_sold_out": item.get("isSoldOut")
            })

        cat_data["Menu"] = menu_items
        featured_category_data.append(cat_data)

    res["Featured_Category"] = json.dumps(featured_category_data)
    res["Currency"] = base_path.get("currencyCode")

    try:
        Restaurant(**res)
        return res
    except ValidationError as v:
        print("Error:",v)
