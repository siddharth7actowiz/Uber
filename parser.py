import json
import pprint

from unicodedata import category


def prser(data:dict):
    res={}
    base_path=data.get("data",{})
    res["Restaurant_Name"]=base_path.get("title")
    res["Phone_No"] = base_path.get("phoneNumber")
    res["Full_Address"]=base_path.get("location",{}).get("address")
    res["Street_address"] = base_path.get("location").get("streetAddress")
    res["City"] = base_path.get("location").get("city")
    res["Country"] = base_path.get("location").get("country")
    res["Region"] = base_path.get("location").get("region")
    res["Pincode"] = base_path.get("location").get("postalCode")
    res["ETA"] = base_path.get("etaRange",{}).get("text")
    res["Map"] = base_path.get("indicatorIcons",[])[0].get("moreInfoSheet",{}).get("url")
    del_path=base_path.get("supportedDiningModes",[])
    dining=[]
    for d in del_path:
        dining.append(
            {
                "Mode":d.get("mode"),
                "isAvailable":d.get("isAvailable")
            }
        )
    res["Dining_Modes"]=json.dumps(dining)


    cuisions_list = base_path.get("cuisineList", [])
    res["Cuisions"] = json.dumps([cusion for cusion in cuisions_list])
    

    #paths for menu and category data
    catalog_sections = base_path.get("catalogSectionsMap", {})

    cat_list = catalog_sections.get("0ad5db85-c10f-5ad6-897c-f8ef6bd5cc78", [])
    #tihs will include categorey data

    category_data=[]

    for items_dict in cat_list:
            menu_items = []

            payload = items_dict.get("payload", {})
            std_payload = payload.get("standardItemsPayload", {})

            # Category info
            cat_name = std_payload.get("title", {}).get("text")
            cat_id = items_dict.get("catalogSectionUUID")

            cat_data = {
                "cat_id": cat_id,
                "cat_name": cat_name
            }

            items = std_payload.get("catalogItems", [])

            for item in items:
                menu_items.append({
                    "item_name": item.get("title"),
                    "item_id": item.get("uuid"),
                    "url": item.get("imageUrl"),
                    "price": item.get("priceTagline", {}).get("text"),
                    "description": item.get("itemDescription"),
                    "is_sold_out": item.get("isSoldOut")
                })

            cat_data["Menu"] = menu_items
            category_data.append(cat_data)
    res["Category"]=json.dumps(category_data) #because sql can parse by itself 

   #featured_items

    featured_cat_list = base_path.get("featuredItemsSections",{}).get('0ad5db85-c10f-5ad6-897c-f8ef6bd5cc78',{})
    featured_category_data = []

    for items_dict in cat_list:
        menu_items = []

        payload = items_dict.get("payload", {})
        std_payload = payload.get("standardItemsPayload", {})

        # Category info
        cat_name = std_payload.get("title", {}).get("text")
        cat_id = items_dict.get("catalogSectionUUID")

        cat_data = {
            "cat_id": cat_id,
            "cat_name": cat_name
        }

        items = std_payload.get("catalogItems", [])

        for item in items:
            menu_items.append({
                "item_name": item.get("title"),
                "item_id": item.get("uuid"),
                "url": item.get("imageUrl"),
                "price": item.get("priceTagline", {}).get("text"),
                "description": item.get("itemDescription"),
                "is_sold_out": item.get("isSoldOut")
            })

        cat_data["Menu"] = menu_items
        featured_category_data.append(cat_data)
    res["Featured_Category"] =json.dumps(featured_category_data)
    res["Currency"]=base_path.get("currencyCode")
    return res