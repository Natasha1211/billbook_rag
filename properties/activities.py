
import re
import json
from rapidfuzz import process
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


def fetches_activities(query, auth_access):
    results=[]
    # print(auth_access)
    if auth_access and isinstance(auth_access, list) and len(auth_access) > 0:
        inner_list = auth_access[0]  
        if inner_list and isinstance(inner_list, list) and len(inner_list) > 0:
            for item in inner_list:
                if isinstance (item, dict):
                    if item.get("reports-read")==True:
                        print("you are accessed in activities")
                            
                        # print(query)
                        
                        with open('properties/data_base/activities.json', 'r') as f:
                            data_base = json.load(f)

                        recent_pattern = r'\b(recent|latest|new|newest|recently)\b'
                        old_pattern = r'\b(old|older|oldest)\b'
                        number_pattern = r'\d+'
                        date_pattern =  r'(?i)\d{4}-\d{2}-\d{2}[tT]\d{2}:\d{2}:\d{2}\.\d{6}'
                        create_pattern= r'\b(created|create|added)\b'
                        update_pattern= r'\b(updated|update)\b'
                        
                        if re.search(recent_pattern, query):
                            if re.search(number_pattern, query):
                                    num=int(re.findall(number_pattern, query)[0])
                                    data_base=data_base[-num:]
                                    for item in data_base:
                                        if isinstance(item, dict):
                                            # for key, value in item.items():
                                            #     print(f"{key}: {value}")
                                            # print("\n")
                                            results.append(item)
                                        else:
                                            # print(item)
                                            # print("\n")
                                            results.append(item)
                            else:
                                    if isinstance(data_base, list) and len(data_base)>0:
                                        last_item=data_base[-1]
                                        if isinstance(last_item, dict):
                                            # for key, value in last_item.items():
                                            #     print(f"{key}: {value}")
                                            # print("\n")
                                            results.append(last_item)
                                        else:
                                            # print(last_item)
                                            # print("\n")
                                            results.append(last_item)
                        
                        elif re.search(old_pattern, query):
                            if re.search(number_pattern, query):
                                num=int(re.findall(number_pattern, query)[0])
                                data_base=data_base[-num:]
                                for item in data_base:
                                    if isinstance(item, dict):
                                        # for key, value in item.items():
                                        #     print(f"{key}: {value}")
                                        # print("\n")
                                        results.append(item)
                                    else:
                                        # print(item)
                                        results.append(item)
                                        # print("\n")
                            else:
                                if isinstance(data_base, list) and len(data_base)>0:
                                    first_item=data_base[0]
                                    if isinstance(first_item, dict):
                                        # for key, value in first_item.items():
                                        #     print(f"{key}: {value}")
                                        # print("\n")
                                        results.append(first_item)
                                    else:
                                        # print(first_item)
                                        results.append(first_item)
                                        # print("\n")

                        elif re.search(date_pattern, query):
                            if re.search(create_pattern, query):
                                print("created date")
                                date=re.findall(date_pattern, query)[0]
                                date = date.replace('t', 'T').rstrip('Z').strip()
                                print(date)
                                for item in data_base:
                                    if isinstance(item, dict):
                                        created_date=item['createdAt']       
                                        if created_date==date:
                                            # for key, value in item.items():
                                            #     print(f"{key}: {value}")
                                            # print("\n")
                                            results.append(item)

                            elif re.search(update_pattern, query):
                                print("updated date")
                                date=re.findall(date_pattern, query)[0]
                                date = date.replace('t', 'T').rstrip('Z').strip()
                                print(date)
                                for item in data_base:
                                    if isinstance(item, dict):
                                        updated_date=item['updatedAt']
                                        if updated_date==date:
                                            # for key, value in item.items():
                                            #     print(f"{key}: {value}")
                                            # print("\n") 
                                            results.append(item)
                            else:
                                pass
                        else:
                            model= SentenceTransformer("all-MiniLM-L6-v2")
                            faiss_index = faiss.read_index('embeddings/activities.faiss')
                            chunks = np.load('embeddings/activities.npy', allow_pickle=True)
                            # pass
                            # to fetch the relevant bios based on simmilarity
                            query_embedding=model.encode([query])
                            k=len(chunks)
                            D,I = faiss_index.search(query_embedding, k=min(len(chunks), 2))
                            relevant_bios=[chunks[i] for i in I[0]]
                            filtered_bios=[bio for bio in relevant_bios]
                            for bio in filtered_bios:
                                # print(bio)
                                results.append(bio)
                                print("\n")

    return(results)
