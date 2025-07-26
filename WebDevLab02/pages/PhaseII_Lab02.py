import streamlit as st
from ctext import setlanguage, searchtexts, gettextasparagraphlist
import plotly.express as px
import requests
setlanguage("en")

st.title("📚 Classical Chinese Text Explorer")
st.write("Try entering Chinese keywords like: `道`, `仁`, `禮`, `天`, `德`")

keyword = st.text_input("Enter a Chinese keyword to search:")

if keyword:
    try:
        results = searchtexts(keyword)
        st.subheader("🔍 Raw Search Results (for debugging)")
        st.json(results)

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

                st.success(f"✅ {len(paras)} paragraphs loaded from `{urn}`")

                
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
            st.warning("⚠ Results were returned, but none had both 'title' and 'urn'. The API format may have changed or keyword is too broad.")

    except Exception as e:
        st.error(f"❌ Error during search or processing: {e}")
else:
    st.info("⏳ Please enter a keyword above to begin.")


