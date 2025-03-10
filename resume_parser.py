import google.generativeai as genai


class ResumeParser:

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')

    def parse_resume(self, resume_text):
        prompt= (
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
            response = self.model.generate_content(
                contents = full_prompt,
                generation_config={
                    'temperature': 0.0,
                    'max_output_tokens': 1500,
                }
            )
            if response and response.text:
                return response.text
            else:
                raise RuntimeError("No response from the AI model.")
        except Exception as e:
            raise RuntimeError("Error during resume parsing: " + str(e))