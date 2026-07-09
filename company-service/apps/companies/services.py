from django.utils.text import slugify
from .models import Company, Job, Category, Location, Skill
from .repositories import JobRepository
from django.utils import timezone

class CompanyService:
    @staticmethod
    def create_company(name, website=None, description=None, logo=None):
        slug = slugify(name)[:200]
        c = Company.objects.create(name=name, slug=slug, website=website, description=description, logo=logo)
        return c

class JobService:
    @staticmethod
    def publish_job(job):
        job.status = Job.STATUS_PUBLISHED
        job.posted_at = timezone.now()
        job.save()
        return job

    @staticmethod
    def close_job(job):
        job.status = Job.STATUS_CLOSED
        job.save()
        return job

    @staticmethod
    def create_job(company, **kwargs):
        job = Job.objects.create(company=company, **kwargs)
        return job
