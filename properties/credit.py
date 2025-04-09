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
creditnotes_collection=db['creditnotes']


def fetches_credit(id):
    print("fetching credit")
    
    credit_data = list(creditnotes_collection.find())
    credits=[]
    credits_id=[]
        
    for item in credit_data:
        if isinstance(item, dict) and 'customerName' in item:
            if item['customerName']==id:
                credits.append(item)
                credits_id.append(id)
    return credits, credits_id