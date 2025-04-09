import json
import re

def check_auth(bussinessId, current_buisness_id):
    access=[]
    
    with open('properties/data_base/businessschemas.json', 'r') as file:
        business_schema=json.load(file)
        
    if bussinessId==current_buisness_id:
        user="admin"
    else:
        user="user"
        
    if user=="admin":
        pass
    else:
        for item in business_schema:
            if isinstance(item, dict) and "_id" in item:
                value=item["_id"]
                if value==current_buisness_id:
                    role=item["role"]
                    # print(role)
        
        for item in business_schema:
            if isinstance(item, dict) and "roleAccess" in item:
                roleacess=item["roleAccess"]
                if role in roleacess:
                    for key in roleacess[role]:
                        data_list=roleacess[role][key]
                        access.append(data_list)
        
    return(access)


    
    
    
    
    
    
    