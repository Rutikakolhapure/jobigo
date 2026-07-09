from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CoverLetterRequestSerializer, CoverLetterResponseSerializer, MatchRequestSerializer
from .services import EmbeddingService
from django.conf import settings

try:
    import openai
    openai.api_key = settings.OPENAI_API_KEY
except Exception:
    openai = None

class CoverLetterView(APIView):
    def post(self, request):
        serializer = CoverLetterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # Use OpenAI to generate cover letter if possible
        prompt = f"Write a professional cover letter based on the resume:\n{data['resume_text']}\n\nJob description:\n{data['job_description']}\n\nSkills:\n{', '.join(data.get('skills', []))}\n\nCover letter:"
        if openai:
            try:
                resp = openai.ChatCompletion.create(model=settings.OPENAI_COMPLETION_MODEL, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                text = resp.choices[0].message.content.strip()
            except Exception:
                text = ""  # fallback
        else:
            # simple fallback template
            text = f"Dear Hiring Manager,\n\nI am excited to apply... (auto-generated stub).\n\nRegards,\nCandidate"
        return Response({'cover_letter': text})

class MatchJobsView(APIView):
    def post(self, request):
        serializer = MatchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        results = EmbeddingService.embed_and_match(data['text'], top_k=data.get('top_k', 10))
        # Return job IDs and scores
        out = [{'job': r['job'], 'score': r['score']} for r in results]
        return Response({'results': out})
