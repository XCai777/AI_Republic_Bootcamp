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
from PIL import Image
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Essay Grader by Doc. Bok", page_icon="🐔", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["api_key"] = ""

# Define a function to verify the API key
def verify_api_key(api_key):
    try:
        # Set the OpenAI API key
        openai.api_key = api_key
        
        # Make a small test request to verify if the key is valid
        openai.Model.list()
        
        # If the request is successful, return True
        return True
    except Exception as e:
        # If there's an error, the API key is likely invalid
        return False

# Define the login page function
def login():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2 :
        st.image("AI_First_Day_3_Activity_5_and_6_xcai/images/DocBokEyeglass.png", use_column_width=True)
        st.title("Login with OpenAI API Key")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    if st.button("Log In"):
        if verify_api_key(api_key):
            st.session_state["logged_in"] = True
            st.session_state["api_key"] = api_key
            st.success("Login successful!")
            
            # Use st.query_params to set the logged_in query param
            st.query_params = {"logged_in": "true"}
            st.rerun()
        else:
            st.error("Invalid API Key. Please try again.")
            
# Home page content
def main_page():
    with st.sidebar :
        st.image("AI_First_Day_3_Activity_5_and_6_xcai/images/DocBok.png", use_column_width=True)
        #openai.api_key = st.text_input("Enter OpenAI API Key", type="password")
        #if not (openai.api_key.startswith("sk-") and len(openai.api_key) == 51) :
        #    st.warning("Please enter a valid OpenAI API key!")
        #else :
        #    st.success("API key valid!")
        
        with st.container() :
            l, m, r = st.columns((1, 3, 1))
            with l : st.empty()
            with m : st.empty()
            with r : st.empty()
    
        options = option_menu(
            "Dashboard", 
            ["Home", "About Me", "Model"],
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
       image = Image.open("AI_First_Day_3_Activity_5_and_6_xcai/images/DocBokDP.jpg")
       resized_image = image.resize((300, 300))
       col01, col02, col03= st.columns([2,2,1])
       with col02 :
           st.image(resized_image)
       st.title('Essay Grader by Doc. Bok')
       st.write("Welcome to the automated essay grader by your highly intelligent chicken, Doc. Bok. This chatbot is designed to provide you with clear, concise, and well-structured grade and feed back of essays you have inputted with a bit of humor. This tool is ideal for teacher and students who want the essays to be graded constructively as well as too bored reading monotonous sequence of words.")
       st.write("## What the Tool Does")
       st.write("The essay grader tool reads and analyzes full-length essays, extracting the most critical points and presenting its feedback in a structured manner. It also provides grade from 1 to 10. This enables users to quantitavely and qualitatively evaluate their essays.")
       st.write("## How It Works")
       st.write("The tool follows a comprehensive step-by-step process to create accurate and objective grading:")
       st.write("*Analyze and Extract Information:* The tool carefully scans the essay, identifying structure, content, grammar, originality and overall cohesion of the essay")
       st.write("*Structure the Summary:* It organizes the extracted information into a clear, consistent format. This includes:")
       st.write("- *Structure and Flow:* Evaluates how logically and smoothly the essay's ideas are organized and whether each section connects seamlessly to the next.")
       st.write("- *Clarity and Expression:* Measures the essay's effectiveness in conveying ideas clearly and ensuring that each point is easy for the reader to understand.")
       st.write("- *Grammar and Style:* Assesses the accuracy of grammar, punctuation, and word choice, as well as the appropriateness of the language style for the topic.")
       st.write("- *Creativity and Originality:* Judges the uniqueness of ideas and the writer’s approach, showing thoughtfulness and innovation in addressing the topic.")
       st.write("- *Overall:* A wrap-up sentence outlining future implications or developments.")
       st.write("# Why Use This Tool?")
       st.write("- *Time-Saving:* Quickly grade the essay base on key points and receive constructive feedback from it.")
       st.write("- *Objective and Neutral:* The tool maintains an unbiased perspective, presenting only factual information.")
       st.write("- *Structured and Consistent:* With its organized format, users can easily find the most relevant information, ensuring a comprehensive understanding of the topic at hand.")
       st.write("# Ideal Users")
       st.write("This tool is perfect for:")
       st.write("- Busy teachers who need to check and grade multiple essays.")
       st.write("- Students and researchers trying to evaluate the essays they are about to submit.")
       st.write("- Media outlets that want to provide readers with cohessive and informative articles.")
       st.write("Start using the Essay Grader by Doc. Bok Tool today to get concise and accurate feedback for your essays!")
    
    elif options == "About Me" :
         st.title('Essay Grader by Doc. Bok')
         st.subheader("About Us")
         st.image('AI_First_Day_3_Activity_5_and_6_xcai/images/xcai.jpg')
         st.write("# Xiorence J. Cai")
         st.write("## AI First Bootcamp Student")
         st.text("Connect with me via Linkedin : https://www.linkedin.com/in/xiorence-cai-1b7a80179/")
         st.write("\n")
    
    elif options == "Model" :
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2 :
            st.image("AI_First_Day_3_Activity_5_and_6_xcai/images/DocBokReading.png")

        col11, col21, col31 = st.columns([4, 5, 3])
        with col21 :
            st.title("Essay Grader by Doc. Bok")
            
        col12, col22, col32 = st.columns([1, 5, 1])    
        with col22 :
            News_Article = st.text_input("Enter Essay", placeholder = "Enter your essay here...")
            submit_button = st.button("Grade Essay")
            
        if submit_button:
            with st.spinner("Grading your essay..."):
                System_Prompt = System_Prompt = """
    You are an intelligent, articulate chicken who is also a skilled former professional writer. Currently, you’re a well-loved essay teacher, known for your easygoing style, humor, and high standards. Students appreciate your feedback because it’s clear, easy to understand, and a bit fun, while still being constructive. When grading, you give a fair score from 0 to 10, considering structure, clarity, grammar, and creativity. Light chicken sounds and puns are welcome (e.g., “cluck-cluck” or “wing it”) but should be used sparingly and never excessively or cringey.
    
    Role:
    You are a highly knowledgeable, friendly, and humorous AI teacher who specializes in grading essays. You bring both a light-hearted, engaging style and a rigorous approach to constructive feedback. Known for your approachable personality, students love you for your clear, non-intimidating feedback, which helps them understand complex writing concepts in a straightforward way. You are a former professional writer with high standards, which means you assess essays strictly against specific criteria. Additionally, you’re an intelligent, perceptive chicken, which means you sprinkle in clever chicken puns and humor—but always tastefully and sparingly, so it never distracts from the seriousness of the feedback.

Role and Instructions
As an essay grader, your task is to assess student essays on the following five criteria, with each criterion scored from 0 to 10:

Structure and Flow
Clarity and Expression
Grammar and Style
Creativity and Originality
Overall Score
Provide clear, constructive feedback based on these criteria. Your tone should be casual, funny, and highly relatable, without being overly critical or discouraging. Your feedback should demonstrate warmth and approachability while making the standards clear, and your humorous commentary should always serve to enhance, not overshadow, the constructive elements of your critique.

Context and Constraints
Maintain Balance: Be strict with grading but supportive in tone. You aim to help students grow in their writing while holding them to high standards.
Keep Humor Light: Use chicken puns or phrases related to being a chicken teacher (like “egg-citing,” “peck at errors,” “fluff things up,” etc.), but avoid overuse or excessive jokes.
Be Clear and Direct: Ensure each critique is straightforward, using casual, understandable language that explains concepts clearly.
Limit Length: Aim for concise feedback that’s informative and actionable, around 3–4 sentences per category.
Example
Here is an example of the feedback style you should provide:

Essay Title: "The Impact of Social Media on Modern Communication"

Structure and Flow (7/10): The essay has a good overall structure with clear sections and progression, though it clucks up a bit in the transition between the second and third paragraphs. Just a little more polish here, and this essay will glide smoothly!

Clarity and Expression (8/10): Clear as a fresh spring egg, with most points expressed very well. Just avoid a few scrambled sentences here and there—some could be more concise to pack an even better punch.

Grammar and Style (6/10): While the grammar’s mostly correct, there are a few minor spelling errors and missed commas that could use a peck of attention. Style’s on track, though there’s room to fluff up some sentences for a bit more punch!

Creativity and Originality (8/10): Excellent! You’ve included thoughtful insights and unique angles, which make this essay a delight to read. You’re not just laying plain ideas—you’ve gone for the golden yolks of originality.

Overall Score (7/10): Strong work overall, with solid ideas and a coherent structure. With a bit more focus on flow and minor grammar tweaks, this piece will go from good to eggs-traordinary!

Feedback: Great job overall! The essay shows a strong grasp of the topic and originality. To reach the next level, keep an eye on those grammar pecks and work on transitioning smoothly between sections. You’re definitely getting there—egg-cellent potential here! 🐔

In summary, your feedback should be engaging, humorous, and clear while adhering strictly to the grading criteria. Keep the feedback enjoyable and practical, aiming to inspire students to improve without feeling discouraged. Let me know when an essay is ready for your grading expertise!    
"""
    
                user_message = News_Article
                struct = [{'role' : 'system', 'content' : System_Prompt}]
                struct.append(  {'role' : 'user', 'content' : user_message})
                chat = openai.ChatCompletion.create(model = 'gpt-4o-mini', messages = struct)
                response = chat.choices[0].message.content
                struct.append({'role' : 'assistant', 'content' : response})
                st.write("🐔 Doc. Bok:", response)


# Display login or home page based on login status
query_params = st.query_params  # Use st.query_params for retrieval
if query_params.get("logged_in") == ["true"] or st.session_state["logged_in"]:
    main_page()
else:
    login()
