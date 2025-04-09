import re
import json
import time
import math
from rapidfuzz import process
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

"""
all the information about the packages and its plans


add auth for super admin

"""
def fetches_package_plan(query, business_id):
    results=[]
        
    with open("properties/data_base/profileforbusinesses.json", 'r') as f:
            data_base=json.load(f)
            
    feature_name=[]
    users=[]
    module_name=[]
    display_name=[]
    mapping = {
            "moduleName": ["mod", "module", "modle"],
            "displayName": ["display", "display name"],
            "name": ["naem", "name"],
    }

    for item in data_base:
        if isinstance(item, dict):
            for key, value in item.items():
                if key=="features":
                    if isinstance(value, list):
                        feature_name.append(
                            [plans["name"] for plans in value if isinstance(plans, dict) and "name" in plans]
                        ) 
                        module_name.append(
                            [plans["moduleName"] for plans in value if isinstance(plans, dict) and "moduleName" in plans]
                        )
                        display_name.append(
                            [plans["displayName"] for plans in value if isinstance(plans, dict) and "displayName" in plans]
                        )                      
                                        
    for item in data_base:
        if isinstance(item, dict):
            for key, value in item.items():
                if key=="modules":
                    if isinstance(value, list):
                        users.append(
                            [plans["name"] for plans in value if isinstance(plans, dict) and "name" in plans]
                        )
                        
    # print(users)


    def fetching_package_plans(query):
        print("fetching package plans\n")
        # print(query)
        if re.search(r'\b(feature|festures)\b', query):
            if re.search(r'\b\d+', query):
                num=re.findall(r'\b\d+', query)[0]
                if num:
                    # print(num)
                    for item in data_base:
                        if isinstance(item, dict) and "features" in item:
                            val = item["features"] 
                            if isinstance(val, list):
                                for items in val:
                                    if items.get("value") == str(num):
                                        for k, v in items.items():
                                            print(f"{k}: {v}")
                                        print("\n") 
                                        
            elif not re.search(r'\b\d+', query):
                best_match, best_score, best_key = None, 0, None
                for name, synonyms in mapping.items():
                    match = process.extractOne(query, synonyms)  # Fuzzy match
                    if match and match[1] > best_score:
                        best_match, best_score, best_key = match[0], match[1], name
                        
                if best_key:
                    key=best_key
                    # print(key)
                    if best_key=="moduleName":
                        match = process.extractOne(query,module_name[0], score_cutoff=70)
                        if match:
                            key_name = match[0]
                        key=="moduleName"
                    elif best_key=="displayName":
                        match = process.extractOne(query,module_name[0], score_cutoff=70)
                        if match:
                            key_name = match[0]
                        key=="displayName"
                    elif best_key=="name":
                        match = process.extractOne(query,module_name[0], score_cutoff=70)
                        if match:
                            key_name = match[0]
                        key=="name"
                    else:
                        key_name==None
                        
                    if key_name:
                        # print(key, key_name)
                        for item in data_base:
                            if isinstance(item, dict) and "features" in item:
                                val=item["features"]
                                if isinstance(val, list):
                                    for items in val:
                                        if items.get(key)==key_name:
                                            for k, v in items.items():
                                                print(f"{k}:{v}")
                                            print("\n")                
            else:
                for item in data_base:
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if key=="features":
                                if isinstance(value, list):
                                    for plans in value:
                                        if isinstance(plans, dict):
                                            for key, value in plans.items():
                                                print(f"{key}: {value}")
                                            print("\n")
                                            
        elif re.search(r'\b(module|module name)\b', query):
            # print(query)
            if re.search(r'name', query):
                match = process.extractOne(query, users[0], score_cutoff=70)
                if match:
                    key_name = match[0]
                # print(key_name)
                for item in data_base:
                    if isinstance(item, dict) and "modules" in item:
                        value=item["modules"]
                        if isinstance(value, list):
                            for items in value:
                                if items.get("name")==key_name:
                                    for k, v in items.items():
                                        print(f"{k}:{v}")
                                    print("\n")
            elif re.search(r'display name', query):
                match = process.extractOne(query, users[0], score_cutoff=70)
                if match:
                    key_name = match[0]
                print(key_name)
                
                for item in data_base:
                    if isinstance(item, dict) and "modules" in item:
                        value=item["modules"]
                        if isinstance(value, list):
                            for items in value:
                                if items.get("displayName")==key_name:
                                    for k, v in items.items():
                                        print(f"{k}:{v}")
                                    print("\n")   
            else:
                for item in data_base:
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if key=="modules":
                                if isinstance(value, list):
                                    for plans in value:
                                        if isinstance(plans, dict):
                                            for key, value in plans.items():
                                                print(f"{key}: {value}")
                                            print("\n")
        else:
            pass

    def fetching_types_of_plans(query):
        print("fetching types of plans")
        with open("data_base/addplantypes.json", 'r') as f:
            data_base=json.load(f)
        print("\nthis is our trail period, if you want to know about subscription period please search for subscription period\n")
        for item in data_base:
            if isinstance(item, dict):
                for key, value in item.items():
                    print(f"{key}: {value}")
                print("\n")
                
    if re.search(r'\b(traial period|types plans|types\s*plans|plan types)\b', query):
            fetching_types_of_plans(query)
    elif re.search(r'\b(subscription period|subscription|subscription\s*period|subscription model|subscriptions|package plans|package\s*plans)\b', query):
        fetching_package_plans(query)
    else:
        pass
                
            
        