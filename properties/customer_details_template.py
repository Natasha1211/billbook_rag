from properties.payments import  fetches_transactions, fetches_payment
from properties.ledger import fetches_ledgers_through_customerid, get_ledger
from properties.invoices import fetches_invoices, get_invoice, fetch_sez_invoice, fetch_export_invoice
from properties.credit import fetches_credit
from properties.supply import fetches_bill_of_supply, delivery_challan, fetches_sales_return
from properties.orders import fetches_orders
from properties.cust_report import fecth_item_wise_report
from properties.quotation import fetches_quotation, fetches_performa


# customer details
def fetching_all_details_of_customer(customer_id, item):
    results=[]
    results.append({"Customer details of": item['name'], "data": item})
    
    invoice, invoice_id=get_invoice(customer_id)
    if invoice_id==[]:
        results.append([f"{item['name']} has no invoice"])
    else:
        results.append({"Total Number of Invoice are":len(invoice_id),"label": "invoice", "data": invoice})
    
    
    payments, payment_id=fetches_payment(customer_id)
    if payment_id==[]:
        results.append([f"{item['name']} has no payment"])
    else:
        results.append({"Total Number of Payments are":len(payment_id),"label": "payments", "data": payments})
        
        
    proforma, proforma_id=fetches_performa(customer_id)
    if proforma_id==[]:
        results.append([f"{item['name']} has no proforma"])
    else:
        results.append({"The Number of Proforma":len(proforma_id),"label": "performa", "data": proforma})
    
    
    quotation, quotation_id=fetches_quotation(customer_id)
    if quotation_id==[]:
        results.append([f"{item['name']} has no quotation"])
    else:
        results.append({"The Number of Quotaions ":len(quotation_id), "label": "quotation", "data": quotation})
    
    
    delivery_challans, delivery_challan_id=delivery_challan(customer_id)
    if delivery_challan_id==[]:
        results.append([f"{item['name']} has no delivery challan"])
    else:
        results.append({"The Number of Delivery Challans":len(delivery_challan_id),"label": "delivery challan", "data": delivery_challans})
    
    
    supply, supply_id=fetches_bill_of_supply(customer_id)
    if supply_id==[]:
        results.append([f"{item['name']} has no supply"])
    else:   
        results.append({"The Number of bill of supply":len(supply_id), "label": "supply", "data": supply})
    
    
    sez_invoice, sez_id=fetch_sez_invoice(customer_id)
    if sez_id==[]:
        results.append([f"{item['name']} has no sez invoice"])
    else:
        results.append({"The Number of sez invoice":len(sez_id), "label": "sez invoice", "data": sez_invoice})
    
    
    export_invoice, export_invoice_id=fetch_export_invoice(customer_id)
    if export_invoice_id==[]:
        results.append([f"{item['name']} has no export invoice"])
    else:
        results.append({"The Number of export invoice":len(export_invoice_id), "label": "export invoice", "data": export_invoice})
    
    
    credit, credit_id=fetches_credit(customer_id)
    if credit_id==[]:
        results.append([f"{item['name']} has no credit"])
    else:
        results.append({"The Number of Credit":len(credit_id), "label": "credit", "data": credit})
    
    
    sales_return, sales_return_id=fetches_sales_return(customer_id)
    if sales_return_id==[]:
        results.append([f"{item['name']} has no sales return"])
    else:
        results.append({"The Number of sales return":len(sales_return_id),"label": "sales return", "data": sales_return})
    
    
    transactions, transactions_id= fetches_transactions(customer_id)
    if transactions_id==[]:
        results.append([f"{item['name']} has no transactions"])
    else:
        results.append({"The Number of sales return":len(transactions_id),"label": "transactions", "data": transactions})


    active_ledger, total_ledger=get_ledger(customer_id)
    if total_ledger==0:
        results.append([f"{item['name']} has no ledger"])
    else:   
        results.append({"Total ledger":total_ledger,"label": "ledger", "data": active_ledger})
    
    cust_report, cust_report_num=fecth_item_wise_report(customer_id)
    if cust_report_num==0:
        results.append([f"{item['name']} has no item wise report"])
    else:
        results.append({"Total customer report":cust_report_num,"label": "product details", "data": cust_report})
    
    return results