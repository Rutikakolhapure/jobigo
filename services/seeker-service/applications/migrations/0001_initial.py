from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('job_id', models.UUIDField(verbose_name='Job ID')),
                ('candidate_id', models.UUIDField(verbose_name='Candidate ID')),
                ('cover_letter', models.TextField(blank=True, verbose_name='Cover Letter')),
                ('resume_url', models.URLField(blank=True, verbose_name='Resume URL')),
                ('status', models.CharField(choices=[('APPLIED', 'Applied'), ('SHORTLISTED', 'Shortlisted'), ('REJECTED', 'Rejected'), ('OFFERED', 'Offered'), ('ACCEPTED', 'Accepted'), ('DECLINED', 'Declined')], default='APPLIED', max_length=20, verbose_name='Status')),
                ('applied_at', models.DateTimeField(auto_now_add=True, verbose_name='Applied At')),
                ('viewed_at', models.DateTimeField(blank=True, null=True, verbose_name='Viewed At')),
                ('rejected_at', models.DateTimeField(blank=True, null=True, verbose_name='Rejected At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted At')),
            ],
            options={'db_table': 'job_applications', 'ordering': ['-applied_at'], 'unique_together': {('job_id', 'candidate_id')}},
        ),
        migrations.CreateModel(
            name='SavedJob',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('candidate_id', models.UUIDField(verbose_name='Candidate ID')),
                ('job_id', models.UUIDField(verbose_name='Job ID')),
                ('saved_at', models.DateTimeField(auto_now_add=True, verbose_name='Saved At')),
            ],
            options={'db_table': 'saved_jobs', 'ordering': ['-saved_at'], 'unique_together': {('candidate_id', 'job_id')}},
        ),
        migrations.AddIndex(
            model_name='savedjob',
            index=models.Index(fields=['candidate_id'], name='saved_jobs_candidate_idx'),
        ),
        migrations.AddIndex(
            model_name='savedjob',
            index=models.Index(fields=['job_id'], name='saved_jobs_job_id_idx'),
        ),
        migrations.AddIndex(
            model_name='jobapplication',
            index=models.Index(fields=['job_id'], name='job_applicat_job_id_idx'),
        ),
        migrations.AddIndex(
            model_name='jobapplication',
            index=models.Index(fields=['candidate_id'], name='job_applicat_candidat_idx'),
        ),
        migrations.AddIndex(
            model_name='jobapplication',
            index=models.Index(fields=['status'], name='job_applicat_status_idx'),
        ),
        migrations.AddIndex(
            model_name='jobapplication',
            index=models.Index(fields=['applied_at'], name='job_applicat_applied__idx'),
        ),
    ]
