import pdfplumber

class PDFExtractor:
    '''
       
         This class uses pdf plumber to extract the text from the reume pdf

    '''
   
    @staticmethod
    def extract_text(uplaoded_file):
        text = ""
        try:
            with pdfplumber.open(uplaoded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print("Error extracting text from the Resume:"+str(e))
        return text
