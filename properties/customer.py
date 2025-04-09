import re
import json
from rapidfuzz import process
import numpy as np
import faiss
from datetime import datetime
from sentence_transformers import SentenceTransformer
from properties.customer_details_template import fetching_all_details_of_customer


"""
extracting :- invoice, credit, sales return, payment, performa, quotation, delivery challan, 
bill of supply, SEZ invoice, export invoice, relevant transaction, ledger, item wise

"""

def fetches_customers(query, auth_access, customer_collection, customers_names):
    results = []
    # print(auth_access)
    name_flag=False
    email_flag=False
    phone_flag=False
    cred_flag=False
    balance_flag=False
    gst_flag=False
    pan_flag=False
    date_flag=False
    
    if auth_access and isinstance(auth_access, list) and len(auth_access) > 0:
        inner_list = auth_access[0]

        if inner_list and isinstance(inner_list, list) and len(inner_list) > 0:
            authorized = False 
            for item in inner_list:
                if isinstance(item, dict) and item.get("customers-read") == True:
                    authorized = True
                    print("\nYou are authorized to access customer details.\n")
                    with open('properties/data_base/addcustomers.json', 'r') as f:
                        data_base = json.load(f)
                        
                    id_pattern = r'\b[a-fA-F0-9]{24}\b'
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    phone_pattern = r'(\+91|91)[\|\-]?(\d+)'
                    credit_pattern = r'\b(credits|credit|Credit|Cred|cred)\b'
                    balance_pattern = r'\b(balance|opening|Balance|Opening)\b'
                    gst_pattern = r"\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}Z[A-Z\d]{1}"
                    pan_pattern = r"[A-Z]{5}\d{4}[A-Z]"
                    date_pattern = r'\d{4}-\d{2}-\d{2}[tT]\d{2}:\d{2}:\d{2}\.\d+(?:Z|[+-]\d{2}:\d{2})?'
                    cust_documents = list(customer_collection.find())
                    
                    print(query)
                    
                    if re.search(email_pattern, query):
                        email_flag=True
                        extracted_email = str(re.findall(email_pattern, query)[0].strip())
                        
                    if re.search(phone_pattern, query):
                        phone_flag=True
                        extracted_phone="".join(re.findall(phone_pattern, query)[0])
                        
                    if re.search(credit_pattern, query):
                        cred_flag=True
                        cred_num = re.findall(r'\d+', query)
                        
                    if re.search(balance_pattern, query):
                        balance_flag=True
                        balance_num=re.findall(r'\d+', query)
                        
                    if re.search(gst_pattern, query, re.IGNORECASE):
                        gst_flag=True
                        gst_num=re.findall(gst_pattern, query.upper())[0]
                        
                    if re.search(pan_pattern, query, re.IGNORECASE):
                        pan_flag=True
                        pan_num=re.findall(pan_pattern, query.upper())[0]
                    
                    if re.search(date_pattern, query, re.IGNORECASE):
                        date_flag=True
                        date = re.findall(date_pattern, query)[0].replace('t', 'T').rstrip('Z').strip()
                        
                    
                    
                    if name_flag:
                        best_match = process.extractOne(query, customers_names, score_cutoff=90)
                        print(best_match)
                        
                    if email_flag:
                        for item in cust_documents:
                            if isinstance(item, dict) and str(item["email"]).strip() == extracted_email:
                                customer_id=item["_id"]
                                results=fetching_all_details_of_customer(customer_id=customer_id, item=item)
                                
                    if phone_flag:
                        for item in cust_documents:
                            if isinstance(item, dict) and str(item["phoneNumber"]).strip() == extracted_phone:
                                customer_id=item["_id"]
                                results=fetching_all_details_of_customer(customer_id=customer_id, item=item)
                              

                    # if cred_flag:
                    #     if cred_num:
                    #         for item in cust_documents:
                    #             if isinstance(item, dict) and str(item["customerCredit"]).strip() == num[0]:
                    #                 customer_id=item.get("customerId")
                    #                 payments=fetches_transactions_through_customerid(customer_id)
                    #                 results.append(item, payments)
                                    
                    if balance_flag:
                        for item in cust_documents:
                            if isinstance(item, dict) and str(item["openingBalance"]).strip() == balance_num[0]:
                                customer_id=item["_id"]
                                results=fetching_all_details_of_customer(customer_id=customer_id, item=item)
                                

                    if gst_flag:
                        for item in cust_documents:
                            if isinstance(item, dict) and str(item["GSTNo"]) == str(gst_num):
                                customer_id=item["_id"]
                                results=fetching_all_details_of_customer(customer_id=customer_id, item=item)

                    if pan_flag:
                        print("inside pan number")
                        for item in cust_documents:
                            if isinstance(item, dict) and str(item["PANNumber"]).strip() == pan_num:
                                customer_id=item["_id"]
                                # print(customer_id)
                                results=fetching_all_details_of_customer(customer_id=customer_id, item=item)

                    if date_flag:
                        print("inside date")
                        for item in cust_documents:
                            if isinstance(item, dict) and 'createdAt' in item:
                                created_at = str(item['createdAt'])
                                if isinstance(created_at, str):
                                    date_obj = datetime.fromisoformat(date.split('Z')[0])
                                    item_date = datetime.fromisoformat(created_at.split('Z')[0])
                                    print(item_date, date_obj)
                                        
                                            
            
                    if not results:
                        # model= SentenceTransformer("all-MiniLM-L6-v2")
                        # faiss_index = faiss.read_index('embeddings/activities.faiss')
                        # chunks = np.load('embeddings/activities.npy', allow_pickle=True)
                        # query_embedding=model.encode([query])
                        # k=len(chunks)
                        # D,I = faiss_index.search(query_embedding, k=min(len(chunks), 2))
                        # relevant_bios=[chunks[i] for i in I[0]]
                        # filtered_bios=[bio for bio in relevant_bios]
                        # for bio in filtered_bios:
                        #     # print(bio)
                        #     results.append(bio)
                        #     print("\n")
                        pass

                    break 
            if not authorized:
                results.append("You are not authorized to access customer details.")
        else:
            results.append("Invalid authorization format.")
    else:
        results.append("No valid authorization provided.")

    return results
