import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from companies.models import Company

class Category(models.Model):
    """Job category model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'), blank=True)
    icon_url = models.URLField(_('Icon URL'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Location(models.Model):
    """Job location model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(_('City'), max_length=100)
    state = models.CharField(_('State'), max_length=100, blank=True)
    country = models.CharField(_('Country'), max_length=100)
    country_code = models.CharField(_('Country Code'), max_length=2, blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        db_table = 'locations'
        unique_together = ['city', 'state', 'country']
        indexes = [
            models.Index(fields=['country']),
        ]

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"

class Skill(models.Model):
    """Skill model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Name'), max_length=100, unique=True)
    category = models.CharField(_('Category'), max_length=50, blank=True)
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        db_table = 'skills'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name

class Job(models.Model):
    """Job posting model."""

    class LocationType(models.TextChoices):
        ONSITE = 'ONSITE', _('On-site')
        REMOTE = 'REMOTE', _('Remote')
        HYBRID = 'HYBRID', _('Hybrid')

    class ExperienceLevel(models.TextChoices):
        ENTRY = 'ENTRY', _('Entry')
        MID = 'MID', _('Mid')
        SENIOR = 'SENIOR', _('Senior')
        LEAD = 'LEAD', _('Lead')

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', _('Full Time')
        PART_TIME = 'PART_TIME', _('Part Time')
        CONTRACT = 'CONTRACT', _('Contract')
        INTERNSHIP = 'INTERNSHIP', _('Internship')

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        PUBLISHED = 'PUBLISHED', _('Published')
        CLOSED = 'CLOSED', _('Closed')
        ARCHIVED = 'ARCHIVED', _('Archived')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'))
    requirements = models.TextField(_('Requirements'), blank=True)
    responsibilities = models.TextField(_('Responsibilities'), blank=True)
    benefits = models.TextField(_('Benefits'), blank=True)
    location = models.CharField(_('Location'), max_length=255)
    location_type = models.CharField(
        _('Location Type'),
        max_length=20,
        choices=LocationType.choices,
        default=LocationType.ONSITE
    )
    salary_min = models.DecimalField(_('Salary Min'), max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(_('Salary Max'), max_digits=12, decimal_places=2, null=True, blank=True)
    experience_level = models.CharField(
        _('Experience Level'),
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.MID
    )
    employment_type = models.CharField(
        _('Employment Type'),
        max_length=20,
        choices=EmploymentType.choices
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    views_count = models.IntegerField(_('Views Count'), default=0)
    applications_count = models.IntegerField(_('Applications Count'), default=0)
    deadline = models.DateField(_('Deadline'), null=True, blank=True)
    posted_by = models.UUIDField(_('Posted By'), help_text='User ID from auth service')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    deleted_at = models.DateTimeField(_('Deleted At'), null=True, blank=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['title']),
            models.Index(fields=['location']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

class JobSkill(models.Model):
    """Job skill requirement model."""

    class ProficiencyLevel(models.TextChoices):
        BEGINNER = 'BEGINNER', _('Beginner')
        INTERMEDIATE = 'INTERMEDIATE', _('Intermediate')
        ADVANCED = 'ADVANCED', _('Advanced')
        EXPERT = 'EXPERT', _('Expert')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(
        _('Proficiency Level'),
        max_length=20,
        choices=ProficiencyLevel.choices
    )
    years_required = models.IntegerField(_('Years Required'), default=1)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        db_table = 'job_skills'
        unique_together = ['job', 'skill']

    def __str__(self):
        return f"{self.job.title} - {self.skill.name}"
