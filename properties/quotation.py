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
quotations_collection=db['addquotations']
proformas_collection=db['addproformas']

def fetches_quotation(id):
    print("fetching qoutation")
    quotations_data = list(quotations_collection.find())
    quotations=[]
    quotations_id=[]
    for item in quotations_data:
        if isinstance(item, dict) and "customerName" in item:
            value=item["customerName"]
            if value==id:
                quotations.append(item)
                quotations_id.append(id)
    return quotations, quotations_id

def fetches_performa(id):
    print("fetching proforma")
    proformas_data = list(proformas_collection.find())
    proforma=[]
    proforma_id=[]
    for item in proformas_data:
        if isinstance(item, dict) and "customerName" in item:
            value=item["customerName"]
            if value==id:
                proforma.append(item)
                proforma_id.append(id)
                
    return proforma, proforma_id
