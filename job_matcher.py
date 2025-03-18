from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

class JobMatcher:

    def __init__(self, job_postings_csv):
        self.job_df = pd.read_csv(job_postings_csv)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.job_embeddings = None

    def preprocess_job_descriptions(self):
        self.job_df['combined_text'] = (
            self.job_df['title'].fillna('') + " " + self.job_df['description'].fillna('')
        )
        print("Preprocessing completed. Combined text ready!")

    def encode_jobs(self):
        combined_texts = self.job_df['combined_text'].tolist()

        # Batch encode with progress bar
        print("Starting to encode job descriptions...")
        self.job_embeddings = self.model.encode(
            combined_texts,
            batch_size=32,
            show_progress_bar=True
        )
        print("Job encoding complete!")

    def match_resume(self, resume_keyword_embeddings, top_k=5):
        if self.job_embeddings is None:
            raise ValueError("Run encode_jobs() before matching resumes.")

        if len(resume_keyword_embeddings.shape) > 1:
            resume_embedding = np.mean(resume_keyword_embeddings, axis=0)
        else:
            resume_embedding = resume_keyword_embeddings

        resume_embedding = resume_embedding.reshape(1, -1)

        similarities = cosine_similarity(resume_embedding, self.job_embeddings)

        top_k_indices = similarities[0].argsort()[::-1][:top_k]

        matches = self.job_df.iloc[top_k_indices].copy()
        matches['similarity'] = similarities[0][top_k_indices]

        # ✅ Fixed column name
        matches = matches.sort_values(by='similarity', ascending=False)
        return matches[['title', 'company_name', 'location', 'similarity', 'description', 'job_posting_url']]
    



