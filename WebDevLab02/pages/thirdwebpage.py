import streamlit as st
from ctext import gettextinfo
import matplotlib.pyplot as plt
import requests

# Define text collections
four_books = {
    "Analects (论语)": "ctp:analects",
    "Mencius (孟子)": "ctp:mengzi",
    "Great Learning (大学)": "ctp:great-learning",
    "Doctrine of the Mean (中庸)": "ctp:doctrine-of-the-mean"
}

five_classics = {
    "Book of Songs (诗经)": "ctp:shijing",
    "Book of Documents (书经)": "ctp:shujing",
    "Book of Rites (礼记)": "ctp:liji",
    "I Ching (易经)": "ctp:yijing",
    "Spring and Autumn Annals (春秋)": "ctp:chunqiu"
}

# Streamlit UI
st.title("📖 Confucian Text Explorer")
st.markdown("Explore classical Chinese texts categorized by Confucian tradition.")

category = st.selectbox("Choose a category:", ["Four Books", "Five Classics"])

texts = four_books if category == "Four Books" else five_classics
selected_text = st.selectbox("Choose a text:", list(texts.keys()))

if selected_text:
    urn = texts[selected_text]
    try:
        # Example uses Analects: you can dynamically modify the chapter/subsection if needed
        response = requests.get(f"https://api.ctext.org/gettext?urn={urn}/xue-er")
        r = response.json()

        # Flatten nested fulltext structure
        flat_paragraphs = []
        for section in r['fulltext']:
            if isinstance(section, list):
                for para in section:
                    if isinstance(para, str):
                        flat_paragraphs.append(para)
            elif isinstance(section, str):
                flat_paragraphs.append(section)

        st.success(f"Retrieved {len(flat_paragraphs)} paragraphs from {selected_text}.")

        # Plot paragraph lengths
        para_lengths = [len(p) for p in flat_paragraphs]
        fig, ax = plt.subplots()
        ax.bar(range(len(para_lengths)), para_lengths)
        ax.set_title(f"Paragraph Lengths in {selected_text}")
        ax.set_xlabel("Paragraph #")
        ax.set_ylabel("Character Count")
        st.pyplot(fig)

        # Display first 5 paragraphs
        with st.expander("📜 Show first 5 paragraphs"):
            for i, para in enumerate(flat_paragraphs[:5]):
                st.markdown(f"**Paragraph {i+1}:** {para}")

    except Exception as e:
        st.error(f"⚠️ Failed to retrieve text: {e}")


