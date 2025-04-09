import re
import json
from rapidfuzz import process
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from properties.invoices import fetch_active_invoice


MONGO_URL = "mongodb+srv://chandini_hirola:dIMUXBAKunFqTgEF@cluster0.cgdy4cu.mongodb.net/billingDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client['billingDB']
payment_collection = db['paymentdetails']
transaction_collection = db['transactionmodels']

def fetches_payment(id):
    print("fetching payment")
    payment_data = list(payment_collection.find())
    payments=[]
    payment_id=[]
    for item in payment_data:
        if isinstance(item, dict) and "customername" in item:
            value=item['customername']
            if value==id:
                payments.append(item)
                payment_id.append(id)
    return payments, payment_id
                            
        
def fetches_transactions(id):
    # print("fetching transactions of: ", id)
    ids=[]
    invoice_id=[]
    transaction=[]
    active_transaction=[]
    filtered_transaction=[]
    
    transaction_data = list(transaction_collection.find())
    
    # print("in side the transactions", id)
    for item in transaction_data:
        if isinstance(item, dict) and 'customerid' in item:
            value=item['customerid']
            if str(value)==str(id):
                transaction.append(item)
    for item in transaction:
        if isinstance(item, dict) and 'invoiceId' in item:
            invoice_id.append(item['invoiceId'])
            
    active_invoice_id=fetch_active_invoice()
    # print(active_invoice_id)
    for item in invoice_id:
        if item in active_invoice_id:
            active_transaction.append(item)
            
    # print("active_transaction", active_transaction)
                
    for item in transaction:
        if isinstance(item, dict) and 'invoiceId' in item:
            if item['invoiceId'] in active_transaction:
                filtered_transaction.append(item)
                ids.append(item['invoiceId'])
                
    return filtered_transaction, ids
            
# def fetches_transactions_through_customerid(customer_id):
#     with open("properties/data_base/transactionmodels.json", "r") as file:
#         transaction_data = json.load(file)
#     for item in transaction_data:
#         if isinstance(item, dict) and "customerid" in item:
#             value=item["customerid"]
#             if value==customer_id:
#                 return(item)
            
        
        
        
    
    