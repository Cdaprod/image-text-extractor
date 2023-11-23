#!/usr/local/bin python3 
# pip install streamlit
import streamlit as st
import requests

st.title("Image Text Extractor")

input_url = st.text_input("Enter the URL of the page:")
extract_button = st.button("Extract Text")

if extract_button and input_url:
    response = requests.post("http://localhost:5001/extract-text", json={"url": input_url})
    if response.status_code == 200:
        data = response.json()
        for snippet in data['data']:
            st.write(f"Image {snippet['id']}: {snippet['extracted_text']}")
    else:
        st.write("Failed to extract text")