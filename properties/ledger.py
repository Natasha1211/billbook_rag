import re
import json
from rapidfuzz import process
import numpy as np
from pymongo import MongoClient
from properties.invoices import fetch_active_invoice

MONGO_URL = "mongodb+srv://chandini_hirola:dIMUXBAKunFqTgEF@cluster0.cgdy4cu.mongodb.net/billingDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
client.admin.command('ismaster')
db = client['billingDB']
ledger_collection=db['ledgermodels']
ledger_data = list(ledger_collection.find())
def get_ledger(id):
    # print(id)
    active_invoice_ledger=[]
    not_deleted_ledgers=[]
    updated_ledger=0
    credit=0
    debit=0
    
    for item in ledger_data:
        if isinstance(item, dict) and "customerid" in item:
            if str(item["customerid"])==str(id) and str(item["isDeleted"]).lower()==str("false").lower():
                not_deleted_ledgers.append(item)
    
    active_invoice=fetch_active_invoice()  
    # print(active_invoice)
    for item in not_deleted_ledgers:
        if isinstance(item, dict) and 'invoiceID' in item:
            if str(item['invoiceId']) in active_invoice:
                active_invoice_ledger.append(item)
                
    # print("active invoice ledger", active_invoice_ledger) 
    for item in active_invoice_ledger:
        if isinstance(item, dict):
            if 'credit' in item:
                credit=item['credit']
                updated_ledger=updated_ledger-credit
            else:
                debit=item['debit']
                updated_ledger=updated_ledger+debit
            # previous_ledger=previous_ledger+debit-credit
            # updated_ledger=previous_ledger+updated_ledger
            
    return active_invoice_ledger, updated_ledger
            
        
def fetches_ledgers_through_customerid(customer_id):
    print("in side the ledger", customer_id)
    with open("properties/data_base/ledgermodels.json", "r") as file:
        ledger_data = json.load(file)
        
    for item in ledger_data:
        if isinstance(item, dict) and "customerid" in item:
            value=item["customerid"]
            if value==customer_id:
                return(item)
            