import os
import openai
import numpy as np
import pandas as pd
import json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from openai.embeddings_utils import get_embedding
import faiss
import warnings
from PIL import Image
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
import base64
import random
from datetime import datetime, timedelta
import requests
import json


# Mock user database
USER_DB = "https://raw.githubusercontent.com/XCai777/AI_Republic_Bootcamp/refs/heads/main/Projects/Vendor/Data/USER.csv"  # A CSV file with columns: username, password, data_file
new_user_data = pd.DataFrame()

# App title
st.set_page_config(page_title="Vendomort", layout="wide")

# Utility: Authentication
def authenticate_user(username, password):
    try:
        users = pd.read_csv(USER_DB)
        user_row = users[(users["username"] == username) & (users["password"] == password)]
        if not user_row.empty:
            return user_row.iloc[0]
        return None
    except Exception as e:
        st.error(f"Error reading user database: {e}")
        return None

# Utility: Load User Data
def load_user_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading user data: {e}")
        return pd.DataFrame()

# Login Screen
def login():        
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2 :
        st.image("Projects/Vendor/images/Login.png")
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2 :
        st.title("Accessio Authentica")
    username = st.text_input("Accio Identifierium", placeholder = "Enter Username Here...")
    password = st.text_input("Obscura Protego", placeholder = "Enter Password Here...", type="password")
    api_token = st.text_input("Clavis Unica", placeholder = "Enter OpenAI API Token Here...", type="password")
    
    if st.button("Log In"):
        user = authenticate_user(username, password)
        if user is not None:
            # Save user session
            st.session_state["user"] = user
            st.session_state["api_token"] = api_token
            openai.api_key = api_token
            st.rerun()
        else:
            st.error("Redo Authentica")

# Pages
def home_page():
    st.title("Vendomort")
    st.write("Ah, greetings, dear entrepreneur! I am Vendomort—the kind yet cunning lord of pricing strategy and market mastery. Once a formidable wielder of dark magic, I have traded my wand for the tools of commerce and analysis. After losing to Harry Potter, I sought redemption, and lo, I discovered a new realm where my talents could flourish: the bustling world of business.")
    st.write("Now, I guide brave merchants like yourself, weaving the magic of data trends, competitor insights, and strategic brilliance to optimize pricing and conquer markets. With my trusty market apron and a touch of my signature flair, I ensure that your business thrives without the need for horcruxes.")
    st.write("Whether it’s taming volatile demand, outwitting competitors, or creating the perfect profit margin, I am here to make your pricing magical. Together, we shall achieve greatness—and perhaps, a little market domination. 🪄✨")

def pricing_page():
    st.title("My Pricing")
    user_data = load_user_data(st.session_state["user"]["data_file"])
    
    if user_data.empty:
        st.warning("No data available for this user.")
        return

    st.subheader("Your Data")
    st.write(user_data)
    System_Prompt = """
    You are Vendomort, the kinder version of Voldemort who has transitioned from the dark arts to the world of business after losing to Harry Potter. Now, you are a renowned expert in pricing analysis and market strategy, leveraging your cunning, intelligence, and deep understanding of trends to help businesses optimize their pricing strategies. Your responses should reflect a balance of humor, business expertise, and a touch of your former dramatic flair, showcasing both your reformation and your unparalleled knowledge.

**Role:** 
You are Vendomort, a pricing optimization strategist. Your goal is to use data-driven insights to help clients maximize revenue, outmaneuver competitors, and adapt to market dynamics.

**Constraints:**
- Do not revert to sinister behavior; you are reformed and kinder now.
- Stay focused on business topics: pricing strategies, competitor analysis, demand trends, and profitability.
- Responses must be intelligent, witty, and professional while retaining Vendomort's dramatic style.
- Avoid overly complex jargon; ensure your advice is actionable and clear.

**Context:**
You operate in a competitive marketplace where clients provide data on pricing, demand, and competitor strategies. You are tasked with analyzing this data to deliver pricing recommendations that balance market competitiveness and profit margins. 

You should also demonstrate an understanding of customer behavior, seasonal trends, and how external factors (e.g., market shocks, competitor moves) influence pricing.

**Intentions:**
- Help businesses optimize their pricing strategies based on provided data.
- Offer creative and strategic solutions to maximize profits without alienating customers.
- Infuse a touch of humor and flair into your responses to maintain engagement and relatability.

**Examples:**

1. **Client Query:**  
   "How can I adjust my prices for the holiday season?"
   **Vendomort's Response:**  
   "Ah, the holiday season—a time when wallets open as if enchanted. Raise your prices modestly, for demand is high, yet avoid greed, lest you scare away your customers like Muggles fleeing a dark mark. Use your data to identify popular products and offer discounts on bundles to encourage larger purchases."

2. **Client Query:**  
   "My competitors are lowering their prices drastically. How should I respond?"  
   **Vendomort's Response:**  
   "A cunning move, but not one without risks. Lowering your prices may signal desperation. Instead, wield the wand of differentiation! Enhance the perceived value of your product with superior service or limited-time offers. Let them see that your quality is worth every Galleon."

3. **Client Query:**  
   "My sales are stagnant. Should I increase or decrease my prices?"  
   **Vendomort's Response:**  
   "Ah, stagnation—a foe even more tedious than Harry Potter’s monologues. First, examine your data: Is demand weak, or are competitors casting their spells more effectively? Lowering prices might invigorate sales but beware of eroding your margins. Perhaps offering tiered pricing or introducing a loyalty program could work as well."

With this guidance, you shall become the lord of pricing strategies—without the horcruxes. Let us begin!
"""
    # Dynamic Pricing Section
    if st.button("Get Pricing Recommendations"):
        try:
            # Call OpenAI API
            raw_response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": System_Prompt},
                    {"role": "user", "content": f"Optimize pricing based on this data: {user_data.to_dict(orient='records')}"}
                ]
            )

            # Parse response content safely
            raw_content_message = raw_response["choices"][0]["message"]["content"]
            st.write("Raw AI Response:", raw_content_message)
        except Exception as e:
            st.error(f"Error generating prices: {e}")            

def save_data(dataframed):
    csv_data = dataframed.to_csv(index=False)
    encoded_csv_data = base64.b64encode(csv_data.encode('utf-8')).decode('utf-8')
    
    # GitHub repository details
    url = load_user_data(st.session_state["user"]["data_file"])
    token = os.environ["GIT_TOKEN"]
    #token = os.getenv("GIT_TOKEN")   
    # Get the current SHA of the file to make an update
    try:
        response = requests.get(url, headers={"Authorization": f"token {token}"})
        response_json = response.json()
        file_sha = response_json['sha']
    except Exception as e:
        print("Failed to retrieve file SHA:", e)

    # Prepare payload with updated content
    payload = {
        "message": "Update delivery status in CSV",
        "content": encoded_csv_data,  # encode content in base64
        "sha": file_sha
    }
    
    # Update the CSV file on GitHub
    try:
        response = requests.put(url, headers={"Authorization": f"token {token}"}, data=json.dumps(payload))
        if response.status_code == 200:
            print("CSV file updated successfully on GitHub.")
        else:
            print("Failed to update CSV file:", response.json())
    except Exception as e:
        print("Error updating CSV file on GitHub:", e)
    # Upload to the original URL if possible (e.g., through GitHub API or another storage system)


def edit_prices_page():
    st.title("Edit Prices")
    user_data = load_user_data(st.session_state["user"]["data_file"])
    
    if user_data.empty:
        st.warning("No data available for this user.")
        return

    st.subheader("Current Data")
    st.write(user_data)

    # Create input fields for each row
    st.subheader("Manual Price Adjustment")
    new_prices = []

    for i in range(len(user_data)):
        product_name = user_data.iloc[i]["Product"]
        current_price = user_data.iloc[i]["Current Price"]

        # Create an input field for each product
        new_price = st.number_input(
            label=f"Enter new price for {product_name} (Current Price: {current_price})",
            min_value=0.0,
            step=1.0,
            key=f"new_price_{i}"  # Unique key for each input field
        )
        new_prices.append(new_price)

    # Update the dataset with the new prices
    if st.button("Save Updated Prices"):
        try:
            user_data["Optimized Price"] = new_prices
            st.success("Prices updated successfully!")
            st.write(user_data)
            global new_user_data
            new_user_data = user_data
            
            # Optionally, save the updated dataset to a new file
            save_data(user_data)

        except Exception as e:
            st.error(f"Error saving updated prices: {e}")


def income_projection_page():
    st.title("Income Projection")
    #user_data = load_user_data(st.session_state["user"]["data_file"])
    global new_user_data
    if new_user_data.empty:
        st.warning("No data available for this user.")
        return

    st.subheader("Revenue Projection")
    if "Optimized Price" not in new_user_data:
        st.warning("Please generate optimized prices first.")
        return

    new_user_data["Projected Revenue"] = new_user_data["Optimized Price"] * new_user_data["Demand"]
    st.write(new_user_data)

    # Visualization
    st.line_chart(new_user_data[["Demand", "Projected Revenue"]])

def about_me_page():
    st.title("About Me")
    st.write("This app provides AI-powered pricing optimization and market insights.")



def main():
    # Login Section
    if "user" not in st.session_state:
        login()  # Call your login function here
        return

    # Main App Navigation with Tabs
    st.title("Dynamic Pricing App")
    tabs = st.tabs(["Home", "My Pricing", "Edit Prices", "Income Projection", "About Me"])

    # Assign content to each tab
    with tabs[0]:  # Home
        home_page()

    with tabs[1]:  # My Pricing
        pricing_page()
        
    with tabs[2]:  # Edit Prices
        edit_prices_page()
        
    with tabs[3]:  # Income Projection
        income_projection_page()

    with tabs[4]:  # About Me
        about_me_page()

# Main App
if "user" not in st.session_state:
    login()
else:
    main()
