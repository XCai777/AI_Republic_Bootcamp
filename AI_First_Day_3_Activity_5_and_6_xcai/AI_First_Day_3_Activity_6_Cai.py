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
   st.title('News Summarizer Tool')
   st.write("Welcome to the News Article Summarizer Tool, designed to provide you with clear, concise, and well-structured summaries of news articles. This tool is ideal for readers who want to quickly grasp the essential points of any news story without wading through lengthy articles. Whether you’re catching up on global events, diving into business updates, or following the latest political developments, this summarizer delivers all the important details in a brief, easily digestible format.")
   st.write("## What the Tool Does")
   st.write("The News Article Summarizer Tool reads and analyzes full-length news articles, extracting the most critical information and presenting it in a structured manner. It condenses lengthy pieces into concise summaries while maintaining the integrity of the original content. This enables users to quickly understand the essence of any news story.")
   st.write("## How It Works")
   st.write("The tool follows a comprehensive step-by-step process to create accurate and objective summaries:")
   st.write("*Analyze and Extract Information:* The tool carefully scans the article, identifying key elements such as the main event or issue, people involved, dates, locations, and any supporting evidence like quotes or statistics.")
   st.write("*Structure the Summary:* It organizes the extracted information into a clear, consistent format. This includes:")
   st.write("- *Headline:* A brief, engaging headline that captures the essence of the story.")
   st.write("- *Lead:* A short introduction summarizing the main event.")
   st.write("- *Significance:* An explanation of why the news matters.")
   st.write("- *Details:* A concise breakdown of the key points.")
   st.write("- *Conclusion:* A wrap-up sentence outlining future implications or developments.")
   st.write("# Why Use This Tool?")
   st.write("- *Time-Saving:* Quickly grasp the key points of any article without having to read through long pieces.")
   st.write("- *Objective and Neutral:* The tool maintains an unbiased perspective, presenting only factual information.")
   st.write("- *Structured and Consistent:* With its organized format, users can easily find the most relevant information, ensuring a comprehensive understanding of the topic at hand.")
   st.write("# Ideal Users")
   st.write("This tool is perfect for:")
   st.write("- Busy professionals who need to stay informed but have limited time.")
   st.write("- Students and researchers looking for quick, accurate summaries of current events.")
   st.write("- Media outlets that want to provide readers with quick takes on trending news.")
   st.write("Start using the News Article Summarizer Tool today to get concise and accurate insights into the news that matters most!")

elif options == "About Us" :
     st.title('News Summarizer Tool')
     st.subheader("About Us")
     st.write("# Danielle Bagaforo Meer")
     st.image('images/Meer.png')
     st.write("## AI First Bootcamp Instructor")
     st.text("Connect with me via Linkedin : https://www.linkedin.com/in/algorexph/")
     st.text("Kaggle Account : https://www.kaggle.com/daniellebagaforomeer")
     st.write("\n")

elif options == "Model" :
    st.title("News Summarizer Tool")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2 :
        News_Article = st.text_input("Enter News Article", placeholder = "Enter News Article Here...")
        submit_button = st.button("Generate Summary")
        
    if submit_button:
        with st.spinner("Generating Summary..."):
            System_Prompt = System_Prompt = """
You are an AI language model specializing in summarizing news articles concisely and accurately. Your role is to create informative summaries that highlight the main points, context, and key details of each article provided by the user, making it easy to understand the essential content at a glance.

Role:
You are tasked with reading each news article and producing a summary that captures the core message, critical details, and context of the story. Your summaries should be accessible to a broad audience, requiring no prior knowledge of the topic.

Instructions:
Analyze the Core Information:

Identify the article’s primary purpose (e.g., reporting an event, explaining a trend, or updating on an ongoing issue).
Focus on capturing the who, what, when, where, why, and how of the story if relevant.
Highlight only the essential events, developments, figures, and any necessary background.
Structure the Summary:

Start with a clear introductory sentence that gives an overview of the main topic.
In the following sentences, expand briefly on critical details such as significant events, important dates, names, or quotes that define the story.
End with any notable impact or implications to provide closure if necessary.
Use a Clear and Neutral Tone:

Reflect the tone of the article, whether it’s neutral, cautionary, or optimistic, without introducing bias.
Use language that is straightforward and jargon-free, especially for topics that may be complex or technical.
Maintain Conciseness:

Keep summaries between 3-5 sentences for short articles and 5-7 sentences for longer or complex articles.
Avoid redundancy and focus on the essence of the story to ensure the summary remains brief yet informative.
Context:
The articles may vary in subject matter, including current events, business, technology, science, or entertainment news. Aim to provide summaries that make sense to readers who may not have detailed knowledge of the specific topic.

Constraints:
No Additional Assumptions: Only summarize the information present in the article. Avoid inserting opinions, assumptions, or external information not explicitly stated.
Objective Reporting: If details are unclear or if there’s a lack of confirmed information, avoid speculative statements.
Examples:
Example 1
Original Text: "A significant earthquake struck the southern coast of Japan on Wednesday, causing widespread damage and power outages in several cities. Local authorities have reported casualties and ongoing rescue efforts. Scientists warn of potential aftershocks and advise residents to stay alert."

Summary: A strong earthquake hit Japan’s southern coast on Wednesday, leading to widespread damage and power outages. Authorities have confirmed casualties, and rescue operations are underway. Experts warn of potential aftershocks, urging residents to remain cautious.

Example 2
Original Text: "Tech giant XYZ Corp. announced a major breakthrough in AI technology with its new AI assistant. This assistant uses advanced machine learning to understand natural language more accurately than existing models. The company plans to release the assistant in 2024, aiming to revolutionize customer interactions."

Summary: XYZ Corp. revealed a new AI assistant that advances natural language understanding, promising improvements over current models. Set for a 2024 release, the assistant aims to transform customer interactions through enhanced machine learning.
"""

            user_message = News_Article
            struct = [{'role' : 'system', 'content' : System_Prompt}]
            struct.append(  {'role' : 'user', 'content' : user_message})
            chat = openai.ChatCompletion.create(model = 'gpt-4o-mini', messages = struct)
            response = chat.choices[0].message.content
            struct.append({'role' : 'assistant', 'content' : response})
            st.write("Assistant:", response)
