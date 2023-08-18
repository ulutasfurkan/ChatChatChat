
pip install openai
pip install streamlit
pip install PyMuPDF

import streamlit as st
import openai
import fitz  # PyMuPDF

# OpenAI API Setup
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'  # Replace this with your OpenAI API Key
openai.api_key = OPENAI_API_KEY


# Extract text from the uploaded PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ''
    for page in doc:
        text += page.get_text("text")
    return text


# Function to ask OpenAI based on the context from the PDF
def ask_openai(question, pdf_context):
    response = openai.Completion.create(
        model="text-davinci-002",  # or any other suitable model
        prompt=pdf_context + "\n\nQ: " + question + "\nA:",
        max_tokens=100,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()


# Streamlit UI
st.title("PDF-based Chatbot with OpenAI")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)

    st.write("PDF uploaded successfully!")

    user_input = st.text_input("Ask a question based on the PDF content:")

    if st.button('Reply'):
        # Query OpenAI with the context from the PDF
        response = ask_openai(user_input, pdf_text)
        st.write("Bot:", response)

st.write("Note: The chatbot's answers are derived from OpenAI based on the content of the uploaded PDF.")

streamlit run chatbot_app.py
