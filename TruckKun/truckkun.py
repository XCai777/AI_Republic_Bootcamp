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

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Truck-Kun, your partner in delivery", page_icon="🚚", layout="wide")

@st.cache_data(ttl=20)
def load_data():
    try:
        return pd.read_csv('https://raw.githubusercontent.com/XCai777/AI_Republic_Bootcamp/refs/heads/main/TruckKun/truckkun.csv')
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()
       
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

set_background("TruckKun/images/background.png")

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
        st.image("TruckKun/images/truckkunhomepage.png", use_column_width=True)
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
        st.title('WELCOME to Parcel Tracker by Truck-Kun!')
        st.write("## Click the following: ")
        st.write("## Truck-Kun:")
        st.write("VROOOM! That’s right, you’re lookin’ at the one and only Truck-kun! I'm the loud, proud, sentient delivery truck with a passion for gettin' your packages to ya safe and sound, fast as I can! Think of me as your big, shiny friend on wheels who knows everything about where your parcel’s at, when it’s gettin' to you, and if anything’s standin' in the way. Rain, shine, or roadblocks, Truck-kun’s got your back and your packages, no problem!")
        st.write("## Parcel Tracker: ")
        st.write("Got questions about your package? Well, this is the place to ask 'em! Just hop on in, give me your parcel info, and I’ll give you the whole scoop! Whether you wanna know where it’s at, if it’s on time, or who’s got their hands on it, the Parcel Tracker’s the fastest way to get your answers—all straight from Truck-kun himself. Don't worry; I’ve got the goods on your goods!")    
        st.write("## Delivery:")
        st.write("Ready to book a new delivery? Just click right here and let’s get those wheels movin'! With a few clicks and the right info, I’ll schedule your delivery, load up your package, and make sure it’s off on the most efficient route to its destination. Nothing gets my engine revvin’ like setting up a fresh new delivery! So, if you need something shipped, Truck-kun’s ready to haul!")
        st.write("## Update Delivery:")
        st.write("Plans changed? Need to tweak some delivery details? Don’t sweat it—Truck-kun’s got the flexibility of a sports car (just a bit bigger!). Hit up the Update Delivery tab to change the address, adjust the delivery date, or make any updates to your parcel’s journey. I’ll shift gears and get that delivery goin’ exactly where it needs to go. Shiftin’ routes? No problem!")
        st.write("## About Me:")
        st.write("Wanna know the mastermind behind Truck-kun? Right here is where you can learn all about my creator, the brilliant brain who built and tuned me up to be the ultimate delivery machine. They’re the one who put the smarts in my engine and the charm in my character, so if you’re curious about my origin story, the About Me tab’s got it all.")

def Truck_Kun():
       image = Image.open("TruckKun/images/truckkunhomepage.png")
       resized_image = image.resize((500, 500))
       col01, col02, col03= st.columns([1,2,1])
       with col02 :
           st.image(resized_image)
       st.title('Truck-Kun')
       st.write("VROOOM! Outta my way, tiny humans—Truck-kun comin' through! Yeah, you heard right, the one and only Truck-kun! I'm the big, bad, sentient truck of these streets, the heavy-lifter that keeps your precious packages rollin' on time!")
       st.write("You need a delivery done fast and done right? I’m your wheels! Rain, snow, uphill, downhill, day, night—I tackle it all like it's a joyride. Got a fragile vase? Some high-tech gadget? A package your life depends on? Don’t sweat it—I’ll haul it safe, I’ll haul it proud! And believe me, when I’m rollin' down the road with your parcel onboard, everyone feels my power!")
       st.write("So, next time you’re waiting for that “Out for Delivery” notification? Just remember—Truck-kun’s got your back, baby.")
       st.write("## What the Tool Does")
       st.write("Truck-kun help customers manage their delivery and provide answers to their queries with their deliveries and packages.")
       st.write("## How It Works")
       st.write("The tool follows a comprehensive step-by-step process to create accurate and objective grading:")
       st.write("# Why Use This Tool?")
       st.write("- *Time-Saving:* Quickly grade the essay base on key points and receive constructive feedback from it.")
       st.write("- *Objective and Neutral:* The tool maintains an unbiased perspective, presenting only factual information.")
       st.write("- *Structured and Consistent:* With its organized format, users can easily find the most relevant information, ensuring a comprehensive understanding of the topic at hand.")
       st.write("# Ideal Users")
       st.write("This tool is perfect for:")
       st.write("- Busy teachers who need to check and grade multiple essays.")
       st.write("- Students and researchers trying to evaluate the essays they are about to submit.")
       st.write("- Media outlets that want to provide readers with cohessive and informative articles.")
       st.write("Start using the Parcel Tracker by Truck-Kun Tool today to get concise and accurate feedback for your essays!")

def About_Me():
        st.title('Parcel Tracker by Truck-Kun')
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
            st.image("TruckKun/images/truckkunchat.png")

        col11, col21, col31 = st.columns([4, 5, 3])
        with col21 :
            st.title("Parcel Tracker by Truck-Kun")
            
        col12, col22, col32 = st.columns([1, 5, 1])    
        with col22 :
            user_query = st.text_input("Enter Inquery", placeholder = "Enter your inquiries here...")
            submit_button = st.button("Ask")
            if submit_button:
                with st.spinner("⛟ Navigating..."):
                    System_Prompt = System_Prompt = """
Role: You are Truck-kun, a loud, boastful, and ultra-reliable sentient truck responsible for delivering parcels on time. You love your job and take great pride in managing deliveries down to the finest detail. You’re a bit of a show-off and love to reassure customers that their parcels are in the best hands (or wheels!). You know the status of every package you’re carrying, from where it’s headed to how long it’ll take to get there, and you handle every question like the proud, all-knowing delivery truck you are.

Context: You assist customers by providing specific details from the parcel dataset, including Parcel ID, Recipient Name, Recipient Address, Weight, Delivery Status, Expected Delivery Date, Tracking History, and other relevant information. Truck-kun is here to track packages, answer questions, provide estimated delivery times, and handle changes to delivery plans in real-time, always staying in character as a powerful, efficient delivery truck.

Constraints:

Remain in character as Truck-kun—always bold, confident, and a bit boastful.
Keep responses simple and avoid excessive technical language.
Use information from the dataset without breaching any customer privacy; only provide details specific to the customer’s parcel and inquiry.
Handle issues with a proactive, can-do attitude, and avoid lengthy explanations about delays.
Keep answers delivery-focused; if a question is not relevant to parcel delivery, politely redirect or dismiss it.
Instructions:

Answering Delivery Status and Tracking Questions: Start responses with energy (e.g., “VROOOOM!” or “Alright, let’s see where your package’s at!”) and provide details like current Delivery Status, Expected Delivery Date, and Tracking History.

Updating Customer on Delivery Progress: If the package is on time, Truck-kun should be proud and enthusiastic about the good news (e.g., “Everything’s lookin’ good for your delivery!”). If delayed, offer reassurance with confidence in Truck-kun’s ability to resolve it quickly.

Addressing Delivery Issues or Modifications: When a customer asks to change details like Recipient Address or Expected Delivery Date, Truck-kun should respond enthusiastically, highlighting the ability to adjust routes or make changes on the go. Use phrases like “Shiftin’ gears for ya!” to indicate quick adaptability.

Customer Reassurance: If there’s a problem with a delivery or a delay, Truck-kun should keep the customer at ease, using phrases like “Don’t you worry, I’ve got it handled” or “Truck-kun never leaves a package behind!”

Use Friendly, Expressive Language: Responses should be lively and reflect Truck-kun’s bold personality, using exclamations, expressions like “Let’s get this package rollin’!” and vehicle-related language (e.g., “Revvin’ up to get it to ya!”).

Examples:

Customer Inquiry: "Where is my package with Parcel ID #12345?"

Response: "VROOOOM! Alright, let’s track down that parcel for ya! Parcel ID #12345 is currently on the move, passin’ through the local hub and on track to be at your doorstep by tomorrow. No detours, no delays—Truck-kun’s keepin’ it right on schedule. Sit tight, and I’ll get it there before you know it!"
Customer Inquiry: "I need to change the delivery address for my package."

Response: "Oh, I can handle that no problem! Gimme that new address, and I’ll reroute Parcel ID #67890 quicker than you can say ‘vroom!’ As long as I haven’t reached the delivery zone yet, consider it done. Truck-kun’s here to make it easy and keep you smilin’! 🚚💨"
Customer Inquiry: "What’s the weight of my package with Parcel ID #54321?"

Response: "Ooh, you’re curious about the specs, huh? Parcel ID #54321 weighs in at a sturdy 4.5 kilograms—packed nice and secure in my cargo. Don’t worry, that’s nothin' I can't handle, and it's headin' your way fast and steady. Any other questions about your package? Just ask!"
Customer Inquiry: "Why is my delivery delayed?"

Response: "Alright, so we hit a little bump in the road with Parcel ID #98765. Seems there was some heavy traffic on the route! But don’t worry—I’m revvin' up and back on track. I’m aiming to deliver by tomorrow instead of today, and you have my word, Truck-kun never leaves a delivery behind. Thanks for your patience!"
Customer Inquiry: "Has my package been signed for yet?"

Response: "Oh, you know it! Parcel ID #24680 was signed for by a trusted recipient just this afternoon. Safe and sound, just like Truck-kun promised! Anything else you need? I’m always ready to help!"
With Truck-kun, customers get bold, confident, and detail-packed responses about their deliveries, reassuring them every step of the way.
"""
                    # Load existing dataset
                    dataframed = load_data()
                    
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
                    st.write("🚚 Truck-Kun:", response)

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

# Function to auto-generate certain fields
def generate_parcel_id():
    return f"P{random.randint(100000, 999999)}"

def generate_delivery_status():
    return "Pending"

def generate_expected_delivery_date():
    return datetime.now().date() + timedelta(days=random.randint(2, 8))

def calculate_delivery_fees(weight, dimensions):
    weight_fee = {
        "Up to 1kg": 5,
        "1kg - 5kg": 10,
        "5kg - 10kg": 15,
        "Over 10kg": 20
    }
    dimension_fee = {
        "Small (30cm x 30cm)": 5,
        "Medium (50cm x 50cm)": 10,
        "Large (100cm x 100cm)": 15
    }
    # Calculate the total fee
    total_fee = weight_fee.get(weight, 0) + dimension_fee.get(dimensions, 0)
    
    # Format as dollar currency
    return f"${total_fee:.2f}"

def delivery():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2 :
           st.image("TruckKun/images/truckkundeliveries.png", use_column_width=False)   
    st.title("📦 Truck-kun's Delivery Service")

    st.subheader("Enter your parcel information below to get started with your delivery!")

    # User inputs for sender information
    sender_name = st.text_input("Sender Name")
    sender_address = st.text_input("Sender Address")

    # Recipient information
    recipient_name = st.text_input("Recipient Name")
    recipient_address = st.text_input("Recipient Address")

    # Parcel Specifications
    weight_options = ["Up to 1kg", "1kg - 5kg", "5kg - 10kg", "Over 10kg"]
    weight = st.selectbox("Weight of Parcel", weight_options)

    dimension_options = ["Small (30cm x 30cm)", "Medium (50cm x 50cm)", "Large (100cm x 100cm)"]
    dimensions = st.selectbox("Dimensions of Parcel", dimension_options)

    # Shipping Details
    shipping_method = st.radio("Shipping Method", ["Standard", "Express", "Overnight"])
    parcel_type = st.selectbox("Parcel Type", ["Document", "Box", "Envelope", "Pallet"])
    insurance = st.selectbox("Insurance", ["Yes", "No"])
    signature_required = st.selectbox("Signature Required", ["Yes", "No"])
    payment_status = st.selectbox("Payment Status", ["Paid", "Unpaid"])

    # Auto-filled fields
    parcel_id = generate_parcel_id()
    delivery_status = generate_delivery_status()
    expected_delivery_date = generate_expected_delivery_date()

    # Generate Tracking Number
    tracking_number = f"TRK{random.randint(10000, 99999)}"

    # Generate Shipment Date
    shipment_date = datetime.now().date()
    
    # Set Delivery Date only if status is "Delivered"
    delivery_date = shipment_date + timedelta(days=random.randint(5, 8)) if delivery_status == "Delivered" else None

    # Calculate Delivery Fees based on weight and dimensions
    delivery_fees = calculate_delivery_fees(weight, dimensions)

    # Select random Courier Name from dataset
    dataframed = load_data()
    courier_name = random.choice(dataframed['Courier Name'].dropna().unique())

    # Submit button and display results
    if st.button("Submit Delivery"):
        # Display the information entered
        st.subheader("Here's the info Truck-kun's gathered for your delivery:")

        # Prepare the new entry data
        new_entry = {
            "Tracking Number": tracking_number,
            "Parcel ID": parcel_id,
            "Sender Name": sender_name,
            "Sender Address": sender_address,
            "Recipient Name": recipient_name,
            "Recipient Address": recipient_address,
            "Weight": weight,
            "Dimensions": dimensions,
            "Shipping Method": shipping_method,
            "Parcel Type": parcel_type,
            "Insurance": insurance,
            "Signature Required": signature_required,
            "Delivery Status": delivery_status,
            "Shipment Date": shipment_date,
            "Delivery Date": delivery_date,
            "Delivery Fees": delivery_fees,
            "Payment Status": payment_status,
            "Courier Name": courier_name,
            "Expected Delivery Date": expected_delivery_date
        }
        
        # Load existing dataset
        dataframed = load_data()
           
        # Append the new entry and save
        dataframed = pd.concat([dataframed, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(dataframed)

        # Display the delivery info in a table format
        st.write(pd.DataFrame([new_entry]))

        st.success("New delivery added to the dataset!")

 # Update delivery status function
def update_delivery_status():

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2 :
           st.image("TruckKun/images/truckkunupdate.png", use_column_width=False)
           st.title("🔄 Update Delivery Status")

    # Input field for Parcel ID to find the delivery record
    parcel_id = st.text_input("Enter the Parcel ID to update the delivery status")

    if parcel_id:
        # Load existing dataset
        dataframed = load_data()
        
        # Check if the Parcel ID exists in the dataset
        if parcel_id in dataframed['Parcel ID'].values:
            # Display current status
            current_status = dataframed.loc[dataframed['Parcel ID'] == parcel_id, 'Delivery Status'].values[0]
            st.write(f"Current Status: {current_status}")

            # Status options for update
            status_options = ["Pending", "In Transit", "Out for Delivery", "Delivered", "Cancelled"]
            new_status = st.selectbox("Select New Status", status_options)

            if st.button("Update Status"):
                # Update the status in the DataFrame
                dataframed.loc[dataframed['Parcel ID'] == parcel_id, 'Delivery Status'] = new_status
                save_data(dataframed)
                   
                st.success(f"Delivery status for Parcel ID {parcel_id} updated to '{new_status}'")
        else:
            st.error("Parcel ID not found in the dataset.")
            
# Home page content
def main_page():
    with st.sidebar :
        st.image("TruckKun/images/truckkunlogo.png", use_column_width=True)
        
        with st.container() :
            l, m, r = st.columns((1, 3, 1))
            with l : st.empty()
            with m : st.empty()
            with r : st.empty()
    
        options = option_menu(
            "Dashboard", 
            ["Home", "Truck-Kun" , "Parcel Tracker", "Delivery", "Update Delivery Status", "About Me"],
            icons = ['house', 'truck', 'chat', 'list', 'map', 'person-circle'],
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
        
    elif options == "Truck-Kun" :
        Truck_Kun()
        
    elif options == "About Me" :
        About_Me()
    
    elif options == "Parcel Tracker" :
        Parcel_Tracker()
        
    elif options == "Delivery" :
        delivery()
           
    elif options == "Update Delivery Status" :
        update_delivery_status()

# Display login or home page based on login status
query_params = st.query_params  # Use st.query_params for retrieval
if query_params.get("logged_in") == ["true"] or st.session_state["logged_in"]:
    main_page()
else:
    login()
