import re
import json
from rapidfuzz import process
import numpy as np
import faiss
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from properties.invoices import fetch_active_invoice, get_invoice


MONGO_URL = "mongodb+srv://chandini_hirola:dIMUXBAKunFqTgEF@cluster0.cgdy4cu.mongodb.net/billingDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
client.admin.command('ismaster')
db = client['billingDB']
partywise_collection=db['partywisereports']
party_wise_data = partywise_collection.find()
product_report_collection=db['productreports']
product_report_data = partywise_collection.find()

def fecth_item_wise_report(id):
    party_details_customer_id=[]
    details_party_customer_id=[]
    product_details=[]
    active_product_id=[]
    active_invoice_id=[]
    invoice=[]
    
    print("fetching item wise report")
    for item in party_wise_data:
        if isinstance(item, dict) and 'customerId' in item:
            value=item['customerId']
            if str(value)==str(id):
                party_details_customer_id.append(id)
                details_party_customer_id.append(item)
    active_invoice_id=fetch_active_invoice()
    for id in party_details_customer_id:     
        invoice, invoice_id=get_invoice(id)
    # print(invoice,invoice_id)
   
    for item in invoice:
        if isinstance(item, dict) and 'invoiceId' in item:
            if item['invoiceId'] in active_invoice_id:
                for product in item['table']:
                    active_product_id.append(product['pid'])
                    
    # print(active_product_id)
    
    for item in product_report_data:
        if isinstance(item, dict) and 'products' in item:
            product_values=item['products']
            for product in product_values:
                if isinstance(product, dict) and 'productId' in product:
                    if product['productId'] in active_product_id:
                        # print(product)
                        product_details.append(product)
                        
    return product_details,len(product_details)

            
            
   
    