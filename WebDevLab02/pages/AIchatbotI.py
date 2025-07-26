import streamlit as st
from ctext import gettextasparagraphlist
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Available classical texts
texts = {
    "Analects (论语)": "ctp:analects",
    "Mencius (孟子)": "ctp:mengzi"
}

st.title("🤖 Confucian Translation Chatbot")
st.markdown("Select a classical Chinese text and ask Gemini to translate a section.")

# User text selection
text_choice = st.selectbox("Select a Confucian text:", list(texts.keys()))
urn = texts[text_choice]

# Load selected text
try:
    paragraphs = gettextasparagraphlist(urn)
except Exception as e:
    st.error(f"❌ Failed to load text: {e}")
    st.stop()

# Paragraph selection
para_index = st.slider("Choose paragraph number", 1, min(10, len(paragraphs)))
selected_text = paragraphs[para_index - 1]

st.markdown("### Selected Text:")
st.write(selected_text)

# Translation direction
direction = st.radio("Translate this paragraph:", ["Chinese to English", "English to Classical Chinese"])

# Translation button
if st.button("Translate with Gemini"):
    if direction == "Chinese to English":
        prompt = f"""Translate the following Classical Chinese paragraph into modern English with a short explanation if needed:\n\n{selected_text}"""
    else:
        prompt = f"""Translate the following modern English into Classical Chinese using the style found in the Analects or Mencius:\n\n{selected_text}"""

    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")

        # Retry logic for quota-related errors
        max_retries = 3
        delay_seconds = 30

        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                st.success("✅ Translation:")
                st.write(response.text)
                break
            except Exception as e:
                if "429" in str(e):
                    st.warning(f"⚠️ Quota exceeded. Retrying in {delay_seconds} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay_seconds)
                else:
                    raise e
        else:
            st.error("❌ Failed after multiple attempts. Please try again later or check your quota.")
    except Exception as final_error:
        st.error(f"❌ Error: {final_error}")



