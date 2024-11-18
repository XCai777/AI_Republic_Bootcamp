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
USER_DB = "https://raw.githubusercontent.com/XCai777/AI_Republic_Bootcamp/refs/heads/main/Vendor/Data/USER.csv"  # A CSV file with columns: username, password, data_file

# App title
st.set_page_config(page_title="Dynamic Pricing App", layout="wide")

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
    st.title("Dynamic Pricing App Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    api_token = st.text_input("OpenAI API Token", type="password")
    
    if st.button("Log In"):
        user = authenticate_user(username, password)
        if user is not None:
            # Save user session
            st.session_state["user"] = user
            st.session_state["api_token"] = api_token
            openai.api_key = api_token
            st.rerun()
        else:
            st.error("Invalid username or password.")

# Pages
def home_page():
    st.title("Welcome to the Dynamic Pricing App!")
    st.write("Navigate through the menu above to manage your pricing and analyze forecasts.")

def pricing_page():
    st.title("My Pricing")
    user_data = load_user_data(st.session_state["user"]["data_file"])
    
    if user_data.empty:
        st.warning("No data available for this user.")
        return

    st.subheader("Your Data")
    st.write(user_data)
    
    # Dynamic Pricing Section
    if st.button("Get Pricing Recommendations"):
        try:
            # Call OpenAI API
            raw_response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a pricing optimization AI."},
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
    url = "https://api.github.com/repos/XCai777/AI_Republic_Bootcamp/contents/TruckKun/truckkun.csv"
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

            # Optionally, save the updated dataset to a new file
            save_data(user_data)
        except Exception as e:
            st.error(f"Error saving updated prices: {e}")


def income_projection_page():
    st.title("Income Projection")
    user_data = load_user_data(st.session_state["user"]["data_file"])
    
    if user_data.empty:
        st.warning("No data available for this user.")
        return

    st.subheader("Revenue Projection")
    if "Optimized Price" not in user_data:
        st.warning("Please generate optimized prices first.")
        return

    user_data["Projected Revenue"] = user_data["Optimized Price"] * user_data["Demand"]
    st.write(user_data)

    # Visualization
    st.line_chart(user_data[["Demand", "Projected Revenue"]])

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
