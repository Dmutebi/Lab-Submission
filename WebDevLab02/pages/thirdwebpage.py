import streamlit as st
from ctext import gettextinfo
import  matplotlib.pyplot as plt
import requests

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


st.title("📖 Confucian Text Explorer")
st.markdown("Explore classical Chinese texts categorized by Confucian tradition.")

category = st.selectbox("Choose a category:", ["Four Books", "Five Classics"])

if category == "Four Books":
    texts = four_books
else:
    texts = five_classics

selected_text = st.selectbox("Choose a text:", list(texts.keys()))

if selected_text:
  # urn = texts[selected_text]
    try:
        #paragraphs = gettextinfo(urn)
        

        r = requests.get(" https://api.ctext.org/gettext?urn=ctp:analects/xue-er")
        r = r.json()
        print(r['fulltext'])
        st.success(f"Retrieved {len(r['fulltext'])} requests from {selected_text}.")
        para_lengths = [len(rs) for rs in r['fulltext']]
        fig, ax = plt.subplots()
        ax.bar(range(len(para_lengths)), para_lengths)
        ax.set_title(f"Paragraph Lengths in {selected_text}")
        ax.set_xlabel("Paragraph #")
        ax.set_ylabel("Character Count")
        st.pyplot(fig)

    
        with st.expander("📜 Show first 5 paragraphs"):
            for i, para in enumerate(r['fulltext'][:5]):
                st.markdown(f"**Paragraph {i+1}:** {para}")

    except Exception as e:
        st.error(f"⚠️ Failed to retrieve text: {e}")
