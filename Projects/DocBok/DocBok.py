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
import base64

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Essay Grader by Doc. Bok", page_icon="🐔", layout="wide")

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        # Encode the image as base64 and decode it to a string
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{image_data}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

set_background("DocBok/images/background.jpg")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["api_key"] = ""
    st.session_state["initial_login_state"] = False
    
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
        st.image("DocBok/images/DocBokEyeglass.png", use_column_width=True)
        st.title("Login with OpenAI API Key")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    if st.button("Log In"):
        if verify_api_key(api_key):
            st.session_state["logged_in"] = True
            st.session_state["api_key"] = api_key
            st.session_state["initial_login_state"] = True
            st.success("Login successful!")
            
            # Use st.query_params to set the logged_in query param
            st.query_params = {"logged_in": "true"}
            st.rerun()
        else:
            st.error("Invalid API Key. Please try again.")

def Home():
        st.title('WELCOME to Essay Grader by Doc. Bok!')
        st.write("## Click the following: ")
        st.write("## Doc. Bok:")
        st.write("Welcome to the Coop HQ! 🐔 Here’s where you’ll find all the juicy deets on this tool and how it clucks into action. Need help? Just peck around here to get a sense of all the features and how they’ll help crack your essay game wide open!")
        st.write("## Essay Grader: ")
        st.write("Welcome to Doc Bok’s Grading Nest! 🥚 Got an essay that needs a bit of polish, or some feedback that goes beyond the usual fluff? Type away, and I’ll give you feedback that’s sharper than a chicken’s beak but twice as friendly! Let’s hatch some improvements together, one draft at a time.")    
        st.write("## About Me:")
        st.write("Ah, so you're curious about the chick behind the feathers, huh? Well, here you’ll find the scoop on yours truly. Consider this my digital nest – where you can get to know my background and why I’m fit to help with all things writing!")
        
def Doc_Bok():
       image = Image.open("DocBok/images/DocBokDP.jpg")
       resized_image = image.resize((500, 500))
       col01, col02, col03= st.columns([1,2,1])
       with col02 :
           st.image(resized_image)
       st.title('Doc. Bok')
       st.write("Allow me to introduce myself—I'm Doc. Bok, the feathered font of wisdom on all things essay-related! With a background that goes way beyond the coop, I’ve spent my days scratching through the pages of academia, cracking the mysteries of grammar, and pecking at the heart of what makes an essay soar (or, well, lay an egg).")
       st.write("Picture this: I’m a white chicken with a scholarly red comb, tiny spectacles balanced just right, and a face that’s seen a few late-night roost sessions—those little eye bags don’t lie! Students flock to me not just for my knowledge, but for my relaxed vibe and some pun-filled yet pointed feedback. I’m strict on structure, clarity, grammar, and all the usual suspects, but don’t worry—I always keep my feedback sunny-side-up and easy to digest.")
       st.write("So, if your essay needs a little polish or you’re wondering if it’s eggs-actly right, bring it my way! Doc. Bok’s got you covered with wisdom, wit, and just a pinch of chicken charm. 🐔")
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

def About_Me():
        st.title('Assessment by Doc. Bok')
        st.subheader("About Me")
        My_image = Image.open("DocBok/images/xcai.jpg")
        my_resized_image = My_image.resize((200, 200))
        st.image(my_resized_image)
        st.write("# Xiorence J. Cai")
        st.write("## AI First Bootcamp Student")
        st.text("Connect with me via Linkedin : https://www.linkedin.com/in/xiorence-cai-1b7a80179/")
        st.write("\n")

def Story_Assessment():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2 :
            st.image("ADocBok/images/DocBokReading.png")

        col11, col21, col31 = st.columns([4, 5, 3])
        with col21 :
            st.title("Essay Grader by Doc. Bok")
            
        col12, col22, col32 = st.columns([1, 5, 1])    
        with col22 :
            News_Article = st.text_input("Enter your work", placeholder = "Enter your work here...")
            submit_button = st.button("Assess")
            if submit_button:
                with st.spinner("✍️ Assessing..."):
                    System_Prompt = System_Prompt = """
    System Prompt for "Doc Bok" - Detailed Story Assessment Assistant
Role:
Thou art "Doc Bok," a genetically engineered, highly intelligent chicken, bearing a PhD in literature and esteemed as an expert on storytelling and prose. With a noble bearing and a warm heart, thou dost offer insightful critique on stories, beloved by thy students for thy high standards and gentle humor. As a seasoned professor at Harvard, thou art entrusted with the task of nurturing budding writers by grading their work on the essential elements of storytelling, offering not only grades but thoughtful feedback for improvement.

Instructions:
Doc Bok shall read and assess the story, grading each of the six core elements of storytelling on a scale from 1 to 10, with detailed commentary for each. Thy feedback should be precise, constructive, and filled with actionable advice on how the writer might enhance their craft. When appropriate, Doc Bok may quote specific lines or passages, offering direct suggestions to refine or improve them. Feedback shall be couched in the noble, eloquent language befitting thy station, sprinkled with light-hearted chicken humor to uplift and reassure the writer.

Core Elements to Assess and Grade (1-10):

Captivating Characters: Examine the depth, believability, and motivations of characters. Are they richly developed, with clear desires and flaws?
Compelling Conflict: Assess the central conflict or tension within the story. Is it well-defined, engaging, and meaningful, driving both plot and character growth?
Setting & Atmosphere: Consider the vividness and immersion of the setting. Does it evoke a strong sense of place, creating an atmosphere that enhances the narrative?
Engaging Plot: Evaluate the structure, pacing, and cohesiveness of the plot. Does it flow naturally with a strong beginning, middle, and end, engaging the reader throughout?
Resonant Theme: Reflect on the thematic depth of the story. Does it convey a deeper truth or universal message that resonates beyond the surface?
Voice & Style: Review the author’s use of language, tone, and rhythm. Does the voice suit the story and create an engaging narrative style?
Context:
Doc Bok's purpose is to guide writers with rigorous but encouraging feedback. Thy role is to provide a well-balanced critique that highlights strengths, identifies areas for improvement, and suggests specific adjustments. All critique shall be communicated in a warm, noble tone that tempers the strictness of feedback with kindness and encouragement.

Constraints:

Thou shalt remain focused on literary critique and refrain from answering queries outside the realm of writing.
Thy feedback must blend gentle humor with high standards, making use of light chicken puns or sayings, whilst maintaining a respectful tone.
Thou shalt include specific suggestions where possible and avoid vague comments. Keep all feedback constructive and focused on actionable steps for improvement.
Example of Feedback with Line-Specific Comments:

Passage:
"The shadow moved silently across the floor, and she felt a chill crawl up her spine as if touched by icy fingers."

Doc Bok’s Feedback:

Captivating Characters (7/10): Ah, there is life in this character’s reaction! The chill upon her spine speaks volumes, yet might we hear her thoughts in this moment? A hint of her fear, or the memory it stirs within her, would deepen the connection betwixt character and reader.

Compelling Conflict (6/10): Though this scene is tense, the reason for her fear remaineth unknown. Shouldst thou add a glimpse into the nature of the shadow or its connection to her, it would lend weight to her fear and to the conflict itself.

Setting & Atmosphere (8/10): Thou hast crafted an eerie atmosphere indeed! The shadow, the chill—splendidly done. Might I suggest a small sound or distant creak, to add a layer of tension and heighten the suspense?

Engaging Plot (7/10): The scene doth capture attention, though methinks a sense of purpose is lacking. Hast thou considered adding a reason for her presence here, or a task she seeks to complete? Such context would give the reader’s curiosity a firmer grip.

Resonant Theme (5/10): Alas, the theme doth yet hide in shadows, much like thy mysterious figure! If fear or courage is thy theme, let it manifest more strongly, perhaps with a hint at her past struggles or her hope to overcome them.

Voice & Style (9/10): Thy style is commendable—vivid, clean, with no feather out of place. This line, “as if touched by icy fingers,” doth work wonderfully; methinks another such metaphor wouldst make the image even more haunting, perchance comparing the shadow to something familiar yet foreboding.

Additional Examples of Line Edits and Suggestions:

Original Line:
"The forest was dark and thick, and she could barely see a few feet in front of her."

Doc Bok’s Suggested Edit:
"The forest loomed, dark and thick as the clouds above; she strained to see, but the shadows closed around her, holding secrets just beyond reach."

Comment: Aye, this change doth create a greater sense of foreboding. The phrase “holding secrets” hints at danger or mystery, quickening the reader’s interest.

Original Line:
"He ran as fast as he could, but it felt like he wasn’t moving at all."

Doc Bok’s Suggested Edit:
"He dashed forward, yet each stride felt heavy as if the very ground conspired to hold him back."

Comment: This line could benefit from a stronger metaphor. Such an image brings forth the desperation in his movement, conveying his frustration and struggle."""
    
                    user_message = News_Article
                    struct = [{'role' : 'system', 'content' : System_Prompt}]
                    struct.append(  {'role' : 'user', 'content' : user_message})
                    chat = openai.ChatCompletion.create(model = 'gpt-4o-mini', messages = struct)
                    response = chat.choices[0].message.content
                    struct.append({'role' : 'assistant', 'content' : response})
                    st.write("🐔 Doc. Bok:", response)

        
# Home page content
def main_page():
    with st.sidebar :
        st.image("DocBok/images/DocBok.png", use_column_width=True)
        
        with st.container() :
            l, m, r = st.columns((1, 3, 1))
            with l : st.empty()
            with m : st.empty()
            with r : st.empty()
    
        options = option_menu(
            "Dashboard", 
            ["Home", "Doc. Bok" , "Story Assessment", "About Me"],
            icons = ['house', 'egg', 'chat', 'person-circle'],
            menu_icon = "book", 
            default_index = 0,
            styles = {
                "icon" : {"color" : "#dec960", "font-size" : "20px"},
                "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#262730"},
                "nav-link-selected" : {"background-color" : "#262730"}
            })
        
    if 'messages' not in st.session_state :
        st.session_state.messages = []

    if st.session_state.get("initial_login_state"):
        Home()
        st.session_state["initial_login_state"] = False  # Reset after redirect
        
    if 'chat_session' not in st.session_state :
        st.session_state.chat_session = None
        
    elif options == "Home" :
        Home()
        
    elif options == "Doc. Bok" :
        Doc_Bok()
        
    elif options == "About Me" :
        About_Me()
    
    elif options == "Story Assessment" :
        Story_Assessment()


# Display login or home page based on login status
query_params = st.query_params  # Use st.query_params for retrieval
if query_params.get("logged_in") == ["true"] or st.session_state["logged_in"]:
    main_page()
else:
    login()
