from .models import Job, Company
from django.db.models import Q

class JobRepository:
    @staticmethod
    def create_job(**kwargs):
        return Job.objects.create(**kwargs)

    @staticmethod
    def update_job(job, **kwargs):
        for k, v in kwargs.items():
            setattr(job, k, v)
        job.save()
        return job

    @staticmethod
    def get_job_by_id(job_id):
        try:
            return Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return None

    @staticmethod
    def search_jobs(q=None, category_id=None, location_id=None, skill_id=None, employment_type=None, remote=None, salary_min=None, salary_max=None, status='PUBLISHED'):
        qs = Job.objects.filter(status=status)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category_id:
            qs = qs.filter(categories__id=category_id)
        if location_id:
            qs = qs.filter(locations__id=location_id)
        if skill_id:
            qs = qs.filter(skills__id=skill_id)
        if employment_type:
            qs = qs.filter(employment_type=employment_type)
        if remote is not None:
            qs = qs.filter(remote=remote)
        if salary_min:
            qs = qs.filter(salary_max__gte=salary_min)
        if salary_max:
            qs = qs.filter(salary_min__lte=salary_max)
        return qs.distinct()
