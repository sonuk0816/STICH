from google import genai
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd



app = FastAPI()

# allowing frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setup openai
client = genai.Client()



# loading data globally
try:
    df = pd.read_csv("products.csv")
    
    # open text file normally
    file = open("policy.txt", "r")
    policy_text = file.read()
    file.close()
    
    print("Data loaded!")
except:
    print("Error: Could not find the files.")

class ChatRequest(BaseModel):
    message: str


# Function to search our local data
def search_data(user_message):
    msg = user_message.lower()
    context = ""

    # 1. Check if user wants policy info
    policies = ["return", "refund", "shipping", "delivery", "warranty", "policy"]
    policy_found = False
    
    for p in policies:
        if p in msg:
            policy_found = True
            break # stop looping if we find one

    if policy_found == True:
        context = context + "STORE POLICIES:\n" + policy_text + "\n\n"

    # 2. Check for products using a normal loop
    words = msg.split()
    found_items = []

    for index, row in df.iterrows():
        # UPDATED to match your exact CSV columns
        product_name = str(row['ProductName']).lower()
        description = str(row['Description']).lower()
        
        match = False
        # checking if any word from user matches the product name or description
        for w in words:
            # skipping tiny words so it doesn't match everything
            if len(w) > 3 and (w in product_name or w in description):
                match = True
        
        if match == True:
            found_items.append(row)
            # just get top 3 items so we don't send too much data
            if len(found_items) == 3:
                break
    
    # if we found products, add them to context
    if len(found_items) > 0:
        context = context + "PRODUCTS IN STOCK:\n"
        for item in found_items:
            # UPDATED to use ProductID, ProductName, and Price (INR)
            context = context + "ID: " + str(item['ProductID']) + " | Name: " + str(item['ProductName']) + " | Price: ₹" + str(item['Price (INR)']) + "\n"

    # if nothing matched, return default string
    if context == "":
        return "No matching products or policies found."
    
    return context

# API Route
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    user_msg = request.message

    # 1. Fetch relevant store context from your CSV
    my_context = search_data(user_msg)

    # 2. Build your prompt for Stitch
    prompt = f"""
    You are Stitch, a helpful virtual assistant for Stitch Culture.
    Use the following store context to answer the customer's question politely and concisely.

    CONTEXT:
    {my_context}

    CUSTOMER MESSAGE: {user_msg}
    """

    try:
        # 3. Call the Gemini model
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        return {"reply": response.text}

    except Exception as e:
        print(f"API Error: {e}")
        return {"reply": "Sorry, I am having trouble connecting to my brain right now."}


    #reload : uvicorn main:app --reload
    #port busy : lsof -ti:8000 | xargs kill -9
