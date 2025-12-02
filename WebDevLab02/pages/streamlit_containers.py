import streamlit as st
from ctext import setlanguage, searchtexts, gettextasparagraphlist
import plotly.express as px
import time 
import requests 
import json 
import google.generativeai as genai 


setlanguage("en")

st.title("📚 Classical Chinese Text Explorer")
keyword = st.text_input("🔍 Enter a Chinese keyword to search:", value="") # Added default value for clarity


if not keyword or keyword.strip() == "":
    st.info("💡 Please enter a Chinese keyword above (e.g., '道', '仁', '禮') to begin your search.")
    st.stop()



try:
    results = searchtexts(keyword)

    
    with st.expander("🔍 Show Raw Search Results (for debugging)"):
        st.write("Results returned by ctext.org:")
        st.json(results)

    if isinstance(results, list) and results:
        with st.container():
            st.markdown("### 📄 Matching Classical Texts")
            options = {}
            
            # Count valid/invalid results for detailed feedback
            total_results = len(results)
            valid_count = 0

            for r in results:
                # Ensure the result is a dictionary and contains the required keys 'title' and 'urn'
                if isinstance(r, dict) and 'title' in r and 'urn' in r:
                    label = f"{r['title']} ({r['urn']})"
                    options[label] = r['urn']
                    valid_count += 1

            if options:
                selected_label = st.selectbox("Select a text to view:", list(options.keys()))

                if selected_label:
                    urn = options[selected_label]

                    try:
                        paras = gettextasparagraphlist(urn)
                    except Exception as e:
                        st.error(f"❌ Error fetching paragraphs: {e}")
                        paras = []

                    if paras:
                        st.success(f"✅ Loaded **{len(paras)} paragraphs** from `{urn}`")

                        col1, col2 = st.columns([1, 1])

                        with col1:
                            st.markdown("#### 📊 Paragraph Length Distribution")
                            lengths = [len(p) for p in paras]
                            fig = px.bar(
                                x=list(range(1, len(lengths) + 1)),
                                y=lengths,
                                labels={'x': 'Paragraph #', 'y': 'Character Count'},
                                title=None
                            )
                            st.plotly_chart(fig, use_container_width=True)

                        with col2:
                            st.markdown("#### 📝 Full Text Output")
                            st.text_area("Paragraphs", "\n\n".join(paras), height=400)

                    else:
                        st.warning("⚠ No paragraph content found for this selection.")
            
            elif total_results > 0 and valid_count == 0:
                st.warning(f"⚠ The search returned {total_results} results, but none contained both a 'title' and 'urn'. Check the raw results above for details.")
            
            else:
                # This should technically not be hit if total_results > 0, 
                # but serves as a final catch if 'options' is empty.
                st.warning("⚠ No valid text entries found.")
                
    else:
        st.warning(f"⚠ No texts found from ctext.org for the keyword '{keyword}'. Try a broader search term.")

except Exception as e:
    st.error(f"❌ An unexpected error occurred during the search: {e}")





