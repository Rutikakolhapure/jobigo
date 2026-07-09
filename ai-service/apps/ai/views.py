from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CoverLetterRequestSerializer, CoverLetterResponseSerializer, MatchRequestSerializer
from .services import EmbeddingService
from django.conf import settings
import re

SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')

def summarize_by_overlap(text, keywords, max_sentences=3):
    sentences = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
    if not sentences:
        return ''
    if not keywords:
        return ' '.join(sentences[:max_sentences])
    scores = []
    lower_keywords = [k.lower() for k in keywords]
    for s in sentences:
        s_l = s.lower()
        score = sum(s_l.count(k) for k in lower_keywords)
        scores.append((score, s))
    scores.sort(key=lambda x: x[0], reverse=True)
    selected = [s for sc, s in scores if sc > 0]
    if len(selected) < max_sentences:
        # pad with leading sentences
        for s in sentences:
            if s not in selected:
                selected.append(s)
            if len(selected) >= max_sentences:
                break
    return ' '.join(selected[:max_sentences])

class CoverLetterView(APIView):
    def post(self, request):
        serializer = CoverLetterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        resume = data['resume_text']
        job_desc = data['job_description']
        skills = data.get('skills', [])

        # Extract a brief summary of resume and job description focusing on skills
        resume_summary = summarize_by_overlap(resume, skills, max_sentences=4)
        job_summary = summarize_by_overlap(job_desc, skills, max_sentences=2)

        # Build a professional cover letter using templates and the summaries
        title_match = re.search(r"(?i)(?:position|role|title)[:\s]*([A-Za-z0-9 \-]+)", job_desc)
        job_title = title_match.group(1).strip() if title_match else None

        opening = f"Dear Hiring Manager,\n\nI am excited to apply for the {job_title if job_title else 'open position'} at your company."
        middle = f"\n\nBased on my background, here are a few highlights from my resume: {resume_summary}\n\nThe role's key focus areas that match my experience include: {job_summary}\n\nI believe my skills in {', '.join(skills) if skills else 'relevant areas'} make me a strong fit for this role."
        closing = "\n\nThank you for considering my application. I would welcome the opportunity to discuss how I can contribute to your team.\n\nSincerely,\nCandidate"
        cover_letter = opening + middle + closing
        return Response({'cover_letter': cover_letter})

class MatchJobsView(APIView):
    def post(self, request):
        serializer = MatchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        results = EmbeddingService.embed_and_match(data['text'], top_k=data.get('top_k', 10))
        # Return job IDs and scores
        out = [{'job': r['job'], 'score': r['score']} for r in results]
        return Response({'results': out})
