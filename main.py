from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from openai import OpenAI

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
client = OpenAI(api_key="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")

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
    
    # get the text from our csv and txt file
    my_context = search_data(user_msg)
    
    # build the prompt for chatgpt
    prompt = "You are Stitch, a chatbot for Stitch Culture. Use ONLY this context to answer. If asked about products, give the ID and price. Context: \n" + my_context
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.3
        )
        
        reply = response.choices[0].message.content
        return {"reply": reply}
        
    except Exception as e:
        print("API Error:", e)
        return {"reply": "Sorry, server error. Please try again."}


    #reload : uvicorn main:app --reload
    #port busy : lsof -ti:8000 | xargs kill -9