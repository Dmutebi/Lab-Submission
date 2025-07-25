import streamlit as st
from ctext import setlanguage, searchtexts, gettextasparagraphlist
import matplotlib.pyplot as plt
import requests

setlanguage("en")

st.title("Classical Chinese Text Explorer")

keyword = st.text_input("Enter Chinese keyword to search:")

if keyword:
    results = searchtexts(keyword)
    st.write(results)
    if results:
        
        
        for r in results:
        #options = {f"{r['title']} ({r['urn']})": r['urn'] for r in results}
            options = {}
            r = requests.get(" https://api.ctext.org/gettext?urn=ctp:analects/xue-er")
            r = r.json()
            print(r['fulltext'])
        urn = st.selectbox("Select a text:", list(options.keys()))
        if urn:
                paras = gettextasparagraphlist(options[urn])
                st.write(f"**{len(paras)}** paragraphs loaded.")
                lengths = [len(p) for p in paras]
                fig, ax = plt.subplots()
                ax.bar(range(len(lengths)), lengths)
                ax.set_xlabel("Paragraph #")
                ax.set_ylabel("Character count")
                st.pyplot(fig)
                st.text_area("Text content:", "\n\n".join(paras), height=300)
    else:
        st.write("No results found.")

