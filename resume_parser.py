import google.generativeai as genai
import json

class ResumeParser:

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')

    def parse_resume(self, resume_text):
        prompt = (
            "You are an AI bot designed to act as a professional for parsing resumes. "
            "You are given a resume and your job is to extract the following information:\n"
            "1. Full Name\n"
            "2. Employment Details\n"
            "3. Skills\n"
            "4. Education\n"
            "5. Work Experience\n"
            "6. Projects\n\n"
            "Give the extracted information in JSON format only. DO NOT include explanations or additional text."
        )

        full_prompt = f"{prompt}\n\nResume Data:\n{resume_text}"

        try:
            response = self.model.generate_content(
                contents=full_prompt,
                generation_config={
                    'temperature': 0.0,
                    'max_output_tokens': 1500,
                }
            )

            if response and response.text:
                raw_text = response.text.strip()

                print("RAW RESPONSE FROM GEMINI API:")
                print(raw_text)

                # Extract JSON portion
                json_start = raw_text.find('{')
                json_end = raw_text.rfind('}') + 1

                if json_start == -1 or json_end == -1:
                    raise RuntimeError("AI response does not contain valid JSON structure.")

                json_str = raw_text[json_start:json_end]

                parsed_json = json.loads(json_str)

                return parsed_json

            else:
                raise RuntimeError("No response from the AI model.")
        
        except Exception as e:
            raise RuntimeError("Error during resume parsing: " + str(e))
