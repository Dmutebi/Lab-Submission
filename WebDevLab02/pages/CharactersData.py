import streamlit as st
from ctext import gettextinfo
import  matplotlib.pyplot as plt
import requests

text_chapters = {
    "Analects (论语)": {
        "学而 (Xue Er)": "ctp:analects/xue-er",
        "为政 (Wei Zheng)": "ctp:analects/wei-zheng",
        "八佾 (Ba Yi)": "ctp:analects/ba-yi"
    },
    "Mencius (孟子)": {
        "梁惠王上 (Liang Hui Wang I)": "ctp:mengzi/liang-hui-wang-i",
        "梁惠王下 (Liang Hui Wang II)": "ctp:mengzi/liang-hui-wang-ii"
    },
    "Great Learning (大学)": {
        "Main Text": "ctp:great-learning"
    },
    "Doctrine of the Mean (中庸)": {
        "Main Text": "ctp:doctrine-of-the-mean"
    },
    "Book of Songs (诗经)": {
        "周南 · 关雎 (Zhou Nan · Guan Ju)": "ctp:shijing/guan-jü",
        "邶风 · 击鼓 (Bei Feng · Ji Gu)": "ctp:shijing/ji-gu"
    },
    "Book of Documents (书经)": {
        "尧典 (Canon of Yao)": "ctp:shujing/yao-dian"
    },
    "Book of Rites (礼记)": {
        "学记 (Record of Education)": "ctp:liji/xue-ji"
    },
    "I Ching (易经)": {
        "乾 (Qian - Creative)": "ctp:yijing/qian",
        "坤 (Kun - Receptive)": "ctp:yijing/kun"
    },
    "Spring and Autumn Annals (春秋)": {
        "隐公元年 (Yin Year 1)": "ctp:chunqiu/yin-gong-yuan-nian"
    }
}

# Streamlit UI
st.title("📖 Confucian Text Explorer")
st.markdown("Explore classical Chinese texts categorized by Confucian tradition.")

category = st.selectbox("Choose a category:", ["Four Books", "Five Classics"])

if category == "Four Books":
    available_texts = [t for t in text_chapters if t in [
        "Analects (论语)", "Mencius (孟子)", "Great Learning (大学)", "Doctrine of the Mean (中庸)"
    ]]
else:
    available_texts = [t for t in text_chapters if t not in [
        "Analects (论语)", "Mencius (孟子)", "Great Learning (大学)", "Doctrine of the Mean (中庸)"
    ]]

selected_text = st.selectbox("Choose a text:", available_texts)

if selected_text:
    chapter_options = list(text_chapters[selected_text].keys())
    selected_chapter = st.selectbox("Choose a chapter:", chapter_options)

    if selected_chapter:
        urn = text_chapters[selected_text][selected_chapter]

        try:
            response = requests.get(f"https://api.ctext.org/gettext?urn={urn}")
            r = response.json()

            # Flatten nested paragraph structure
            flat_paragraphs = []
            for section in r.get('fulltext', []):
                if isinstance(section, list):
                    flat_paragraphs.extend([p for p in section if isinstance(p, str)])
                elif isinstance(section, str):
                    flat_paragraphs.append(section)

            if flat_paragraphs:
                st.success(f"Retrieved {len(flat_paragraphs)} paragraphs from {selected_chapter}.")

                para_lengths = [len(p) for p in flat_paragraphs]
                fig, ax = plt.subplots()
                ax.bar(range(len(para_lengths)), para_lengths)
                ax.set_title(f"Paragraph Lengths in {selected_chapter}")
                ax.set_xlabel("Paragraph #")
                ax.set_ylabel("Character Count")
                st.pyplot(fig)

                with st.expander("📜 Show first 5 paragraphs"):
                    for i, para in enumerate(flat_paragraphs[:5]):
                        st.markdown(f"**Paragraph {i+1}:** {para}")
            else:
                st.warning("No paragraph content returned.")

        except Exception as e:
            st.error(f"⚠️ Failed to retrieve text: {e}")

