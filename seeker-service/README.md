# Seeker Service for JobiGo

This service manages candidate profiles, resumes, education, experience, saved & applied jobs.

Features
- Django + DRF
- Resume upload (PDF/DOCX) stored locally
- Resume parsing and summary using pdfminer.six, python-docx and spaCy (local)
- Profile completion scoring
- SavedJobs and AppliedJobs referencing job IDs from company-service
- Dockerized with entrypoint that runs migrations and installs spaCy model if needed

All features use free/local libraries — no paid APIs.
