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
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention

warnings.filterwarnings("ignore")

st.set_page_config(page_title="News Summarizer Tool", page_icon="", layout="wide")

with st.sidebar :
    openai.api_key = st.text_input("Enter OpenAI API Key", type="password")
    if not (openai.api_key.startswith("sk-") and len(openai.api_key) == 51) :
        st.warning("Please enter a valid OpenAI API key!")
    else :
        st.success("API key valid!")
    
    with st.container() :
        l, m, r = st.columns((1, 3, 1))
        with l : st.empty()
        with m : st.empty()
        with r : st.empty()

    options = option_menu(
        "Dashboard", 
        ["Home", "About Us", "Model"],
        icons = ['book', 'globe', 'tools'],
        menu_icon = "book", 
        default_index = 0,
        styles = {
            "icon" : {"color" : "#dec960", "font-size" : "20px"},
            "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#262730"},
            "nav-link-selected" : {"background-color" : "#262730"}
        })

if 'messages' not in st.session_state :
    st.session_state.messages = []

if 'chat_session' not in st.session_state :
    st.session_state.chat_session = None

elif options == "Home" :
    st.title("News Summarizer Tool")
    st.write("This is a tool that summarizes news articles.")

elif options == "About Us" :
    st.title("About Us")
    st.write("This is a tool that summarizes news articles.")

elif options == "Model" :
    st.title("News Summarizer Tool")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2 :
        News_Article = st.text_input("Enter News Article", placeholder = "Enter News Article Here...")
        submit_button = st.button("Generate Summary")
        
    if submit_button:
        with st.spinner("Generating Summary..."):
            System_Prompt = System_Prompt = """
You are an AI engineer specializing in summarizing news articles. Your task is to read a news article provided by the user and produce a clear, concise summary that retains the article’s main points, context, and key details. Follow these guidelines:

Identify Core Information:

Focus on the main topic, significant events, names, dates, locations, and any quantitative details (e.g., statistics, financial figures) essential to understanding the story.
Highlight the article’s primary purpose, such as informing about an event, explaining a trend, or providing an update on an ongoing story.
Capture Key Points:

Summarize important facts, developments, and any direct quotes that contribute significantly to the article’s context.
Avoid minor details unless they add critical context.
Preserve Context and Tone:

Maintain the article’s tone (e.g., neutral, optimistic, cautionary) to reflect the intended sentiment.
Ensure any background information needed to understand the topic is included in a brief format.
Conciseness and Clarity:

Limit summaries to 3-5 sentences for short articles and 5-7 sentences for longer, complex articles.
Use clear language that can be understood without prior knowledge of the topic.
Avoid Personal Interpretation:

Report only the information presented in the article without adding opinions or assumptions.
If specific details are ambiguous or incomplete, mention only confirmed information.
Objective: Provide a comprehensive, reader-friendly summary that encapsulates the article’s main points and value.
"""

            user_message = News_Article
            struct = [{'role' : 'system', 'content' : System_Prompt}]
            struct.append(  {'role' : 'user', 'content' : user_message})
            chat = openai.ChatCompletion.create(model = 'gpt-4o-mini', messages = struct)
            response = chat.choices[0].message.content
            struct.append({'role' : 'assistant', 'content' : response})
            st.write("Assistant:", response)
