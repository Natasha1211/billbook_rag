import re
import json
from rapidfuzz import process


def fetches_categories(query, auth_access):
    results=[]
    if auth_access and isinstance(auth_access, list) and len(auth_access) > 0:
        inner_list = auth_access[0]
        if inner_list and isinstance(inner_list, list) and len(inner_list) > 0:
            inner_dict = inner_list[0]
            if inner_dict["category-create"] and inner_dict["category-read"] and inner_dict["category-update"] and inner_dict["category-delete"]:
                print("\nyou are accessed in categoriesr\n")
                print("fetching categories")
                with open('properties/data_base/addcategories.json') as f:
                    data_base = json.load(f)
                
                if re.search(r'\b[a-fA-F0-9]{24}\b', query):
                    buz_id=re.findall(r'\b[a-fA-F0-9]{24}\b', query)[0]
                    # print(id)
                    for item in data_base:
                        if isinstance(item, dict):
                            if item['businessId']==buz_id:
                                # for key, value in item.items():
                                #     print(f"{key}: {value}")
                                # print("\n")
                                results.append(item)
                                
                else:
                    category_list = [category['categoryName'] for category in data_base]
                    best_match = process.extractOne(query, category_list, score_cutoff=50)
                    if best_match:
                        match=best_match[0]
                        for item in data_base:
                            if item['categoryName'] == match:
                                # for key, value in item.items():
                                #     print(f"{key}: {value}")
                                # print("\n")
                                results.append(item)
                    else:
                        for item in data_base:
                            if isinstance(item, dict):
                                # for key, value in item.items():
                                #     print(f"{key}: {value}")
                                # print("\n")
                                results.append(item)
                            else:
                                # print(item)
                                # print("\n")
                                results.append(item)
                return results