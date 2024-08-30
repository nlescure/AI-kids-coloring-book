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

# Set page configuration first
st.set_page_config(page_title="Kids' Coloring Image Generator", page_icon="🖍️")

# Translations
translations = {
    'en': {
        'language': 'Language',
        'title': "🎨 Kids' Coloring Image Generator",
        'input_prompt': "Enter a description of the image you want to generate:",
        'generate_button': "Generate Image",
        'download_button': "Download Image",
        'instructions': """
            **Instructions:** 
            1. Type a fun description of what you want to see in the image.
            2. Click 'Generate Image' to create a magical coloring page!
            3. Download and print the image for endless coloring fun!
            
            Let your imagination run wild and happy coloring! 🌈✏️
        """,
        'image_prompt': "You are a teacher for young kids (3 years old). In the style of a coloring book for kids, generate a simple, black and white line drawing for kids to color: {prompt}. Never add texts in the image."
    },
    'fr': {
        'language': 'Langue',
        'title': "🎨 Générateur d'Images à Colorier pour Enfants",
        'input_prompt': "Entrez une description de l'image que vous souhaitez générer :",
        'generate_button': "Générer l'Image",
        'download_button': "Télécharger l'Image",
        'instructions': """
            **Instructions :** 
            1. Tapez une description amusante de ce que vous voulez voir dans l'image.
            2. Cliquez sur 'Générer l'Image' pour créer une page de coloriage magique !
            3. Téléchargez et imprimez l'image pour un plaisir de coloriage sans fin !
            
            Laissez libre cours à votre imagination et bon coloriage ! 🌈✏️
        """,
        'image_prompt': "Vous êtes un enseignant pour jeunes enfants (3 ans). Dans le style d'un livre de coloriage pour enfants, générez un dessin simple en noir et blanc à colorier : {prompt}. N'ajoutez jamais de texte dans l'image."
    }
}

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to right top, #ff9a9e, #fad0c4, #ffecd2);
        color: #333333;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.8);
        color: #333333;
    }
    h1 {
        color: #333333;
        text-align: center;
    }
    .stTextInput label{
        color: #666666;
    }
    .language-selector {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .language-selector .stSelectbox {
        width: 150px;
    }
    .language-selector .stSelectbox > div > div {
        padding: 2px 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Language selector
st.markdown('<div class="language-selector">', unsafe_allow_html=True)
language = st.selectbox(
    '',
    ['fr', 'en'],
    format_func=lambda x: '🇫🇷 Français' if x == 'fr' else '🇬🇧 English',
    key='language_selector',
    index=0  # This sets the default to the first option, which is now 'fr'
)
st.markdown('</div>', unsafe_allow_html=True)

# Use translations
t = translations[language]

# Title
st.title(t['title'])

# Use session state to store the prompt
if 'prompt' not in st.session_state:
    st.session_state.prompt = ''

prompt = st.text_input(t['input_prompt'], value=st.session_state.prompt)

# Update session state when prompt changes
if prompt != st.session_state.prompt:
    st.session_state.prompt = prompt

if st.button(t['generate_button']):
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
                    label=t['download_button'],
                    data=img_byte_arr,
                    file_name="coloring_image.png",
                    mime="image/png"
                )
            else:
                st.error("Failed to generate image. Please try again.")
    else:
        st.warning("Please enter a description first.")

st.markdown(t['instructions'])