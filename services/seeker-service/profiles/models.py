import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class CandidateProfile(models.Model):
    """Candidate profile model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(_('User ID'), unique=True, help_text='User ID from auth service')
    headline = models.CharField(_('Headline'), max_length=255, blank=True)
    summary = models.TextField(_('Summary'), blank=True)
    location = models.CharField(_('Location'), max_length=255, blank=True)
    profile_completion_percentage = models.IntegerField(_('Profile Completion'), default=0)
    resume_url = models.URLField(_('Resume URL'), blank=True)
    portfolio_url = models.URLField(_('Portfolio URL'), blank=True)
    github_url = models.URLField(_('GitHub URL'), blank=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True)
    website_url = models.URLField(_('Website URL'), blank=True)
    years_of_experience = models.IntegerField(_('Years of Experience'), default=0)
    current_job_title = models.CharField(_('Current Job Title'), max_length=255, blank=True)
    current_company = models.CharField(_('Current Company'), max_length=255, blank=True)
    is_open_to_opportunities = models.BooleanField(_('Open to Opportunities'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    deleted_at = models.DateTimeField(_('Deleted At'), null=True, blank=True)

    class Meta:
        db_table = 'candidate_profiles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['location']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Profile - {self.user_id}"

class Education(models.Model):
    """Education model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='education')
    school_name = models.CharField(_('School Name'), max_length=255)
    field_of_study = models.CharField(_('Field of Study'), max_length=255, blank=True)
    degree = models.CharField(_('Degree'), max_length=100, blank=True)
    start_date = models.DateField(_('Start Date'), blank=True, null=True)
    end_date = models.DateField(_('End Date'), blank=True, null=True)
    is_current = models.BooleanField(_('Currently Studying'), default=False)
    grade = models.CharField(_('Grade'), max_length=10, blank=True)
    description = models.TextField(_('Description'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        db_table = 'education'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['profile']),
        ]

    def __str__(self):
        return f"{self.school_name} - {self.degree}"

class Experience(models.Model):
    """Work experience model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(_('Job Title'), max_length=255)
    company_name = models.CharField(_('Company Name'), max_length=255)
    location = models.CharField(_('Location'), max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=True)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'), blank=True, null=True)
    is_current = models.BooleanField(_('Currently Working'), default=False)
    employment_type = models.CharField(_('Employment Type'), max_length=50, blank=True)
    industry = models.CharField(_('Industry'), max_length=100, blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        db_table = 'experience'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['profile']),
            models.Index(fields=['start_date']),
        ]

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Resume(models.Model):
    """Resume model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='resumes')
    file_name = models.CharField(_('File Name'), max_length=255)
    file_url = models.URLField(_('File URL'))
    file_size = models.IntegerField(_('File Size'), null=True, blank=True)
    is_primary = models.BooleanField(_('Primary Resume'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        db_table = 'resumes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['profile']),
        ]

    def __str__(self):
        return f"{self.file_name}"

class Skill(models.Model):
    """Candidate skills model."""

    class ProficiencyLevel(models.TextChoices):
        BEGINNER = 'BEGINNER', _('Beginner')
        INTERMEDIATE = 'INTERMEDIATE', _('Intermediate')
        ADVANCED = 'ADVANCED', _('Advanced')
        EXPERT = 'EXPERT', _('Expert')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(_('Skill Name'), max_length=100)
    proficiency_level = models.CharField(
        _('Proficiency Level'),
        max_length=20,
        choices=ProficiencyLevel.choices,
        default=ProficiencyLevel.INTERMEDIATE
    )
    years_of_experience = models.IntegerField(_('Years of Experience'), default=1)
    endorsements_count = models.IntegerField(_('Endorsements'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        db_table = 'candidate_skills'
        ordering = ['-created_at']
        unique_together = ['profile', 'skill_name']
        indexes = [
            models.Index(fields=['profile']),
        ]

    def __str__(self):
        return f"{self.skill_name} - {self.proficiency_level}"
