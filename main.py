import streamlit as st
import pdfplumber
import google.generativeai as genai
import json
import os


genai.configure(api_key="AIzaSyBi-CV-dMeDQkQvSbc8Zd1DyqNOfowNEo4")

model = genai.GenerativeModel('gemini-2.0-flash-001')

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file-like object using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error("Error extracting text from PDF: " + str(e))
    return text

def ats_extractor(resume_text):
    """
    Send the extracted resume text to the Gemini API with a prompt
    that instructs the model to parse the resume into JSON format.
    """
    prompt = (
        "You are an AI bot designed to act as a professional for parsing resumes. "
        "You are given a resume and your job is to extract the following information:\n"
        "1. full name\n"
        "2. employment details\n"
        "3. Skills\n"
        "4. Education\n"
        "5. Work Experience\n"
        "6. Projects\n\n"
        "Give the extracted information in json format only."
    )
    
    full_prompt = f"{prompt}\n\nResume Data:\n{resume_text}"
    
    try:
        response = model.generate_content(
            contents=full_prompt,
            generation_config={
                'temperature': 0.0,
                'max_output_tokens': 1500,
            }
        )
        if response and response.text:
            return response.text
        else:
            st.error("No response from the AI model.")
            return None
    except Exception as e:
        st.error("Error during resume parsing: " + str(e))
        return None
    
def extract_keywords(resume_text):
    """
    Send the extracted resume text to the Gemini API with a prompt
    that instructs the model to extract keywords from the resume.
    """
    keywords_list = []

    prompt = (
        "Extract key keywords or phrases from the following resume text:\n\n"
        f"{resume_text}\n\n"
        "Identify and list the most important keywords or key phrases in the text to match with any job description. "
        "These keywords should capture the main skills, roles, or subjects discussed in the resume."
        "The keywords should be relevant to the content of the resume and should be useful for matching the resume to job descriptions."
        "The keywords should be extracted from the resume text itself, not generated or inferred."
        "The keywords should be listed in a readable format, such as a comma-separated list or a bulleted list."
        "Don't categorize them differently, just list them as a flat list of keywords or key phrases."
    )
    
    try:
        response = model.generate_content(
            contents=prompt,
            generation_config={
                'temperature': 0.0,
                'max_output_tokens': 500,
            }
        )
        if response and response.text:
            return response.text
        else:
            st.error("No response from the AI model for keyword extraction.")
            return None
    except Exception as e:
        st.error("Error during keyword extraction: " + str(e))
        return keywords_list


def main():
    st.title("Resume Parser")
    st.write("Upload your resume as a PDF file below.")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        resume_text = extract_text_from_pdf(uploaded_file)
        keyword_output = extract_keywords(resume_text)

        
        if resume_text:
            # Optionally display the extracted resume text (for debugging purposes)
            #st.text_area("Extracted Resume Text", resume_text, height=300)

            st.write("Analyzing resume with AI...")
            parsed_output = ats_extractor(resume_text)
            
            if parsed_output:
                st.subheader("Parsed Resume Data (JSON):")
                try:
                    parsed_json = json.loads(parsed_output)
                    st.json(parsed_json)
                except json.JSONDecodeError:
                    st.code(parsed_output, language="json")

            if keyword_output:
                st.subheader("Extracted Keywords:")
                st.code(keyword_output, language="text")
        else:
            st.error("No text could be extracted from the uploaded resume.")
    else:
        st.info("Please upload a PDF file to begin.")

            
    

if __name__ == "__main__":
    main()
