import re
import json
import time
import ast
import math
from rapidfuzz import process
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient

MONGO_URL = "mongodb+srv://chandini_hirola:dIMUXBAKunFqTgEF@cluster0.cgdy4cu.mongodb.net/billingDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
client.admin.command('ismaster')
db = client['billingDB']
export_invoice_collection=db['exportinvoices']
sez_collection=db['sezinvoices']
invoice_collection=db['addinvoices']


def fetch_export_invoice(id):
    # print("fetching export invoice")
    export_invoice=[]
    export_invoice_id=[]
    export_invoice_data = list(export_invoice_collection.find())
    for item in export_invoice_data:
        if isinstance(item, dict) and "customerName" in item:
            if str(item['customerName'])==str(id):
                export_invoice.append([item])
                export_invoice_id.append(id)
    return export_invoice, export_invoice_id

def fetch_active_invoice():
    active_id=[]
    # print("fetching invoice status")
    invoice_data=list(invoice_collection.find())
    for item in invoice_data:
        if isinstance(item, dict) and "status" in item:
            if item['status']=="Active":
                active_id.append(item['invoiceId'])
    return active_id

def fetch_sez_invoice(id):
    print("fetching sez invoice")
    sez=[]
    sez_id=[]
    sez_data = list(sez_collection.find())
    for item in sez_data:
        if isinstance(item, dict) and "customerName" in item:
            if str(item['customerName'])==str(id):
                sez.append([item])
                sez_id.append(id)
    return sez, sez_id
    
def get_invoice(id):
    print("fetching invoice")
    invoice=[]
    invoice_id=[]
    invoice_data = list(invoice_collection.find())
    for item in invoice_data:
        if isinstance(item, dict) and "customerName" in item:
            if str(item['customerName'])==str(id):
                # print(item['customerName'], id)
                invoice.append(item)
                invoice_id.append(item['invoiceId'])
    return invoice, invoice_id


def fetches_invoices(query, auth_access):
    results=[]
    if auth_access and isinstance(auth_access, list) and len(auth_access) > 0:
        inner_list = auth_access[0]
        if inner_list and isinstance(inner_list, list) and len(inner_list) > 0:
            inner_dict = inner_list[0]
            if inner_dict["invoice-read"]==True:
                print("\nyou are accessed in invoice\n")
                print("fetching invoices")

                with open("properties/data_base/addinvoices.json", 'r') as f:
                    data_base=json.load(f)

                date_pattern = r'(?i)\d{4}-\d{2}-\d{2}[tT]\d{2}:\d{2}:\d{2}\.\d{6}'
                id_pattern = r'\b(id|ID|Id)\b'
                pan_pattern= r'\b(pan|PAN|Pan)\b'
                tax_pattern= r'\b(tax|TAX|Tax|taxable|cgstTax|cgst tax|sgst tax|sgstTax|cgst|sgst)\b'

                # payment_type=[item for item in data_base]

                if re.search(r'\b(bal|Balance|Bal|balance|total|Total)\b', query):
                    print("in balance")
                    label="balance" #print total amount, taxable, balance
                    amt=re.search(r'\b\d+', query)[0]
                    # print(amt)
                    for item in data_base:
                        if isinstance(item, dict):
                            total=str(item["balance"]).strip()
                            if total==amt:
                                # for key, value in item.items():
                                #     print(f"{key}: {value}")
                                # print("\n")
                                results.append(item)

                if re.search(r'\b(Status|Stat|status)\b', query):
                    print("in invoice status")
                    label="invoiceStatus"
                    invoice_status=['PAID', 'UNPIAD']

                    status=process.extractOne(query.upper(), invoice_status, score_cutoff=50)
                    print(status)
                    for item in data_base:
                        if isinstance(item, dict):
                            invoice_status=str(item["invoiceStatus"]).strip()
                            if invoice_status==status[0]:
                                # for key, value in item.items():
                                #     print(f"{key}: {value}")
                                # print("\n")
                                results.append(item)

                if re.search(id_pattern, query):
                    if re.search(r'\b(cust|customer)\b', query):
                        print("its the customer id")
                        label="customerId"
                    elif re.search(r'\b(business|buis|buisness)\b', query):
                        print("its the business id")
                        label="businessId"
                    elif re.search(r'\b(invoice|invioces|invoices)\b', query):
                        print("its the invoice id")
                        label="invoiceId"
                    elif re.search(r'\b(bank|Bank|BANK)\b', query):
                        print("its the product id")
                        label="bankId"
                    else:
                        pass
                    
                    extracted_id = str(re.findall(id_pattern, query)[0].strip())
                    # print(id)
                    for item in data_base:
                        if isinstance(item, dict):
                            item_id = str(item[label]).strip()
                            # print(item_id, extracted_id)
                            if item_id == extracted_id:
                                # for key, val in item.items():
                                #     print(f"{key}:{val}")
                                # print("\n")
                                results.append(item)

                if re.search(date_pattern, query, re.IGNORECASE):
                    # print(query)
                    if re.search(r'\b(created|create)\b', query):
                        label="invoiceDate"
                    elif re.search(r'\b(due)\b', query):
                        label="dueDate"
                    else:
                        pass
                    # print(label)
                    date=re.findall(date_pattern, query)[0]
                    date = date.replace('t', 'T').rstrip('Z').strip()
                    for item in data_base:
                        if isinstance(item, dict):
                            created_date=item[label] 
                            if created_date==date:
                                # for key, value in item.items():
                                #     print(f"{key}: {value}")
                                # print("\n")
                                results.append(item)

                if re.search(r'\b(number|num|Number|NUMBER)\b', query):
                    # print("in number")
                    # print(query)
                    if re.search(pan_pattern, query):
                        if re.search(r'\b(cust|customer)\b', query):
                            # print("customer pan")
                            label="custPANNumber"
                        elif re.search(r'\b(business|buis|buisness)\b', query):
                            # print("business pan")
                            label="bussPANNumber"
                        else:
                            pass
                    elif re.search(r'\b(invoice|Invoice|Invo|INVOICE)\b', query):
                        # print("in invoice number")
                        label="invoiceNumber"
                    elif re.searc(r'\b(custom|Cust|Custom)\b', query):
                        # print("in custom number")
                        label="isCustomInvoiceNumber"
                    elif re.search(r'\b(LTU|ltu|Ltu)\b', query):
                        # print("in ltu number")
                        label="ltuNumber"
                    else:
                        pass
                    # print(label)
                    number=re.findall(r'\d+', query)[0]
                    for item in data_base:
                        if isinstance(item, dict):
                            invoice_number=item[label]
                            if invoice_number==number:
                                # for key, value in item.items():
                                #     print(f"{key}: {value}")
                                # print("\n")
                                results.append(item)

                if re.search(tax_pattern, query, re.IGNORECASE):
                    if re.search(r'\b(total)\b', query):
                        if re.search(r'\b(percentage|percent|%)\b', query):
                            pass
                        else:
                            label="totalTax"
                    elif re.search(r'\b(cgst|CGST|Cgst)\b', query):
                        # print("cgst tax")
                        label="cgstTaxAmount"
                    elif re.search(r'\b(sgst|SGST|Sgst)\b', query):
                        # print("sgst tax")
                        label="sgstTaxAmount"
                    elif re.search(r'\b(taxable)\b', query):
                        # print("tcs tax")
                        label="taxableAmount"
                    else:
                        pass

                    tax_list = re.findall(r'\b\d+\.\d+\b', query)
                    if tax_list:
                        tax = float(tax_list[0])
                        for item in data_base:
                            if isinstance(item, dict):
                                try:
                                    total_tax = float(item[label])
                                except (ValueError, TypeError):
                                    continue
                                if math.isclose(total_tax, tax, rel_tol=1e-5):
                                    # for key, value in item.items():
                                    #     print(f"{key}: {value}")
                                    # print("\n")
                                    results.append(item)

                if re.search(r'\b(percentage|percent|%)\b', query, re.IGNORECASE):
                    if re.search(r'\b(discount|Discoutn|discount)\b', query):
                        # print("total tax percentage")
                        label="totalDiscountPercentage"
                    
                    elif re.search(r'\b(cgst|CGST|Cgst)\b', query):
                        # print("cgst tax percentage")
                        label="cgstTaxPercentage"
                    
                    elif re.search(r'\b(sgst|SGST|Sgst)\b', query):
                        # print("sgst tax percentage")
                        label="sgstTaxPercentage"

                    elif re.search(r'\b(TAX|tax|Tax)\b', query):
                        # print("tcs tax")
                        label="totalTaxPercentage"

                    # elif re.search(r'\b(tcs|TCS|Tcs)\b', query):
                    #     # print("tcs tax")
                    #     label="tcspercentage"
                    else:
                        pass

                    percentage_match = re.findall(r'\b\d+', query)
                    if percentage_match:
                        percentage = percentage_match[0].strip()
                        for item in data_base:
                            if isinstance(item, dict):
                                invoice_number = item[label]
                                if isinstance(invoice_number, (int, float)):
                                    if str(invoice_number) == str(percentage):
                                        # for key, value in item.items():
                                        #     print(f"{key}: {value}")
                                        # print("\n")
                                        results.append(item)

                if re.search(r'\b(tcs|TCS|Tcs)\b', query):
                    if re.search(r'\b(amount|AMT|amt|Amt)\b', query):
                        # print("tcs amount")
                        label="tcsAmountvalue"
                    elif re.search(r'\b(percentage|percent|%)\b', query):
                        # print("tcs percentage")
                        label="tcspercentage"
                    else:
                        pass
                    # print(label)
                    # num=re.findall(r'\d+', query)
                    # if num:
                    #     num = num[0].strip()
                    #     for item in data_base:
                    #         if isinstance(item, dict):
                    #             number = item[label]
                                # if isinstance(num, (int, float)):
                                #     if str(num) == str(number):
                                #         for key, value in item.items():
                                #             print(f"{key}: {value}")
                                #         print("\n")
                                #     elif str(num) == "NULL":
                                #         for key, value in item.items():
                                #             print(f"{key}: {value}")
                                #         print("\n")
                                #     else:
                                #         pass

                if re.search(r'\b(apply|applied|aply)\b', query):
                    if re.search(r'\b(tcs|TCS|Tcs)\b', query):
                        print("inside the apply TCS")
                        for item in data_base:
                            if isinstance(item, dict):
                                applied = item["applyTCS"]
                                if applied is True:
                                    # for key, value in item.items():
                                    #     print(f"{key}: {value}")
                                    # print("\n")
                                    results.append(item)
                                    
                    elif re.search(r'\b(tds|TDS|Tds)\b', query):
                        print("inside the apply tds")
                        for item in data_base:
                            if isinstance(item, dict):
                                applied = item["applyTDS"]
                                if applied is True:
                                    # for key, value in item.items():
                                    #     print(f"{key}: {value}")
                                    # print("\n")
                                    results.append(item)
                    else:
                        pass
                elif re.search(r'\b(not\s*apply|not\s*applied|not\s*aply)\b', query):
                    if re.search(r'\b(tcs|TCS|Tcs)\b', query):
                        print("inside the not apply TCS")
                        for item in data_base:
                            if isinstance(item, dict):
                                # Get value safely and check if False
                                applied = item.get("applyTCS", False)
                                if applied is False:  # Fetch where applyTCS is False
                                    # for key, value in item.items():
                                    #     print(f"{key}: {value}")
                                    # print("\n")
                                    results.append(item)
                    elif re.search(r'\b(tds|TDS|Tds)\b', query):
                        print("inside the not apply TDS")
                        for item in data_base:
                            if isinstance(item, dict):
                                # Get value safely and check if False
                                applied = item.get("applyTDS", False)
                                if applied is False:  # Fetch where applyTDS is False
                                    # for key, value in item.items():
                                    #     print(f"{key}: {value}")
                                    # print("\n")
                                    results.append(item)
                    else:
                        pass
                
                else:
                    pass
                
                
                return(results)
