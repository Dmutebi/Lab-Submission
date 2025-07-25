import streamlit as st
from ctext import setlanguage, searchtexts, gettextasparagraphlist
import plotly.express as px
import requests


setlanguage("en")


st.title("📚 Classical Chinese Text Explorer")


keyword = st.text_input("Enter a Chinese keyword to search:")

if keyword:
    
    results = searchtexts(keyword)
    
    if results:
        
        options = {}
        for r in results:
            if isinstance(r, dict) and 'title' in r and 'urn' in r:
                label = f"{r['title']} ({r['urn']})"
                options[label] = r['urn']

       
        if options:
            selected_label = st.selectbox("Select a text:", list(options.keys()))

            if selected_label:
                urn = options[selected_label]
                paras = gettextasparagraphlist(urn)

                st.write(f"✅ **{len(paras)} paragraphs** loaded from: `{urn}`")

              
                lengths = [len(p) for p in paras]
                fig = px.bar(
                    x=list(range(1, len(lengths) + 1)),
                    y=lengths,
                    labels={'x': 'Paragraph #', 'y': 'Character Count'},
                    title='Paragraph Length Distribution'
                )
                st.plotly_chart(fig)

               
                st.text_area("📜 Full Text", "\n\n".join(paras), height=300)
        else:
            st.warning("⚠ No valid text options found in API results.")
    else:
        st.warning("⚠ No results found.")

