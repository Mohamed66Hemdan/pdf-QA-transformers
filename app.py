# ===============================  
# Enhanced Document QA System 
# ===============================  

import streamlit as st
import PyPDF2
import re
from transformers import pipeline

# ===============================  
# Load QA Model
# ===============================  
qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# ===============================  
# Function to read PDF
# ===============================  
def read_pdf(file_path):
    """Reads a PDF file and returns its text as a string."""
    text = ""
    pdf = PyPDF2.PdfReader(file_path)
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# ===============================  
# Function to split text into chapters
# ===============================  
def split_chapters(text):
    """
    Splits text into chapters based on 'Chapter X' headings.
    Returns a dict: { "Chapter 1": "text", "Chapter 2": "text", ... }
    """
    chapters = {}
    lines = text.split("\n")
    current_chap = None
    for line in lines:
        line = line.strip()
        if line.startswith("Chapter"):
            chap_num = line.split("—")[0].strip()  # e.g., "Chapter 1"
            current_chap = chap_num
            chapters[current_chap] = ""
        elif current_chap:
            chapters[current_chap] += line + " "
    return chapters

# ===============================  
# Function to ask a question on a specific context
# ===============================  
def ask_question(context, question):
    """Uses QA model to answer question from given context."""
    result = qa_model(question=question, context=context)
    return result['answer']

# ===============================  
# Streamlit UI
# ===============================  
st.set_page_config(page_title="📄 Document QA System", page_icon="🤖", layout="wide")
st.markdown(
    """
    <h1 style='text-align: center; color: #4B0082;'>Document Question Answering System 📄🤖</h1>
    <p style='text-align: center; color: #6A5ACD;'>Upload a PDF or TXT file and ask questions about its content!</p>
    """,
    unsafe_allow_html=True
)

# Upload file section
uploaded_file = st.file_uploader("Upload a PDF or TXT file:", type=["pdf", "txt"], key="file_uploader")

if uploaded_file:
    # Read content
    if uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)
    else:
        text = str(uploaded_file.read(), "utf-8")

    # Split text into chapters
    chapters = split_chapters(text)

    # Sidebar: show chapters for reference
    st.sidebar.header("📚 Chapters in Document")
    for chap in chapters.keys():
        st.sidebar.write(chap)

    # User input: question
    st.markdown("### Ask a Question About Your Document")
    question = st.text_input("Enter your question here:")

    if question:
        # Try to detect chapter number from question
        chap_match = re.search(r"Chapter (\d+)", question, re.IGNORECASE)
        if chap_match:
            chap_num = chap_match.group(1)
            chap_key = f"Chapter {chap_num}"
            context = chapters.get(chap_key, text)  # fallback to full text
        else:
            context = text  # use full text if no chapter specified

        # Get answer
        answer = ask_question(context, question)

        # Display answer in styled box
        st.markdown(
            f"""
            <div style='background-color:#E6E6FA; padding:15px; border-radius:10px;'>
                <h3 style='color:#4B0082;'>Answer:</h3>
                <p style='font-size:18px; color:#333;'>{answer}</p>
            </div>
            """,
            unsafe_allow_html=True
        )