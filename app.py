import streamlit as st
import requests
from latin_cyrillic_symbols import to_cyrillic
from tqdm import tqdm

api_key = st.secrets["API_TOKEN"]
# API URL and headers
API_URL = "https://api-inference.huggingface.co/models/shohabbosdev/text-to-audio"
headers = {"Authorization": f"Bearer {api_key}"}

# Function to handle text-to-speech conversion
def text_to_speech(text, language="uz"):
    try:
        # Preprocess the text
        text = text.replace('\n', ' ')
        text = text if any('\u0400' <= char <= '\u04FF' for char in text) else to_cyrillic(text)
        
        # Send the API request
        payload = {"inputs": text}
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.status_code, text, response.content
        else:
            return response.status_code, text, None
    
    except Exception as e:
        st.error(f"❌ Error in text-to-speech conversion: {e}")
        return None, None, None

# Streamlit app
st.set_page_config(page_title="Text-to-Speech App", page_icon="🔊")

# Sidebar menu
with st.sidebar:
    st.image('image.png', width=200)
    with st.container(border=True):
        lang = st.toggle("🏴󠁧󠁢󠁥󠁮󠁧󠁿 English", value=False, help="🔊 Toggle between English and Uzbek")
        
        menu = ["🏘 Home", "✍️ About"] if lang else ["🏘 Bosh sahifa", "✍️ Dastur haqida"]
        select_menu = st.selectbox("🔽 Select menu", menu)

# Main content
if select_menu == menu[0]:  # Home
    sahifa = st.title("🎁 Text-to-Speech Conversion App") if lang else st.title("🎁 Matndan nutqqa generatsiya qilish dasturi")
    input_text = st.text_area("💬 Enter text", height=300, help="🤲 Please limit the text to 500 words or less.") if lang else st.text_area("💬 Matn kiriting", height=300, help="🤲 Iltimos bu qismda so'zlar soni 500 tadan oshmasin")
    
    # Tugmani disabled yoki enabled qilish uchun shart
    convert_disabled = not input_text.strip()
    
    if st.button("🎧 Convert to Speech", disabled=convert_disabled, type='primary'):
        progress_text = "Jarayon boshlandi. Iltimos ozgina vaqt kuting."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in tqdm(range(100)):
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        status_code, processed_text, audio_content = text_to_speech(input_text, "en" if lang else "uz")
        my_bar.empty()
        
        if status_code == 200:
            st.success("✅ Text converted to speech successfully!")
            with st.expander("🔻 Processed Text 🔻"):
                st.write(processed_text)
            st.audio(audio_content, format='audio/wav', autoplay=True)
        else:
            st.error(f"❌ Error occurred with status code: {status_code}")

else:  # About
    st.image('image.png', caption="TTSUZ")
    st.markdown("""
        ### Generative AI (GenAI)
        - Generative AI (GenAI) is an artificial intelligence system capable of generating text, images, videos, or other forms of data using generative models.
        - It often responds to prompts and has seen unprecedented growth in recent years due to advancements in transformer-based deep neural networks and large language models (LLMs).
        - Examples include chatbots like ChatGPT, image generation systems like Stable Diffusion, and video generation models like Sora.

        ### Applications and Concerns
        - GenAI is being applied in various fields, including software development, healthcare, finance, entertainment, marketing, art, fashion, and product design.
        - However, concerns have been raised about the potential misuse of GenAI for cybercrime, spreading misinformation, or replacing human jobs on a large scale.
    """, unsafe_allow_html=True)
    st.link_button("🧑‍💻  Dasturchi haqida", url='https://t.me/shohabbosdev', type="secondary")
