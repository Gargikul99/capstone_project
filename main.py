import streamlit as st
import json
from config import Config
from pdf_extractor import PDFExtractor
from resume_parser import ResumeParser
from keywords_extractor import KeywordsExtractor
from keywords_transformer import KeywordsTransformer

class App:
    def __init__(self):
        self.config = Config()
        self.pdf_extractor = PDFExtractor()
        self.resume_parser = ResumeParser(api_key=self.config.API_KEY)
        self.keyword_extractor = KeywordsExtractor(api_key=self.config.API_KEY)
        self.keywords_transformer = KeywordsTransformer()

    def run(self):
        st.title("Resume Parser")
        st.write("Upload your resume as a PDF file below.")
        
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        
        if uploaded_file is not None:
            try:
                resume_text = self.pdf_extractor.extract_text(uploaded_file)
                
                if resume_text:
                    st.text_area("Extracted Resume Text", resume_text, height=300)

                    st.write("Analyzing resume with AI...")
                    parsed_output = self.resume_parser.parse_resume(resume_text)
                    
                    if parsed_output:
                        st.subheader("Parsed Resume Data (JSON):")
                        try:
                            parsed_json = json.loads(parsed_output)
                            st.json(parsed_json)
                        except json.JSONDecodeError:
                            st.code(parsed_output, language="json")

                    st.write("Extracting keywords with AI...")
                    keywords_output = self.keyword_extractor.extract_keywords(resume_text)
                    
                    if keywords_output:
                        st.subheader("Extracted Keywords:")
                        st.write(keywords_output)

                        # Transform keywords and print the list
                        keyword_embeddings = self.keywords_transformer.transform_keywords(keywords_output)
                        st.write("Keyword Embeddings:", keyword_embeddings)
                    
                else:
                    st.error("No text could be extracted from the uploaded resume.")
            except Exception as e:
                st.error(str(e))
        else:
            st.info("Please upload a PDF file to begin.")

if __name__ == "__main__":
    app = App()
    app.run()
