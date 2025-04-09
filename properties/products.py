import re
import json
import time
import ast
import math
from rapidfuzz import process
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


"""
fetching all the product related information

"""
def fetches_products(query, auth_access):
    results=[]
    if auth_access and isinstance(auth_access, list) and len(auth_access) > 0:
        inner_list = auth_access[0]
        if inner_list and isinstance(inner_list, list) and len(inner_list) > 0:
            inner_dict = inner_list[0]
            if inner_dict["products-create"]==True and inner_dict["products-read"]==True and inner_dict["products-update"]==True and inner_dict["products-delete"]==True:
                print("\nyou are accessed in products\n")
                print("fetching products")
                
                with open(r'properties/data_base/addproducts.json', 'r') as file:
                    data_base=json.load(file)

                def fetching_through_id(query):
                    # product and business id
                    if re.search(r'\bEasyBBProductID\d{13}\b', query, re.IGNORECASE):
                        print("inside customer id")
                        
                        prod_id = re.findall(r'\bEasyBBProductID\d{13}\b', query, re.IGNORECASE)
                        
                        if prod_id:
                            prod_id=prod_id[0].strip()
                        # print(prod_id) 
                        
                        for item in data_base:
                            if isinstance(item, dict):
                                if item.get("productId").lower()==prod_id:
                                    for key, val in item.items():
                                        print(f"{key}:{val}")
                                    print("\n")
                    
                    elif re.search(r'[0-9a-f]{24}', query, re.IGNORECASE):
                        if not re.search(r'\b(gst)\b', query):
                            print("inside the buisiness id")
                            buisiness_id = re.findall(r'[0-9a-f]{24}', query, re.IGNORECASE)
                            if buisiness_id:
                                buisiness_id=buisiness_id[0].strip()
                            # print(buisiness_id)
                            
                            for item in data_base:
                                if isinstance(item, dict):
                                    if item.get("businessId").lower()==buisiness_id:
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")
                    else:
                        print("no such id")
                                        
                def fetching_through_tax(query):
                    # taxtype, taxpurchasetype, gsttaxtype, gst tax rate
                    matched_tax=None
                    if re.search(r'\b(type)\b', query):
                        print("inside tax type")
                        tax_type=[values for item in data_base if isinstance(item, dict) for key, values in item.items() if key=="taxType"]

                        best_matched_tax= process.extractOne(query, tax_type, score_cutoff=50)
                        if best_matched_tax:
                            matched_tax, _, _=best_matched_tax
                        
                        for item in data_base:
                            if isinstance(item, dict) and "taxType" in item:
                                val=item["taxType"]
                                if val==matched_tax:
                                    for key, value in item.items():
                                        print(f"{key}:{value}")
                                    print("\n")
                    elif re.search(r'\b(purchase)\b', query):
                        print("inside purchase tax")
                        purchase_tax_type=[values for item in data_base if isinstance(item, dict) for key, values in item.items() if key=="taxpurchaseType"]
                        best_matched_tax= process.extractOne(query, purchase_tax_type, score_cutoff=50)
                        if best_matched_tax:
                            matched_tax, _, _=best_matched_tax
                        # print(matched_tax)
                        for item in data_base:
                            if isinstance(item, dict) and "taxpurchaseType" in item:
                                val=item["taxpurchaseType"]
                                if val==matched_tax:
                                    for key, value in item.items():
                                        print(f"{key}:{value}")
                                    print("\n")
                                    
                    elif re.search(r'\b(gst)\b', query):
                        print("inside gst tax")
                        if re.search(r'[0-9a-f]{24}', query, re.IGNORECASE):
                            gst=re.findall(r'[0-9a-f]{24}', query, re.IGNORECASE)
                            gst=gst[0]
                            print(gst)
                        for item in data_base:
                            if isinstance(item, dict) and "gstTaxRate" in item:
                                val=item["gstTaxRate"]
                                if val==str(gst):
                                    for key, value in item.items():
                                        print(f"{key}:{val}")
                                    print("\n")
                        
                    else:
                        pass

                def fetching_through_godown(query):
                    # godown
                    if re.search(r'\b(godown)\b', query):
                        print("inside godown")
                        godown=[str(values) for item in data_base if isinstance(item, dict) for key, values in item.items() if key=="Godown"]
                        godown_list = ast.literal_eval(godown[0])
                        best_matched_godown= process.extractOne(query, godown_list, score_cutoff=50)
                        
                        if best_matched_godown:
                            matched_godown, _, _=best_matched_godown
                            for item in data_base:
                                if isinstance(item, dict) and "godown" in item:
                                    val=item["Godown"]
                                    if isinstance(val, list):
                                        for num in val:
                                            if num==matched_godown:
                                                for key, value in item.items():
                                                    print(f"{key}:{value}")
                                                print("\n")
                
                def fetching_through_item(query):    
                    print("inside item")
                    if re.search(r'\b(category)\b', query):
                        num=re.findall(r'[0-9a-f]{24}', query, re.IGNORECASE)
                        if num:
                            num=num[0]
                            for item in data_base:
                                if isinstance(item, dict) and "itemCategory" in item:
                                    val=item["itemCategory"]
                                    if val==str(num):
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")
                    
                    elif re.search(r'\b(code)\b', query):
                        num=re.findall(r'[0-9]{5}', query)
                        if num:
                            num=num[0]
                            for item in data_base:
                                if isinstance(item, dict) and "itemCode" in item:
                                    val=item["itemCode"]
                                    if val==str(num):
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")
                    elif re.search(r'\b(HSN|hsn)\b'):
                        print("searching hsn code")
                    else:
                        item_list=[values for item in data_base if isinstance(item, dict) for key, values in item.items() if key=="itemName"]
                        best_matched_item=process.extractOne(query, item_list, score_cutoff=50)
                        if best_matched_item:
                            match, _, _ =best_matched_item
                        # print(match)
                        for item in data_base:
                            if isinstance(item, dict) and "itemName" in item:
                                val=item["itemName"]
                                if val == match:
                                    for k, v in item.items():
                                        print(f"{k}:{v}")
                                    print("\n")

                def fetching_through_price(query):
                    # sales price, purchase price, whole sale price, retail price, mrp
                    if re.search(r'\b(sales|sale|selling|sell)\b', query, re.IGNORECASE):
                        # print("sales")
                        price=re.findall(r'\d+', query)
                        if price:
                            price=price[0]
                            for item in data_base:
                                if isinstance(item, dict) and "salesPrice" in item:
                                    val=item[ "salesPrice"]
                                    if val==str(price):
                                        for k, v in item.items():
                                            print(f"{k}:{v}")
                                        print("\n")
                                        
                        else:
                            print("no item")
                    if re.search(r'\b(cost|pruchase|mrp)\b',query, re.IGNORECASE):
                        price=re.findall(r'\d+', query)
                        if price:
                            price=price[0]
                            for item in data_base:
                                print("-"*50)
                                print("purchase")
                                if isinstance(item, dict) and "purchasePrice" in item:
                                    val=item["purchasePrice"]
                                    if val==str(price):
                                        print("-"*50)
                                        print("purchase price:", {price})
                                        for k, v in item.items():
                                            print(f"{k}:{v}")
                                        print("\n")
                                        
                                elif isinstance(item, dict) and "MRP" in item:
                                    val=item["MRP"]
                                    if val==str(price):
                                        print("-"*50)
                                        print("MRP:", {price})
                                        for k, v in item.items():
                                            print(f"{k}:{v}")
                                        print("\n")
                                else:
                                    pass
                        else:
                            print("no item")
                    if re.search(r'\b(wholesale|whole sale)\b', query, re.IGNORECASE):
                        price=re.findall(r'\d+', query)
                        if price:
                            price=price[0]
                            for item in data_base:
                                if isinstance(item, dict) and "wholeSalePrice"in item:
                                    val=item["wholeSalePrice"]
                                    if val==str(price):
                                        for k, v in item.items():
                                            print(f"{k}:{v}")
                                        print("\n")
                        else:
                            print("no item")
                    if re.search(r'\b(retail)\b', query, re.IGNORECASE):
                        price=re.findall(r'\d+', query)
                        if price:
                            price=price[0]
                            for item in data_base:
                                if isinstance(item, dict) and "retailPrice" in item:
                                    val=item["retailPrice"]
                                    if val==str(price):
                                        for k, v in item.items():
                                            print(f"{k}:{v}")
                                        print("\n")
                        else:
                            print("no item")
                                    
                def fetching_thorugh_stock(query):
                    # opening stock, fixed opening stock, low stock quantity, stock value,
                    if re.search(r'\b(opening|open)\b', query, re.IGNORECASE):
                        print("inside opening stock")
                        num=re.findall(r'\d+', query)
                        # print(num)
                        if num:
                            num=num[0]
                            for item in data_base:
                                if isinstance(item, dict) and "openingStock" in item:
                                    val=item["openingStock"]
                                    if str(val)==str(num):
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")
                                                
                    if re.search(r'\b(fix|fixed|fixed opening)\b', query, re.IGNORECASE):
                        print("inside fixed opening")
                        num=re.findall(r'\d+', query)
                        # print(num)
                        if num:
                            num=num[0]
                            for item in data_base:
                                if isinstance(item, dict) and "fixedOpeningStock" in item:
                                    val=item["fixedOpeningStock"]
                                    if str(val)==str(num):
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")
                        
                    if re.search(r'\b(low)\b', query, re.IGNORECASE):
                        print("inside the low stock")
                        num=re.findall(r'\d+', query)
                        # print(num)
                        if num:
                            num=num[0]
                            for item in data_base:
                                if isinstance(item, dict) and "lowStockQuantity" in item:
                                    val=item["lowStockQuantity"]
                                    if str(val)==str(num):
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")
                        
                    if re.search(r'\b(val|value)\b', query, re.IGNORECASE):
                        print("inside the stock value")
                        num=re.findall(r'\d+', query)
                        # print(num)
                        if num:
                            num=num[0]
                            for item in data_base:
                                if isinstance(item, dict) and "stockValue" in item:
                                    val=item["stockValue"]
                                    if str(val)==str(num):
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")
                        
                def fetching_through_product_details(query):
                    # product description, sales product, purchase product, product image
                    
                    if re.search(r'\b(sales|sale)\b', query, re.IGNORECASE):
                        print("in prodcut sales")
                        num=re.findall(r'\d+', query)
                        if num:
                            num=num[0]
                            for item in data_base:
                                if isinstance(item,dict) and "salesProduct" in item:
                                    value=item["salesProduct"]
                                    if str(value)==str(num):
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")
                    if re.search(r'\b(purchase|cost)\b', query, re.IGNORECASE):
                        print("in purchase product")
                        num=re.findall(r'\d+', query)
                        if num:
                            num=num[0]
                            for item in data_base:
                                if isinstance(item,dict) and "purchaseProduct" in item:
                                    value=item["purchaseProduct"]
                                    if str(value)==str(num):
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")        
                    """
                    ask and add
                    """     
                    # if re.search(r'\b(image|pic|picture|pictures|images|pics)\b'):
                    #     print("in pictures")
                    product_description=[value for item in data_base if isinstance(item, dict) for key, value in item.items() if key=="productDescription"]
                    best_match=process.extractOne(query,product_description,score_cutoff=50)
                    match=None
                    if best_match:
                        match, _, _=best_match
                        for item in data_base:
                            if isinstance(item, dict) and "productDescription" in item:
                                value=item["productDescription"]
                                if str(value)==str(match):
                                    for key, val in item.items():
                                        print(f"{key}:{val}")
                                    print("\n")
                                    
                def fetching_through_service(query):
                    #service name, service code
                    if re.search(r'\b(code)\b', query):
                        num=re.findall(r'\d+', query)
                        if num:
                            num=num[0]
                            # print(num)
                            for item in data_base:
                                if isinstance(item,dict) and "serviceCode" in item:
                                    value=item["serviceCode"]
                                    if str(value)==str(num):
                                        for key, val in item.items():
                                            print(f"{key}:{val}")
                                        print("\n")
                    product_description=[value for item in data_base if isinstance(item, dict) for key, value in item.items() if key=="serviceName"]
                    best_match=process.extractOne(query,product_description,score_cutoff=50)
                    match=None
                    if best_match:
                        match, _, _=best_match
                        for item in data_base:
                            if isinstance(item, dict) and "serviceName" in item:
                                value=item["serviceName"]
                                if str(value)==str(match):
                                    for key, val in item.items():
                                        print(f"{key}:{val}")
                                    print("\n")

                def fetching_through_variant():
                    #primary prod variant, is prod variant, variants
                    
                    pass
                    
                def fetching_through_online_store(query):
                    #serialization, searial number, online store
                    print("inside store")
                    if re.search(r"\b(serialization)\b", query, re.IGNORECASE) and not re.search(r"\b(no|doesnt|not|does not)\b", query, re.IGNORECASE):
                        for item in data_base:
                            if isinstance(item, dict) and "serialization" in item:
                                value=item["serialization"]
                                if value == True or value == "true":
                                    for key, val in item.items():
                                        print(f"{key}:{val}")
                                    print("\n")
                    elif re.search(r'\b(no|doesnt|not|does not)\b', query, re.IGNORECASE):
                        for item in data_base:
                            if isinstance(item, dict) and "serialization" in item:
                                value=item["serialization"]
                                if value == False or value == "false":
                                    for key, val in item.items():
                                        print(f"{key}:{val}")
                                    print("\n")
                    elif re.search(r'\b(serial number|num|number)\b', query, re.IGNORECASE):
                        num=re.findall(r'\d+', query)
                        if num:
                            results=[]
                            num=num[0]
                            for item in data_base:
                                if isinstance(item, dict) and "serialNumbers" in item:
                                    value=item["serialNumbers"]
                                    if isinstance(value, list):
                                        for nums in value:
                                            if nums==num:
                                                results.append(item)
                                                for key, val in item.items():
                                                    print(f"{key}:{val}")
                                                print("\n")
                                            else:
                                                print("no such product")
                                                
                                                
                            if results:
                                return results
                            else:
                                return "no such product"
                                            #     for key, val in item.items():
                                            #         print(f"{key}:{val}")
                                            #     print("\n")
                                            # else:
                                            #     print("no such product")
                        
                    else:
                        pass

                def fetching_products(query):
                    print("inside products.py")
                    
                    
                    mapping = {
                        "id": ["id"],
                        "tax": ["tax type", "purchase tax", "tax purchase type", "tax"],
                        "godown": ["godown"],
                        "item": ["item category", "item name", "item code", "item",  "category", "code", "CODE",  "Code", "name", "Name"],
                        "price": ["sales price", "purchase price", "wholesale price", "retail price", "price"],
                        "stock": ["opening stock", "low stock quantity", "stock value", "stock"],
                        "product": ["product description", "product image", "sales product", "purchase product"],
                        "service": ["service name", "service code", "service"],
                        "variant": ["primary prod variant", "is prod variant", "variants"],
                        "store": ["online store", "serialization", "serial number"],
                        
                    }
                    
                    
                    best_match, best_score, best_key = None, 0, None
                    for name, synonyms in mapping.items():
                        match = process.extractOne(query, synonyms)  # Fuzzy match
                        if match and match[1] > best_score:
                            best_match, best_score, best_key = match[0], match[1], name
                            
                    if best_key:
                        print(best_key)
                        
                    if best_key=="id":
                        fetching_through_id(query)
                        
                    if best_key=="tax":
                        fetching_through_tax(query)
                        
                    if best_key=="godown":
                        fetching_through_godown(query)
                        
                    if best_key=="item":
                        fetching_through_item(query)
                        
                    if best_key=="price":
                        fetching_through_price(query)
                        
                    if best_key=="stock":
                        fetching_thorugh_stock(query)
                        
                    if best_key=="product":
                        fetching_through_product_details(query)
                        
                    if best_key=="service":
                        fetching_through_service(query)
                        
                    # if best_key=="variant":
                    #     fetching_through_variant()
                        
                    if best_key=="store":
                        ans=fetching_through_online_store(query)
                        # print("ans4", ans)
                        return ans
                    
                    
                    
                            
                    