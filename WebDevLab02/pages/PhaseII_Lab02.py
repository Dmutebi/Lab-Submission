import streamlit as st
from ctext import setlanguage, searchtexts, gettextasparagraphlist
import plotly.express as px
import requests
import json
import time


setlanguage("en")


def generate_analysis(text):
    """Calls the Gemini API to generate a thematic analysis of the text."""
    
    MAX_CHARS = 15000 
    text_content = text if len(text) <= MAX_CHARS else text[:MAX_CHARS] + "..."
    
  
    system_prompt = "You are a specialized Sinologist and literary critic. Provide a concise, thematic analysis of the classical Chinese text provided. Focus on the core philosophical concepts, major figures, and the overall structure. The response must be formatted as a single, coherent paragraph."
    user_query = f"Analyze the core themes and structure of this text:\n\n---\n{text_content}"
    
    
    api_key = "" 
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }
    

    max_retries = 5
    delay = 1
    
    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)
            
            result = response.json()
            
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            
            return generated_text
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429 and attempt < max_retries - 1:
                # Retry on rate limiting with increasing delay
                time.sleep(delay)
                delay *= 2
            else:
                raise e
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                raise e

    return "Error: Could not retrieve analysis after multiple attempts."


st.title("📚 Classical Chinese Text Explorer")
st.write("Try entering Chinese keywords like: `道`, `仁`, `禮`, `天`, `德`")

keyword = st.text_input("Enter a Chinese keyword to search:")

if keyword:
    try:
        results = searchtexts(keyword)
    
        st.subheader("🔍 Raw Search Results (for debugging)")
        st.json(results)
        
        options = {}
        
        if results:
            for r in results:
                if isinstance(r, dict) and 'title' in r and 'urn' in r:
                    label = f"{r['title']} ({r['urn']})"
                    options[label] = r['urn']
                    
        if options:
            selected_label = st.selectbox("Select a text:", list(options.keys()))
            
            if selected_label:
                urn = options[selected_label]
                
                paras = gettextasparagraphlist(urn)
                full_text = "\n\n".join(paras)

                st.success(f"✅ {len(paras)} paragraphs loaded from `{urn}`")

                with st.spinner("🧠 Generating thematic analysis using Gemini..."):
                    llm_analysis = generate_analysis(full_text)
                
                st.subheader("💡 Gemini Thematic Analysis")
                st.markdown(llm_analysis)
                
            
                lengths = [len(p) for p in paras]
                
                
                fig = px.bar(
                    x=list(range(1, len(lengths) + 1)),
                    y=lengths,
                    labels={'x': 'Paragraph #', 'y': 'Character Count'},
                    title='Paragraph Length Distribution'
                )
                
          
                st.plotly_chart(fig)
                st.text_area("📜 Full Text", full_text, height=300)
        
        elif results:
            st.warning("⚠ Results were returned, but none had both 'title' and 'urn'. The API format may have changed or keyword is too broad.")
        
        else:
            st.info(f"😔 No texts found for the keyword '{keyword}'.")
    except Exception as e:
       
        st.error(f"❌ An error occurred during search or processing: {e}")
        
else:
    st.info("⏳ Please enter a Chinese keyword above to begin the search.")



