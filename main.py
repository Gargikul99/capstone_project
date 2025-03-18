"""
import streamlit as st
from pdf_extractor import PDFExtractor
from resume_parser import ResumeParser
from keywords_extractor import KeywordsExtractor
from keywords_transformer import KeywordsTransformer



import json

# Initialize components
API_KEY = "AIzaSyBi-CV-dMeDQkQvSbc8Zd1DyqNOfowNEo4"  # Replace with your Gemini API key

parser = ResumeParser(API_KEY)
keyword_extractor = KeywordsExtractor(API_KEY)
keyword_transformer = KeywordsTransformer()


def main():
    st.set_page_config(page_title="Resume Parser & Link Extractor", layout="centered")
    
    st.title("📄 AI Resume Parser with Links & Keywords")

    uploaded_file = st.file_uploader("Upload your resume PDF", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner('Extracting resume text...'):
            resume_text = PDFExtractor.extract_text(uploaded_file)

        if not resume_text:
            st.error("Couldn't extract any text from the PDF. Try another file.")
            return

        st.subheader("Resume Text (Preview)")
        st.text_area("", resume_text[:1000], height=300)

        if st.button("Parse Resume"):
            with st.spinner('Parsing resume data...'):
                parsed_data = parser.parse_resume(resume_text)

            st.subheader("Parsed Resume Information")
            st.json(parsed_data)

        if st.button("Extract Keywords"):
            with st.spinner('Extracting keywords...'):
                keywords = keyword_extractor.extract_keywords(resume_text)

            st.subheader("Extracted Keywords")
            st.text(keywords)

            embeddings = keyword_transformer.transform_keywords(keywords)

            st.subheader("Keyword Embeddings (Shape)")
            st.write(f"Shape: {embeddings.shape}")
            
            # Optional: show first few embeddings
            st.write("Sample Embeddings:", embeddings[:3])

if __name__ == "__main__":
    main()
"""

import streamlit as st
from pdf_extractor import PDFExtractor
from resume_parser import ResumeParser
from keywords_extractor import KeywordsExtractor
from keywords_transformer import KeywordsTransformer
from job_matcher import JobMatcher

# ✅ SET PAGE CONFIG AT THE TOP BEFORE ANYTHING ELSE
st.set_page_config(page_title="Resume Parser & Job Matcher", layout="centered")

# Initialize components
API_KEY = "AIzaSyBi-CV-dMeDQkQvSbc8Zd1DyqNOfowNEo4"

parser = ResumeParser(API_KEY)
keyword_extractor = KeywordsExtractor(API_KEY)
keyword_transformer = KeywordsTransformer()

@st.cache_resource
def load_job_matcher():
    matcher = JobMatcher('job_postings_cleaned.csv')
    matcher.preprocess_job_descriptions()
    matcher.encode_jobs()
    return matcher

matcher = load_job_matcher()

def main():
    st.title("📄 AI Resume Parser & Job Matcher")

    uploaded_file = st.file_uploader("Upload your resume PDF", type=["pdf"])

    if uploaded_file is not None:
        st.info(f"Uploaded file: {uploaded_file.name}")

        with st.spinner('Extracting resume text...'):
            resume_text = PDFExtractor.extract_text(uploaded_file)

        if not resume_text:
            st.error("Couldn't extract any text from the PDF. Try another file.")
            return

        st.subheader("📑 Resume Text (Preview)")
        st.text_area("", resume_text[:1000], height=300)

        if st.button("🔍 Parse Resume"):
            with st.spinner('Parsing resume data...'):
                parsed_data = parser.parse_resume(resume_text)

            st.subheader("Parsed Resume Information")
            st.json(parsed_data)

        if st.button("📝 Extract Keywords & Match Jobs"):
            with st.spinner('Extracting keywords...'):
                keywords = keyword_extractor.extract_keywords(resume_text)

            st.subheader("Extracted Keywords")
            st.text(keywords)

            embeddings = keyword_transformer.transform_keywords(keywords)

            st.subheader("Keyword Embeddings")
            st.write(f"Shape: {embeddings.shape}")
            st.write("Sample Embeddings:", embeddings[:3])

            # Match with job descriptions
            with st.spinner('Finding matching job postings...'):
                top_matches = matcher.match_resume(embeddings, top_k=10)
                top_matches['similarity'] = top_matches['similarity'].round(2)

            st.subheader("🎯 Top Matching Job Postings")
            st.dataframe(top_matches)

if __name__ == "__main__":
    main()
