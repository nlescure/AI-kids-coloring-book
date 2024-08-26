import streamlit as st
from PIL import Image
import requests
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_image(prompt):
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    api_url = "https://api.openai.com/v1/images/generations"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "prompt": f"You are a teacher for young kids (3 years old). In the style of a coloring book for kids, generate a simple, black and white line drawing for kids to color: {prompt}. Never add texts in the image.",
        "n": 1,
        "model": "dall-e-3",
        "size": "1024x1024",
        "response_format": "url"
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response_data = response.json()
        
        if 'data' in response_data and response_data['data']:
            image_url = response_data['data'][0]['url']
            return Image.open(io.BytesIO(requests.get(image_url).content))
        else:
            st.error("Unexpected response format from the API.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while calling the API: {str(e)}")
        return None

st.title("Kids' Coloring Image Generator")

# Use session state to store the prompt
if 'prompt' not in st.session_state:
    st.session_state.prompt = ''

prompt = st.text_input("Enter a description of the image you want to generate:", value=st.session_state.prompt)

# Update session state when prompt changes
if prompt != st.session_state.prompt:
    st.session_state.prompt = prompt

if st.button("Generate Image"):
    if prompt:
        with st.spinner("Generating image..."):
            image = generate_image(prompt)
            if image:
                st.image(image, caption="Generated coloring image", use_column_width=True)
                
                # Convert the image to bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # Create a download button
                st.download_button(
                    label="Download Image",
                    data=img_byte_arr,
                    file_name="coloring_image.png",
                    mime="image/png"
                )
            else:
                st.error("Failed to generate image. Please try again.")
    else:
        st.warning("Please enter a description first.")

st.markdown("**Instructions:** Type a description of what you want to see in the image, then click 'Generate Image'. The AI will create a simple, black and white line drawing perfect for coloring!")