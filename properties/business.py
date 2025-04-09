import re
import json
import numpy as np
import faiss
from rapidfuzz import process
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time


with open("properties/data_base/businessschemas.json", 'r') as f:
    business_schema=json.load(f)
    
with open("properties/data_base/businessrelateddetails.json", 'r') as f:    
    business_details=json.load(f)
    
for item in business_details:
    if isinstance(item, dict) and "businessId"in item:
        business_id=item["businessId"]

def fetching_buisness_details(query):
    # isAdmin=False
    
    def ID(query):
        id=re.findall(r'\b[a-fA-F0-9]{24}\b', query, re.IGNORECASE)[0]
        return id
        
    def check_admin(user_id, buisness_id):
        if user_id == buisness_id:
            # isAdmin=True
            return True
        else:
            # isAdmin=False
            return False
    
    def get_user_personal_details(query):
        #user id , user name, user email, user phone, industry type, registration type, gst number
        #Pan number, has admin, adminId
        pass
    
    def business_details(query):
        #business name, business type, business count, user count, ltu buisness
        pass
    
    def subscription_details(query):
        # has subscribed, has active plan, status , plan selection
        pass
    
    def invoice_details(query):
        #invoice count, total revenue , posbilling, sezinvoice, exporttaxinvoice, bill of supply 
        pass
    
    def check_tds_tcds(query):
        #TDS, TCS
        pass
    
    def history_details(query):
        #plan history
        pass
    
    def create_update_section(query):
        #createdAt, updatedAt
        pass
    
    def role_acess_details(query):
        #role access
        # if isAdmin:
        #     print("admin access")
        # else:
        #     print("you don't have admin access")
        pass
    
    def ticket_generated_details(query):
        #tickets
        pass
    
    print("inside buisness details, query", query)
    mapping={
        # "userPersonalDetails":[name for item in business_schema if isinstance(item, dict) for key, name in item.items() if key=="name"],
        "businessDetails":["business"],
        "subscriptionDetails":["subscription", "subscribe", "plan", "plans"],
        "invoiceDetails":["invoice", "invoices"],
        "checkTdsTcds":["tds", "tcds"],
        "historyDetails":["history", "plan", "past"],
        "createUpdateSection":["date", "created", "updated"],
        "roleAcessDetails":["role", "access"],
        "ticketGeneratedDetails":["ticket", "tickets"],
    }
    
    best_match, best_score, best_key = None, 0, None
    for name, synonyms in mapping.items():
        match = process.extractOne(query, synonyms)  # Fuzzy match
        if match and match[1] > best_score:
            best_match, best_score, best_key = match[0], match[1], name
    if best_key:
        best_key=best_key
    
    print(best_key)
    user_id=ID(query)
    # if check_admin(user_id, business_id):
    #     print("the user is super admin")
    # else:
    #     print("the user is not super admin")

    
    names=[name for item in business_schema if isinstance(item, dict) for key, name in item.items() if key=="name"]
    best_match=process.extractOne(query, names)
    
    if best_match:
        best_match=best_match[0]
        for item in business_schema:
            if isinstance(item, dict) and "name" in item:
                name=item["name"]
                if name==best_match:
                    print(f"giving the details of {name}")
                    for key, value in item.items():
                        print(f"{key}:{value}")
                    print("\n")
                    
    
    # if best_key=="userPersonalDetails":
        
    #     get_user_personal_details(query)
    
    # elif best_key=="businessDetails":
    #     business_details(query)
    
    # elif best_key=="subscriptionDetails":
    #     subscription_details(query)
    
    # elif best_key=="invoiceDetails":
    #     invoice_details(query)
    
    # elif best_key=="checkTdsTcds":
    #     check_tds_tcds(query)
    
    # elif best_key=="historyDetails":
    #     history_details(query)
    
    # elif best_key=="createUpdateSection":
    #     create_update_section(query)
    
    # elif best_key=="roleAcessDetails":
    #     role_acess_details(query)
    
    # elif best_key=="ticketGeneratedDetails":
    #     ticket_generated_details(query)
    
    # else:
    #     pass
    
   
    
    
    
    
    
    
    



