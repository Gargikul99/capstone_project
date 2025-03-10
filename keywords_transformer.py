from sentence_transformers import SentenceTransformer

class KeywordsTransformer:

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def transform_keywords(self, keywords):
        keywords= keywords.replace("Here's a list of key keywords and phrases extracted from the resume text:\n\n", "")
        keyword_list = keywords.split(",")
        print("Keywords list:", keyword_list)
        
        keyword_embeddings = self.model.encode(keyword_list)
        print(type(keyword_embeddings), keyword_embeddings.shape)
        return keyword_embeddings
