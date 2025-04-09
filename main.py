from rapidfuzz import process
import spacy
from chat_functions import *
from auth import check_auth
from pymongo import MongoClient
import json


nlp = spacy.load("en_core_web_sm")

MONGO_URL = "mongodb+srv://chandini_hirola:dIMUXBAKunFqTgEF@cluster0.cgdy4cu.mongodb.net/newBillingMain?retryWrites=true&w=majority"


def find_prompt_route(query,auth_access):
    customers=[]
    client = MongoClient(MONGO_URL)
    client.admin.command('ismaster')
    db = client['newBillingMain']
    customer_collection = db['addcustomers']
    # activity_collection = db['activities']
    # invoice_collection = db['invoices']
    # category_collection = db['categories']
    # packageplan_collection = db['packageplans']
    # product_collection = db['products']
    # business_collection = db['business']
    
    customer_documents = customer_collection.find()
    for doc in customer_documents:
        if isinstance(doc, dict) and "name" in doc:
            customers.append(doc["name"])
    # print(customers)
    bill_book_mapping={
        "activity":["activities"],
        "customer":[customers, "balance", "credit", "phone", "mobile", "gst" ,"gst number", "pan", "pan number", "created"],
        "invoice":["invoices"],
        "category": ["categories", "category", "cat", "properties", "property", "categorys"],
        "packageplan":["packageplans", "packages", "plans","subscription","subscribe"],
        "products":["products", "Products", "Pro"],
        "report":["reports", "report", "Report", "Reports"],
    }

    best_match, best_score, best_key = None, 0, None
    for nutrient, synonyms in bill_book_mapping.items():
        match = process.extractOne(query, synonyms)  # Fuzzy match
        if match and match[1] > best_score:
            best_match, best_score, best_key = match[0], match[1], nutrient
    if best_key:
        best_key=best_key
        
    if best_key=="customer":
        ans=fetch_customers(query, auth_access, customer_collection, customers)
        print("in main")
        return(ans)
    
    # elif best_key=="activity":
    #     ans=fetch_activities(query, auth_access, activity_collection)
    #     print("in main")
    #     with open("response.json", "w") as f:
    #         json.dump(ans, f)
    #     return(ans)

    # elif best_key=="invoice":
    #     fetch_invoices(query, auth_access)

    # elif best_key=="category":
    #     ans=fetch_categories(query, auth_access)
    #     print(ans)

    # elif best_key=="packageplan":
    #     fetch_package_plans(query, auth_access)
        
    # elif best_key=="products":
    #     ans=fetching_add_products(query, auth_access)
    #     # print(ans)
    #     return ans

    # elif best_key=="business":
    #     ans=fetching_from_buisness_details(query, auth_access)
    #     # print(ans)

    else:
        print("Nothing found")
        
    # print(best_key)
def remove_stop_words(query):
    doc = nlp(query)
    grammar_words = [token.text.lower() for token in doc if token.is_stop and token.text.lower() not in ["due","name"]]
    return grammar_words
    
def query_tokenizetion(query):
    query = query.lower().strip().replace('"', '')
    grammer_words=remove_stop_words(query=query)
    # print(grammer_words)
    query=[words for words in query.split() if words not in grammer_words]
    query=" ".join(query)
    return(query)

# """
# chat bot main

# """
def chat_main(query_structure):
    # return("i got it")
    # demo query: give me the details of the products which has serial number 123
    for item in query_structure:
        query=item["question"]
        business_id=item["businessId"]
        current_business_id=item["curent_business"]
    query=query_tokenizetion(query)
    auth_access=check_auth(business_id, current_business_id)
    ans=find_prompt_route(query, auth_access=auth_access)
    return ans

        
    




