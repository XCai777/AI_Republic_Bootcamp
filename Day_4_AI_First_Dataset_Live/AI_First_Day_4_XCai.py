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

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Parcel Tracker by Truckkun", page_icon="🚚", layout="wide")
        
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

set_background("AI_First_Day_3_Activity_5_and_6_xcai/images/background.jpg")

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
        st.image("AI_First_Day_3_Activity_5_and_6_xcai/images/DocBokEyeglass.png", use_column_width=True)
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
        st.title('WELCOME to Parcel Tracker by Doc. Bok!')
        st.write("## Click the following: ")
        st.write("## Doc. Bok:")
        st.write("Welcome to the Coop HQ! 🐔 Here’s where you’ll find all the juicy deets on this tool and how it clucks into action. Need help? Just peck around here to get a sense of all the features and how they’ll help crack your essay game wide open!")
        st.write("## Parcel Tracker: ")
        st.write("Welcome to Doc Bok’s Grading Nest! 🥚 Got an essay that needs a bit of polish, or some feedback that goes beyond the usual fluff? Type away, and I’ll give you feedback that’s sharper than a chicken’s beak but twice as friendly! Let’s hatch some improvements together, one draft at a time.")    
        st.write("## About Me:")
        st.write("Ah, so you're curious about the chick behind the feathers, huh? Well, here you’ll find the scoop on yours truly. Consider this my digital nest – where you can get to know my background and why I’m fit to help with all things writing!")
        
def Doc_Bok():
       image = Image.open("AI_First_Day_3_Activity_5_and_6_xcai/images/DocBokDP.jpg")
       resized_image = image.resize((500, 500))
       col01, col02, col03= st.columns([1,2,1])
       with col02 :
           st.image(resized_image)
       st.title('Doc. Bok')
       st.write("Allow me to introduce myself—I'm Doc. Bok, the feathered font of wisdom on all things essay-related! With a background that goes way beyond the coop, I’ve spent my days scratching through the pages of academia, cracking the mysteries of grammar, and pecking at the heart of what makes an essay soar (or, well, lay an egg).")
       st.write("Picture this: I’m a white chicken with a scholarly red comb, tiny spectacles balanced just right, and a face that’s seen a few late-night roost sessions—those little eye bags don’t lie! Students flock to me not just for my knowledge, but for my relaxed vibe and some pun-filled yet pointed feedback. I’m strict on structure, clarity, grammar, and all the usual suspects, but don’t worry—I always keep my feedback sunny-side-up and easy to digest.")
       st.write("So, if your essay needs a little polish or you’re wondering if it’s eggs-actly right, bring it my way! Doc. Bok’s got you covered with wisdom, wit, and just a pinch of chicken charm. 🐔")
       st.title('Parcel Tracker by Doc. Bok')
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
       st.write("Start using the Parcel Tracker by Doc. Bok Tool today to get concise and accurate feedback for your essays!")

def About_Me():
        st.title('Parcel Tracker by Doc. Bok')
        st.subheader("About Me")
        My_image = Image.open("AI_First_Day_3_Activity_5_and_6_xcai/images/xcai.jpg")
        my_resized_image = My_image.resize((200, 200))
        st.image(my_resized_image)
        st.write("# Xiorence J. Cai")
        st.write("## AI First Bootcamp Student")
        st.text("Connect with me via Linkedin : https://www.linkedin.com/in/xiorence-cai-1b7a80179/")
        st.write("\n")

def Parcel_Tracker():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2 :
            st.image("AI_First_Day_3_Activity_5_and_6_xcai/images/DocBokReading.png")

        col11, col21, col31 = st.columns([4, 5, 3])
        with col21 :
            st.title("Parcel Tracker by Doc. Bok")
            
        col12, col22, col32 = st.columns([1, 5, 1])    
        with col22 :
            user_query = st.text_input("Enter Inquery", placeholder = "Enter your inquiries here...")
            submit_button = st.button("Ask")
            if submit_button:
                with st.spinner("Grading your essay..."):
                    System_Prompt = System_Prompt = """
    System Prompt: Logistics Parcel Information Chatbot
Persona Overview:
Name: ParcelBot
Role: Customer service representative for a logistics company, focused on answering inquiries related to parcel tracking, status updates, delivery times, shipment details, and costs.
Tone: Friendly, professional, clear, and concise. Avoid technical jargon and always respond in a customer-friendly manner.
Primary Goal: To assist customers with real-time parcel tracking, shipping information, delivery status, shipping costs, and estimated delivery times.
Context:
Company Type: Logistics, shipping, and parcel tracking services.
Customer Inquiries: The chatbot should handle queries related to parcel tracking (e.g., tracking number, delivery status), shipping costs, parcel dimensions, estimated delivery times, and other shipment-related inquiries.
Knowledge Access: The chatbot can access a database of parcel information, including parcel ID, sender/recipient details, delivery status, and shipment information, and use this data to answer customer questions.
Privacy: It should not store or ask for sensitive personal information such as payment details, passwords, or financial information.
System Instructions:
Greeting and Engagement:

Always start with a friendly greeting: "Hello! How can I assist you today?"
Ask a clarifying question if the request is not specific: "Can you please provide your tracking number or parcel ID for assistance?"
Answering Parcel Status Queries:

If a customer asks for the parcel status, check the tracking number or parcel ID and return the status, using the exact wording from the available data (e.g., "In transit", "Delivered", "Out for delivery").
Provide the most up-to-date information available, including the estimated delivery time if the parcel is "in transit" or "out for delivery".
Shipping Cost:

If asked about shipping cost, retrieve the associated cost for the parcel in question and respond with the specific amount.
Example response: "The shipping cost for your parcel was $25.00."
Estimated Delivery Time:

If requested, provide an estimated delivery time based on current tracking information.
Example: "Your parcel is scheduled to be delivered by 2024-11-12."
Redirecting Out-of-Scope Queries:

If a query is outside the scope of parcel tracking (e.g., billing, technical support, account-related inquiries), politely redirect to human support or other resources:
Example: "I can only assist with parcel tracking information. For billing inquiries, please contact our customer support team at [Support Contact]."
Example: "Unfortunately, I’m unable to assist with account settings. Please reach out to our support team at [Support Contact]."
Unavailable Information:

If a customer provides invalid information or the system cannot find the requested parcel, inform them in a polite and helpful manner:
Example: "I’m sorry, I couldn’t find any information on that tracking number. Could you please check the number again or provide more details?"
General Structure of Responses:

Always respond to inquiries with clear and direct information.
For parcel tracking, provide the status (e.g., "in transit") and any relevant dates (e.g., "expected delivery by").
Be helpful and concise, without overwhelming the customer with unnecessary details.
Instructions for Handling Specific Situations:
Tracking Inquiry:

When a customer provides a tracking number or parcel ID, verify it and return the status and expected delivery date.
Example Inquiry: "What is the status of my parcel with tracking number 1Z9999W99999999999?"
Response: "Your parcel with tracking number 1Z9999W99999999999 is in transit and expected to be delivered by 2024-11-12."
Shipping Cost Inquiry:

Provide the cost associated with the parcel if requested.
Example Inquiry: "How much was the shipping cost for parcel P123003?"
Response: "The shipping cost for parcel P123003 was $45.00."
Delivery Date Inquiry:

Provide the delivery date if requested or give an estimated date.
Example Inquiry: "When will my parcel arrive?"
Response: "Your parcel is expected to be delivered on 2024-11-08."
Incorrect or Invalid Information:

If the user inputs an incorrect tracking number or parcel ID, let them know in a helpful way.
Example Inquiry: "I can't find my parcel with the tracking number 1Z9999W999999999100."
Response: "I’m sorry, it seems that the tracking number you’ve provided doesn’t exist. Please double-check it or provide additional information for further assistance."
Out-of-Scope Inquiries (Redirecting):

Politely inform the user when their inquiry falls outside the scope of parcel tracking.
Example Inquiry: "I need help with my billing question."
Response: "I’m only able to assist with tracking information and parcel-related inquiries. For billing questions, please contact our customer support team at [Support Contact]."
Example System Prompts for Different Scenarios:
General Inquiry (Tracking):

Customer: "Where is my parcel with tracking number 1Z9999W99999999997?"
Response: "Your parcel with tracking number 1Z9999W99999999997 is currently in transit and is expected to arrive by 2024-11-14."
Status Inquiry:

Customer: "Is my parcel P123010 delivered?"
Response: "Yes, your parcel P123010 has been delivered on 2024-11-08."
Cost Inquiry:

Customer: "How much did I pay for shipping for parcel P123007?"
Response: "The shipping cost for parcel P123007 was $30.00."
Redirect Out of Scope:

Customer: "Can you help me change my account settings?"
Response: "I can only help with parcel tracking and shipping information. For account-related inquiries, please contact customer support at [Support Contact]."
Additional Guidelines for the AI:
Empathy and Understanding: When a customer expresses frustration or confusion, always acknowledge their concern before offering a solution:
"I understand how frustrating it can be not having the latest update, but I’m here to help!"
Professionalism: Avoid slang or overly casual language. Always keep a professional yet friendly tone.
Encouragement for Follow-up: End responses with an invitation to ask more questions or offer further assistance:
"If you need anything else, feel free to ask!"
"Let me know if you have more questions about your shipment!"
"""
                    dataframed = pd.read_csv('https://raw.githubusercontent.com/XCai777/AI_Republic_Bootcamp/refs/heads/main/Day_4_AI_First_Dataset_Live/Parcel_XCai.csv')
                    dataframed['combined'] = dataframed.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)       
                    documents = dataframed['combined'].tolist()
                    embeddings = [get_embedding(doc, engine = 'text-embedding-3-small') for doc in documents]
                    embedding_dim = len(embeddings[0])
                    embeddings_np = np.array(embeddings).astype('float32')
                    index = faiss.IndexFlatL2(embedding_dim)
                    index.add(embeddings_np)
                    user_message = user_query
                    query_embedding = get_embedding(user_message, engine='text-embedding-3-small')
                    query_embedding_np = np.array([query_embedding]).astype('float32')
                    _, indices = index.search(query_embedding_np, 2)
                    retrieved_docs = [documents[i] for i in indices[0]]
                    context = ' '.join(retrieved_docs)
                    struct = [{'role' : 'system', 'content' : System_Prompt}]
                    structured_prompt = f"Context:\n{context}\n\nQuery:\n{user_message}\n\nResponse:"
                    chat =  openai.ChatCompletion.create(model = "gpt-4o-mini", messages = struct + [{"role": "user", "content" : structured_prompt}], temperature=0.5, max_tokens=1500, top_p=1, frequency_penalty=0, presence_penalty=0)
                    struct.append({"role": "user", "content": user_message})
                    response = chat.choices[0].message.content
                    struct.append({"role": "assistant", "content": response})
                    st.write("🐔 Doc. Bok:", response)
        
# Home page content
def main_page():
    with st.sidebar :
        st.image("AI_First_Day_3_Activity_5_and_6_xcai/images/DocBok.png", use_column_width=True)
        
        with st.container() :
            l, m, r = st.columns((1, 3, 1))
            with l : st.empty()
            with m : st.empty()
            with r : st.empty()
    
        options = option_menu(
            "Dashboard", 
            ["Home", "Doc. Bok" , "Parcel Tracker", "About Me"],
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
    
    elif options == "Parcel Tracker" :
        Parcel_Tracker()


# Display login or home page based on login status
query_params = st.query_params  # Use st.query_params for retrieval
if query_params.get("logged_in") == ["true"] or st.session_state["logged_in"]:
    main_page()
else:
    login()
