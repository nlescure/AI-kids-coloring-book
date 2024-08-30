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
        'image_prompt': "You are a teacher for young kids (3 years old). In the style of a coloring book for kids, generate a simple, black and white line drawing for kids to color: {prompt}. Never add texts in the image.",
        'input_placeholder': "e.g., a flying unicorn in front of a big and old castle"
    },
    'fr': {
        'language': 'Langue',
        'title': "🎨 Générateur d'images à colorier pour enfants",
        'input_prompt': "Entrez une description de l'image que vous souhaitez générer :",
        'generate_button': "Générer l'Image",
        'download_button': "Télécharger l'Image",
        'instructions': """
            **Instructions :** 
            1. Tapez une description amusante de ce que vous voulez voir dans l'image.
            2. Cliquez sur 'Générer l'image' pour créer une page de coloriage magique !
            3. Téléchargez et imprimez l'image pour un plaisir de coloriage sans fin !
            
            Laissez libre cours à votre imagination et bon coloriage ! 🌈✏️
        """,
        'image_prompt': "Tu es un enseignant pour jeunes enfants (3 ans). Dans le style d'un livre de coloriage pour enfants, génére un dessin simple en noir et blanc à colorier : {prompt}. N'ajoute jamais de texte dans l'image.",
        'input_placeholder': "ex : une licorne volante devant un grand et vieux château"
    }
}

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to right top, #ff9a9e, #fad0c4, #ffecd2);
        color: #333333;
    }
    .stButton, .stDownloadButton {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }
    .stButton>button, .stDownloadButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        color: #cccccc;
    }
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.8);
        color: #333333;
    }
    .stTextInput>div>div>input::placeholder {
        color: #999999;
        opacity: 1;
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
        width: 180px;
    }
    .language-selector .stSelectbox > div > div {
        padding: 2px 10px;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .spinner {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 4px solid #333;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
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

prompt = st.text_input(
    t['input_prompt'],
    value=st.session_state.get('prompt', ''),
    placeholder=t['input_placeholder']
)

# Update session state when prompt changes
if prompt != st.session_state.prompt:
    st.session_state.prompt = prompt

def custom_spinner():
    spinner_html = """
        <div class="spinner"></div>
        <p style="text-align: center;">Generating image...</p>
    """
    return st.markdown(spinner_html, unsafe_allow_html=True)

if st.button(t['generate_button']):
    if prompt:
        spinner = custom_spinner()
        image = generate_image(prompt)
        spinner.empty()  # Remove the spinner
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
                mime="image/png",
            )
        else:
            st.error("Failed to generate image. Please try again.")
    else:
        st.warning("Please enter a description first.")

st.markdown(t['instructions'])