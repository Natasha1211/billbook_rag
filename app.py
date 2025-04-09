# from datetime import datetime
# from main import chat_main
# from bson import ObjectId
# import requests
# import json
# import asyncio
# import sys
# from sentence_transformers import SentenceTransformer
# import streamlit.watcher.local_sources_watcher as lsw
# import streamlit as st

# def safe_get_module_paths(module):
#     paths_extractors = [
#         lambda m: [getattr(m, '__file__', None)],
#         lambda m: [getattr(m.__spec__, 'origin', None) if m.__spec__ else None],
#         lambda m: list(getattr(getattr(m, '__path__', []), '_path', [])) if hasattr(m, '__path__') else [],
#     ]
#     paths = set()
#     for extract in paths_extractors:
#         try:
#             results = extract(module)
#             if results:
#                 paths.update(filter(None, results))
#         except Exception:
#             continue
#     return paths

# lsw.get_module_paths = safe_get_module_paths


# def convert_to_serializable(obj):
#     if isinstance(obj, dict):
#         return {k: convert_to_serializable(v) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [convert_to_serializable(i) for i in obj]
#     elif isinstance(obj, datetime):
#         return obj.isoformat()
#     elif isinstance(obj, ObjectId):
#         return str(obj)
#     return obj 

# st.title('Billbook bot 🤖')

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# query = st.chat_input("Write your question here...")

# if query:
#     with st.chat_message("user"):
#         st.markdown(query)

#     st.session_state.messages.append({"role": "user", "content": query})    
#     query_sturcture=[{"question" : f"{query}", "businessId" : "67c5a2e6610c0de6560ecb22", "curent_business": "67c98620a081ecf70f1b3349"}]
    
#     with st.chat_message("assistant"):
#         with st.spinner("analyzing ..."):
#             message_placeholder = st.empty()
#             response = chat_main(query_sturcture)
#             serialized_response = convert_to_serializable(response)
#             with open("response.json", "w") as f:
#                 json.dump(serialized_response, f)
#             with open("response.json", "r") as f:
#                 data = json.load(f)
#             prompt=f"""
#             You are a helpful RAG based assistant that generates natural, detailed responses based on JSON data about customers, 
#             act as if you already know about the data, dont mention "Based on the data provided", "extract the following details" kind of phrases. 

#             Rules:
#             - Extract the detailed answer from each data you have been provided
#             - Replace $ with INR
#             - Act as if you know the data about the customer, and reply in such manner
#             - Summarize clearly based on the query
#             - Ignore null, empty, or missing values (mention that the user doesn't have those).
#             - Assume all currency is in INR (replace "$" with "INR").
#             - Do not give any ID's like Customer ID, '66c56e4dda11f3b0bb97729d', 'EasyBBINID5948885577' in information you provide, as it will be confidential.


#             [User Message]
#             Show me details for customer Ram Kumar.

#             [JSON Data]
#             {
#             "name": "Ram Kumar",
#             ...
#             }
            
#             Data:
#             {data}
#             Question:
#             {query}

#             Provide a clear and relevant answer to the question using the data above.
#             """
#             response = requests.post(
#                 'http://localhost:11434/api/generate',
#                 json={
#                     'model': 'llama3.2:latest',
#                     'prompt': prompt,
#                     'stream': True
#                 },
#                 stream=True
#             )
#             full_response = "" 
#             for line in response.iter_lines():
#                 if line:
#                     try:
#                         data=json.loads(line.decode('utf-8'))
#                         chunk=data.get("response", "")
#                         full_response += chunk
#                         message_placeholder.markdown(full_response)
#                     except json.JSONDecodeError:
#                         print("\n[Error parsing JSON]:", data)
#             st.session_state.messages.append({"role": "assistant", "content": full_response})



# """
# this code below is for checking the json data fetched is corect or not
# so that we can filter the data according to the question

# """



from datetime import datetime
from main import chat_main
from bson import ObjectId
import requests
import json
import asyncio
import sys
import streamlit.watcher.local_sources_watcher as lsw
import streamlit as st


def safe_get_module_paths(module):
    paths_extractors = [
        lambda m: [getattr(m, '__file__', None)],
        lambda m: [getattr(m.__spec__, 'origin', None) if m.__spec__ else None],
        lambda m: list(getattr(getattr(m, '__path__', []), '_path', [])) if hasattr(m, '__path__') else [],
    ]
    paths = set()
    for extract in paths_extractors:
        try:
            results = extract(module)
            if results:
                paths.update(filter(None, results))
        except Exception:
            continue
    return paths

lsw.get_module_paths = safe_get_module_paths

def convert_to_serializable(obj):
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, ObjectId):
        return str(obj)
    return obj 

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

st.title('Billbook bot 🤖')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Write your question here...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append({"role": "user", "content": query})    
    query_sturcture=[{"question" : f"{query}", "businessId" : "67c5a2e6610c0de6560ecb22", "curent_business": "67c98620a081ecf70f1b3349"}]
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = chat_main(query_sturcture)
        if response:
            serialized_response = convert_to_serializable(response)
            formatted_json = json.dumps(serialized_response, indent=2)
            st.markdown(f"```json\n{formatted_json}\n```")
            st.session_state.messages.append({"role": "assistant", "content": serialized_response})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "No data found regarding the customer."})
            