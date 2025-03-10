import google.generativeai as genai


class KeywordsExtractor:

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')

    def extract_keywords(self, resume_text):
        prompt= ("Extract key keywords or phrases from the following resume text:\n\n"
        f"{resume_text}\n\n"
        "Identify and list the most important keywords or key phrases in the text to match with any job description. "
        "These keywords should capture the main skills, roles, or subjects discussed in the resume."
        "The keywords should be relevant to the content of the resume and should be useful for matching the resume to job descriptions."
        "The keywords should be extracted from the resume text itself, not generated or inferred."
        "The keywords should be listed in a readable format, such as a comma-separated list or a bulleted list."
        "Don't categorize them differently, just list them as a flat list of keywords or key phrases."
    )
    
        try:
            response = self.model.generate_content(
                contents = prompt,
                generation_config = {
                    'temperature':0.0,
                    'max_output_tokens':500
                }
,            )
            if response and response.text:
                return response.text
            else:
                raise RuntimeError("No response from the AI model for keyword extraction.")
        except Exception as e:
            raise RuntimeError("Error during keyword extraction:"+ str(e))
        