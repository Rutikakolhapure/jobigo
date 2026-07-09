import io
from pdfminer.high_level import extract_text
import docx
import re
from django.conf import settings

SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')

def extract_text_from_pdf(file_path):
    try:
        text = extract_text(file_path)
        return text
    except Exception:
        return ''

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full = []
        for p in doc.paragraphs:
            full.append(p.text)
        return '\n'.join(full)
    except Exception:
        return ''

def summarize_text_by_keywords(text, keywords=None, max_sentences=3):
    sentences = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
    if not sentences:
        return ''
    if not keywords:
        return ' '.join(sentences[:max_sentences])
    lower_keywords = [k.lower() for k in keywords]
    scores = []
    for s in sentences:
        s_l = s.lower()
        score = sum(s_l.count(k) for k in lower_keywords)
        scores.append((score, s))
    scores.sort(key=lambda x: x[0], reverse=True)
    selected = [s for sc, s in scores if sc > 0]
    if len(selected) < max_sentences:
        for s in sentences:
            if s not in selected:
                selected.append(s)
            if len(selected) >= max_sentences:
                break
    return ' '.join(selected[:max_sentences])

class ResumeService:
    @staticmethod
    def parse_resume(file_path):
        if file_path.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception:
                text = ''
        # lightweight summary
        summary = summarize_text_by_keywords(text, keywords=None, max_sentences=4)
        return text, summary
