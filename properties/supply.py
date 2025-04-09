import re
import json
from rapidfuzz import process
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient


MONGO_URL = "mongodb+srv://chandini_hirola:dIMUXBAKunFqTgEF@cluster0.cgdy4cu.mongodb.net/billingDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
client.admin.command('ismaster')
db = client['billingDB']
proformas_collection=db['deliverychallens']
sales_return_collection=db['salesreturns']
bill_of_supply_collection=db['billofsupplies']


def fetches_sales_return(id):
    print("fetching sales return")
    sales_return_data = list(sales_return_collection.find())
    sales_return=[]
    sales_return_id=[]
        
    for item in sales_return_data:
        if isinstance(item, dict) and 'customerName' in item:
            if item['customerName']==id:
                sales_return.append(item)
                sales_return_id.append(id)
    return sales_return, sales_return_id
                
def fetches_bill_of_supply(id):
    print("fetching bill of supply")
    bos_data = list(bill_of_supply_collection.find())
    bos_challans=[]
    bos_challans_id=[]
        
    for item in bos_data:
        if isinstance(item, dict) and 'customerName' in item:
            if item['customerName']==id:
                bos_challans.append(item)
                bos_challans_id.append(id)
    return bos_challans, bos_challans_id
            
def delivery_challan(id):
    print("fetching delivery challan")
    proformas_data = list(proformas_collection.find())
    delivery_challans=[]
    delivery_challans_id=[]
    
    for item in proformas_data:
        if isinstance(item, dict) and "customerName" in item:
            if item["customerName"]==id:
                delivery_challans.append(item)
                delivery_challans_id.append(id)
    return delivery_challans, delivery_challans_id