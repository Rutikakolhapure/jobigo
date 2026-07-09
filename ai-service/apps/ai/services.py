import os
import json
import numpy as np
import requests
from django.conf import settings
from .models import Embedding

try:
    import openai
    openai.api_key = settings.OPENAI_API_KEY
except Exception:
    openai = None

class EmbeddingService:
    @staticmethod
    def _to_vector(obj):
        if isinstance(obj, str):
            return np.array(json.loads(obj), dtype=float)
        if isinstance(obj, list):
            return np.array(obj, dtype=float)
        return np.array([], dtype=float)

    @staticmethod
    def generate_embedding(text):
        """Generate embedding for text using OpenAI if available, otherwise deterministic fallback."""
        if settings.OPENAI_API_KEY and openai:
            try:
                resp = openai.Embedding.create(model=settings.OPENAI_MODEL, input=text)
                vec = resp['data'][0]['embedding']
                return vec
            except Exception:
                pass
        # Deterministic fallback: use simple hashing to vector
        import hashlib
        h = hashlib.sha256(text.encode('utf-8')).digest()
        # create 128-d vector from hash bytes
        vec = [b / 255.0 for b in h]
        return vec

    @staticmethod
    def save_embedding(source, text, vector):
        ev = Embedding.objects.create(source=source, text=text, vector=json.dumps(vector))
        return ev

    @staticmethod
    def cosine_similarity(a, b):
        a = np.array(a, dtype=float)
        b = np.array(b, dtype=float)
        if a.size == 0 or b.size == 0:
            return 0.0
        denom = (np.linalg.norm(a) * np.linalg.norm(b))
        if denom == 0:
            return 0.0
        return float(np.dot(a, b) / denom)

    @staticmethod
    def embed_and_match(text, top_k=10):
        """Fetch jobs from company service, generate embeddings, compare and return ranked jobs."""
        # Generate query embedding
        q_emb = EmbeddingService.generate_embedding(text)

        # Fetch jobs from company service
        url = settings.COMPANY_SERVICE_URL.rstrip('/') + '/jobs/'
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            jobs = r.json()
        except Exception:
            # In failure, return empty
            jobs = []

        results = []
        for job in jobs:
            job_id = job.get('id')
            desc = job.get('description') or job.get('title') or ''
            # generate embedding for job
            job_vec = EmbeddingService.generate_embedding(desc)
            score = EmbeddingService.cosine_similarity(q_emb, job_vec)
            results.append({'job': job, 'score': score})
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
