import streamlit as st
import matplotlib.pyplot as plt
import requests

four_books = {
    "Analects (论语)": "ctp:analects",
    "Mencius (孟子)": "ctp:mengzi",
    "Great Learning (大学)": "ctp:great‑learning",
    "Doctrine of the Mean (中庸)": "ctp:doctrine‑of‑the‑mean"
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
texts = four_books if category == "Four Books" else five_classics
selected_text = st.selectbox("Choose a text:", list(texts.keys()))

if selected_text:
    urn_base = texts[selected_text]
    # Let user optionally pick chapter/subsection:
    chapter_suffix = st.text_input("Optional: enter chapter URN suffix (e.g., xue‑er):", value="")
    urn = urn_base + ("/" + chapter_suffix if chapter_suffix else "")
    
    try:
        url = f"https://api.ctext.org/gettext?urn={urn}"
        r = requests.get(url).json()
        st.write("DEBUG — raw response:", r)

        if 'error' in r:
            st.error(f"API error: {r['error'].get('description','Unknown error')}")
        elif 'fulltext' not in r:
            st.warning("⚠ No fulltext returned — perhaps needs authentication or incorrect URN.")
        else:
            flat_paragraphs = []
            for section in r['fulltext']:
                if isinstance(section, list):
                    for para in section:
                        if isinstance(para, str):
                            flat_paragraphs.append(para)
                elif isinstance(section, str):
                    flat_paragraphs.append(section)

            st.success(f"Retrieved {len(flat_paragraphs)} paragraphs from {selected_text} ({urn}).")

            para_lengths = [len(p) for p in flat_paragraphs]
            fig, ax = plt.subplots()
            ax.bar(range(len(para_lengths)), para_lengths)
            ax.set_title(f"Paragraph Lengths in {selected_text}")
            ax.set_xlabel("Paragraph #")
            ax.set_ylabel("Character Count")
            st.pyplot(fig)

            with st.expander("📜 Show first 5 paragraphs"):
                for i, para in enumerate(flat_paragraphs[:5]):
                    st.markdown(f"**Paragraph {i+1}:** {para}")

    except Exception as e:
        st.error(f"⚠️ Failed to retrieve text: {e}")
