import streamlit as st
import google.generativeai as genai

# Title of App
st.title("Chinese Language Learning")

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team XX, Web Development - Section X")
st.subheader("Dembe Mutebi")


# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description
#       4. **Page Name**: Description

st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. Home Page
2. Characters Data-->Diplays data about the number of characters in each paragraph
3. Choose a Text!-->Lets you pick a text from the API by typing the name of the text or the name of the character
4. AI Chatbot-->Translating between both languages

""")

