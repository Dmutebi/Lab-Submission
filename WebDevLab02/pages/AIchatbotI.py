import streamlit as st
from ctext import gettextasparagraphlist
import google.generativeai as genai
#from dotenv import load_dotenv
import os


#load_dotenv()


#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")\
GEMINI_API_KEY = "AIzaSyCRPO4GFrRZ7I5nAiycwKkg9rUFLNNVvV8"
if not GEMINI_API_KEY:
    st.error("❌ Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
    st.stop()

genai.configure(api_key="AIzaSyCRPO4GFrRZ7I5nAiycwKkg9rUFLNNVvV8")


texts = {
    "Analects (论语)": "ctp:analects",
    "Mencius (孟子)": "ctp:mengzi"
}

st.title("🤖 Confucian Translation Chatbot")
st.markdown("Select a classical Chinese text and ask Gemini to translate a section.")


text_choice = st.selectbox("Select a Confucian text:", list(texts.keys()))
urn = texts[text_choice]

try:
    paragraphs = gettextasparagraphlist(urn)
except Exception as e:
    st.error(f"❌ Failed to load text: {e}")
    st.stop()

para_index = st.slider("Choose paragraph number", 1, min(10, len(paragraphs)))
selected_text = paragraphs[para_index - 1]

st.markdown("### Selected Text:")
st.write(selected_text)


direction = st.radio("Translate this paragraph:", ["Chinese to English", "English to Classical Chinese"])


if st.button("Translate with Gemini"):
    if direction == "Chinese to English":
        prompt = f"""Translate the following Classical Chinese paragraph into modern English with a short explanation if needed:\n\n{selected_text}"""
    else:
        prompt = f"""Translate the following modern English into Classical Chinese using the style found in the Analects or Mencius:\n\n{selected_text}"""

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        st.success("✅ Translation:")
        st.write(response.text)
    except Exception as e:
        st.error(f"⚠️ LLM Error: {e}")


