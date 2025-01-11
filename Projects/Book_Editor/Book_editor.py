import streamlit as st
import requests
from PIL import Image
import io
import PyPDF2
import os

# Set your API token
API_TOKEN = st.secrets["API_TOKEN"]

def evaluate_book_cover(image_bytes):
    # Convert image to base64 or appropriate format for API
    # This is a placeholder - adjust according to GPT4-mini API requirements
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    prompt = "Evaluate this book cover and provide specific recommendations for improvement."
    
    try:
        response = requests.post(
            "https://api.gpt4mini.com/v1/chat/completions",  # Replace with actual GPT4-mini endpoint
            headers=headers,
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a professional book cover designer and critic."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error in evaluation: {str(e)}"

def generate_cover_suggestion(recommendations):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            "https://api.gpt4mini.com/v1/chat/completions",  # Replace with actual GPT4-mini endpoint
            headers=headers,
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a professional book cover designer."},
                    {"role": "user", "content": f"Based on these recommendations, suggest a detailed description for a new book cover: {recommendations}"}
                ]
            }
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error in generation: {str(e)}"

def analyze_story(text):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Split text into chunks if it's too long
        text_chunk = text[:4000]  # Adjust size based on API limits
        
        response = requests.post(
            "https://api.gpt4mini.com/v1/chat/completions",  # Replace with actual GPT4-mini endpoint
            headers=headers,
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a professional book editor and critic."},
                    {"role": "user", "content": f"Analyze this story and provide a summary, editing suggestions, and recommendations: {text_chunk}"}
                ]
            }
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error in analysis: {str(e)}"

def main():
    st.title("Book Analysis Assistant")
    
    tab1, tab2 = st.tabs(["Cover Evaluation", "Story Analysis"])
    
    with tab1:
        st.header("Book Cover Evaluation")
        uploaded_image = st.file_uploader("Upload book cover image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Book Cover", use_column_width=True)
            
            if st.button("Evaluate Cover"):
                with st.spinner("Evaluating cover..."):
                    # Convert image to bytes for API
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format=image.format)
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    evaluation = evaluate_book_cover(img_byte_arr)
                    st.write("### Evaluation and Recommendations:")
                    st.write(evaluation)
                    
                    if st.button("Generate New Cover Suggestion"):
                        with st.spinner("Generating suggestion..."):
                            suggestion = generate_cover_suggestion(evaluation)
                            st.write("### New Cover Suggestion:")
                            st.write(suggestion)
    
    with tab2:
        st.header("Story Analysis")
        uploaded_file = st.file_uploader("Upload story PDF", type=['pdf'])
        
        if uploaded_file is not None:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            if st.button("Analyze Story"):
                with st.spinner("Analyzing story..."):
                    analysis = analyze_story(text)
                    st.write("### Story Analysis:")
                    st.write(analysis)

if __name__ == "__main__":
    main()