import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    """Company model."""

    class CompanySize(models.TextChoices):
        STARTUP = 'STARTUP', _('Startup')
        SMALL = 'SMALL', _('Small')
        MEDIUM = 'MEDIUM', _('Medium')
        LARGE = 'LARGE', _('Large')
        ENTERPRISE = 'ENTERPRISE', _('Enterprise')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    website = models.URLField(_('Website'), blank=True)
    logo_url = models.URLField(_('Logo URL'), blank=True)
    cover_image_url = models.URLField(_('Cover Image URL'), blank=True)
    email = models.EmailField(_('Email'), blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    industry = models.CharField(_('Industry'), max_length=100, blank=True)
    company_size = models.CharField(
        _('Company Size'),
        max_length=20,
        choices=CompanySize.choices,
        blank=True
    )
    founded_year = models.IntegerField(_('Founded Year'), null=True, blank=True)
    headquarters = models.CharField(_('Headquarters'), max_length=255, blank=True)
    is_verified = models.BooleanField(_('Is Verified'), default=False)
    created_by = models.UUIDField(_('Created By'), help_text='User ID from auth service')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    deleted_at = models.DateTimeField(_('Deleted At'), null=True, blank=True)

    class Meta:
        db_table = 'companies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['industry']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name
