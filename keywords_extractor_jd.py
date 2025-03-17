import google.generativeai as genai
import re

class KeywordsExtractor:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')

    def extract_keywords(self, job_desc):
        prompt = (
            "Extract key keywords or phrases from the following Job Description:\n\n"
            f"{job_desc}\n\n"
            "Identify and list the most important keywords or key phrases in the text that will be needed to search for a candidate to match with this job description. "
            "The keywords should be directly taken from the job description, not generated or inferred. "
            "Provide the output as a **comma-separated list** of keywords or phrases. No additional text or explanations."
        )
    
        try:
            response = self.model.generate_content(
                contents=prompt,
                generation_config={
                    'temperature': 0.0,
                    'max_output_tokens': 500
                }
            )
            if response and response.text:
                # Extract keywords using regex (assuming comma-separated output)
                keywords_text = response.text.strip()
                keywords_list = re.split(r',\s*', keywords_text)  # Convert to a list
                
                return keywords_list  # Return a list instead of raw text
            else:
                raise RuntimeError("No response from the AI model for keyword extraction.")
        except Exception as e:
            raise RuntimeError("Error during keyword extraction: " + str(e))
