import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class JobApplication(models.Model):
    """Job application model."""

    class Status(models.TextChoices):
        APPLIED = 'APPLIED', _('Applied')
        SHORTLISTED = 'SHORTLISTED', _('Shortlisted')
        REJECTED = 'REJECTED', _('Rejected')
        OFFERED = 'OFFERED', _('Offered')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        DECLINED = 'DECLINED', _('Declined')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_id = models.UUIDField(_('Job ID'), help_text='Job ID from company service')
    candidate_id = models.UUIDField(_('Candidate ID'), help_text='User ID from auth service')
    cover_letter = models.TextField(_('Cover Letter'), blank=True)
    resume_url = models.URLField(_('Resume URL'), blank=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED
    )
    applied_at = models.DateTimeField(_('Applied At'), auto_now_add=True)
    viewed_at = models.DateTimeField(_('Viewed At'), null=True, blank=True)
    rejected_at = models.DateTimeField(_('Rejected At'), null=True, blank=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    deleted_at = models.DateTimeField(_('Deleted At'), null=True, blank=True)

    class Meta:
        db_table = 'job_applications'
        ordering = ['-applied_at']
        unique_together = ['job_id', 'candidate_id']
        indexes = [
            models.Index(fields=['job_id']),
            models.Index(fields=['candidate_id']),
            models.Index(fields=['status']),
            models.Index(fields=['applied_at']),
        ]

    def __str__(self):
        return f"Application - {self.candidate_id} for {self.job_id}"

class SavedJob(models.Model):
    """Saved job model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate_id = models.UUIDField(_('Candidate ID'), help_text='User ID from auth service')
    job_id = models.UUIDField(_('Job ID'), help_text='Job ID from company service')
    saved_at = models.DateTimeField(_('Saved At'), auto_now_add=True)

    class Meta:
        db_table = 'saved_jobs'
        ordering = ['-saved_at']
        unique_together = ['candidate_id', 'job_id']
        indexes = [
            models.Index(fields=['candidate_id']),
            models.Index(fields=['job_id']),
        ]

    def __str__(self):
        return f"Saved Job - {self.candidate_id}"
