import streamlit as st
from ctext import setlanguage, searchtexts, gettextasparagraphlist
import plotly.express as px

setlanguage("en")

with st.container():
    st.title("📚 Classical Chinese Text Explorer")
    keyword = st.text_input("🔍 Enter a Chinese keyword to search:")

if keyword:
    results = searchtexts(keyword)

    if isinstance(results, list) and results:
        with st.container():
            st.markdown("### 📄 Matching Classical Texts")
            options = {}
            for r in results:
                if isinstance(r, dict) and 'title' in r and 'urn' in r:
                    label = f"{r['title']} ({r['urn']})"
                    options[label] = r['urn']

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
                        st.warning("⚠ No paragraph content found.")
            else:
                st.warning("⚠ No valid text entries found.")
    else:
        st.warning("⚠ No results found from ctext.org.")



