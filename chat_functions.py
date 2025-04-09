import re
import json
import math
from rapidfuzz import process
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from properties.products import  fetches_products
# from properties.packageplan import fetching_types_of_plans, fetching_package_plans
from properties.business import fetching_buisness_details
from properties.customer import fetches_customers
from properties.activities import fetches_activities
from properties.categories import fetches_categories
from properties.invoices import fetches_invoices
from properties.packageplan import fetches_package_plan


def fetch_activities(query, auth_access, activity_collection):
    ans= fetches_activities(query=query, auth_access=auth_access)
    print("in chat functions")
    return ans
# def fetch_categories(query, auth_acess):
#     return fetches_categories(query=query, auth_acess=auth_acess)

def fetch_customers(query, auth_access, customer_collection, customers_names):
    ans=fetches_customers(query=query, auth_access=auth_access, customer_collection=customer_collection, customers_names=customers_names)
    print("in chat functions")
    return ans

# def fetch_invoices(query, auth_access):
#     return(fetches_invoices(query=query, auth_access=auth_access))

# def fetch_package_plans(query, auth_access):
#     return(fetches_package_plan(query=query, auth_access=auth_access))
    
# def fetching_add_products(query):
#     return(fetches_products(query))
    
# def fetching_from_buisness_details(query):
#     return(fetching_buisness_details(query))

