import re
import json
from rapidfuzz import process
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def fetches_orders(id):
    with open("properties/data_base/purchasesorders.json", 'r') as f:
        purchase_orders=json.load(f)
        
    for item in purchase_orders:
        if isinstance(item, dict) and "businessId" in item:
            if isinstance(item["businessId"], dict) and "$oid" in item["businessId"] and item["businessId"]["$oid"] == id:
                # print(item)
                return item
            