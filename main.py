import streamlit as st
import PyPDF2
import io
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("AI Resume Analyzer (FREE with Gemini)")
st.write("Upload your resume and get AI feedback.")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("API key not found. Add GEMINI_API_KEY to .env")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
job_role = st.text_input("Target Job Role (optional)")
analyze = st.button("Analyze Resume")


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(file.read()))
    return file.read().decode("utf-8")


if analyze and uploaded_file:
    try:
        content = extract_text(uploaded_file)

        if not content.strip():
            st.error("File is empty")
            st.stop()
    

        prompt = f"""
Analyze this resume and give structured feedback:

1. Content clarity
2. Skills
3. Experience
4. Improvements for {job_role if job_role else "general jobs"}

Resume:
{content}
"""

        model = genai.GenerativeModel("gemini-3-flash-preview")

        with st.spinner("Analyzing..."):
            response = model.generate_content(prompt)

        st.subheader("Analysis Result")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {str(e)}")