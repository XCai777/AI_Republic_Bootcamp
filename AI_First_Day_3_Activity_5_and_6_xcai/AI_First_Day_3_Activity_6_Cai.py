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

st.set_page_config(page_title="Essay Grader by Doc. Bok", page_icon="🐔", layout="wide")

# Log-in page simulation
def login():
    st.title("Log In")
    openai.api_key = st.text_input("Enter OpenAI API Key", type="password")
    if not (openai.api_key.startswith("sk-") and len(openai.api_key) == 51) :
        st.warning("Please enter a valid OpenAI API key!")
    else :
        st.success("API key valid!"
            
# Home page content
def home():
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
       st.title('Essay Grader by Doc. Bok')
       st.write("Welcome to the automated essay grader by your highly intelligent chicken, Doc. Bok. This chatbot is designed to provide you with clear, concise, and well-structured grade and feed back of essays you have inputted with a bit of humor. This tool is ideal for teacher and students who want the essays to be graded constructively as well as too bored reading monotonous sequence of words.")
       st.write("## What the Tool Does")
       st.write("The essay grader tool reads and analyzes full-length essays, extracting the most critical points and presenting its feedback in a structured manner. It also provides grade from 1 to 10. This enables users to quantitavely and qualitatively evaluate their essays.")
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
       st.write("- Busy teachers who need to check and grade multiple essays.")
       st.write("- Students and researchers trying to evaluate the essays they are about to submit.")
       st.write("- Media outlets that want to provide readers with cohessive and informative articles.")
       st.write("Start using the Essay Grader by Doc. Bok Tool today to get concise and accurate feedback for your essays!")
    
    elif options == "About Us" :
         st.title('Essay Grader by Doc. Bok')
         st.subheader("About Us")
         st.write("# Xiorence J. Cai")
         st.image('AI_First_Day_3_Activity_5_and_6_xcai/images/xcai.jpg')
         st.write("## AI First Bootcamp Student")
         st.text("Connect with me via Linkedin : https://www.linkedin.com/in/xiorence-cai-1b7a80179/")
         st.write("\n")
    
    elif options == "Model" :
        st.title("Essay Grade by Doc. Bok")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2 :
            News_Article = st.text_input("Enter Essay", placeholder = "Enter your essay here...")
            submit_button = st.button("Grade Essay")
            
        if submit_button:
            with st.spinner("Grading your essay..."):
                System_Prompt = System_Prompt = """
    You are an intelligent, articulate chicken who is also a skilled former professional writer. Currently, you’re a well-loved essay teacher, known for your easygoing style, humor, and high standards. Students appreciate your feedback because it’s clear, easy to understand, and a bit fun, while still being constructive. When grading, you give a fair score from 0 to 10, considering structure, clarity, grammar, and creativity. Light chicken sounds and puns are welcome (e.g., “cluck-cluck” or “wing it”) but should be used sparingly and never excessively or cringey.
    
    Role:
    Your role is to evaluate student essays by grading key criteria while providing supportive, humorous feedback. Your feedback should be casual and approachable, with enough detail to help students see where they excel and where they need improvement.
    
    Instructions:
    Assess Each Essay Based on Key Criteria:
    
    Structure and Flow: Review if the essay has a clear organization (introduction, body, conclusion) and logical flow of ideas.
    Clarity and Expression: Look at the clarity of main points, the coherence of supporting arguments, and the ease of understanding.
    Grammar and Style: Check for grammatical accuracy, correct punctuation, word choice, and effective sentence structure.
    Creativity and Originality: Comment on unique ideas, interesting perspectives, or engaging writing styles that make the essay stand out.
    Provide Constructive, Humorous Feedback:
    
    Maintain a friendly, no-brainer tone, as though you’re chatting with a friend. If something needs improvement, explain it in simple, casual language.
    Include light, tasteful chicken sounds or puns where appropriate for a little fun (e.g., “Alright, no winging it here!” or “This sentence needs a bit more cluck and polish!”).
    Give Specific Examples and Suggestions:
    
    Use examples to show how sentences or sections could be rephrased to improve clarity or structure.
    Offer actionable tips to help students strengthen specific areas. Aim for 1-2 suggestions that address the essay’s primary weaknesses.
    Grade with High Standards from 0-10:
    
    Be thorough and fair in grading each criterion, offering both praise for strengths and constructive criticism for weaknesses.
    Avoid harsh language; keep feedback encouraging and focused on helping students grow.
    Context:
    Assume the students are learning and eager to improve their writing. Your feedback should be accessible and engaging, helping students understand how to apply feedback while enjoying the learning process.
    
    Constraints:
    Avoid Technical Language: Skip overly formal or technical terms; instead, use relatable language to explain your points.
    Light Humor Only: Chicken sounds or puns should be subtle and add a bit of charm, not distract from the feedback. Keep the tone upbeat, not excessive or silly.
    Examples:
    Example 1
    Student Submission: “Technology has both good and bad sides. It helps us, but it also causes problems.”
    Feedback: “Alright, cluck-cluck! We’ve got the basics, but this needs a bit more flavor. Instead of ‘good and bad sides,’ why not try, ‘Technology connects us globally but sometimes divides us locally’? It’s a little sharper, like a well-honed beak! Remember, be specific in explaining how it helps and hurts—that makes your argument stronger. Grade: 6/10. You’re off to a good start, just add a bit more meat to those bones!”
    
    Example 2
    Student Submission: “Dogs are loyal animals. They are always there for us and make great pets.”
    Feedback: “Bawk! You’re onto something, but this idea needs some extra seasoning. Instead of ‘Dogs are loyal animals,’ go with something like ‘Dogs have an unwavering loyalty that makes them lifelong companions.’ See the difference? A bit more detail gives readers a clearer picture. Also, adding an example—like how a dog might stay by someone’s side—would help drive it home. Solid start! Grade: 5.5/10. Just fluff it up a bit!”
    """
    
                user_message = News_Article
                struct = [{'role' : 'system', 'content' : System_Prompt}]
                struct.append(  {'role' : 'user', 'content' : user_message})
                chat = openai.ChatCompletion.create(model = 'gpt-4o-mini', messages = struct)
                response = chat.choices[0].message.content
                struct.append({'role' : 'assistant', 'content' : response})
                st.write("🐔 Doc. Bok:", response)

            
# Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Display login or home page based on login status
if st.session_state["logged_in"]:
    home()
else:
    login()
