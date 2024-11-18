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
            st.experimental_rerun()
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
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a pricing optimization AI."},
                    {"role": "user", "content": f"Optimize pricing based on this data: {user_data.to_dict(orient='records')}"}
                ]
            )
            suggestions = eval(response["choices"][0]["message"]["content"])  # Ensure the model output is valid Python
            user_data["Optimized Price"] = suggestions
            st.success("Pricing optimization complete!")
            st.write(user_data)
        except Exception as e:
            st.error(f"Error generating prices: {e}")

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

# Main App
if "user" not in st.session_state:
    login()
else:
    # Top Navigation Menu
    menu = st.selectbox("Menu", ["Home", "My Pricing", "Income Projection", "About Me"], key="menu")

    if menu == "Home":
        home_page()
    elif menu == "My Pricing":
        pricing_page()
    elif menu == "Income Projection":
        income_projection_page()
    elif menu == "About Me":
        about_me_page()