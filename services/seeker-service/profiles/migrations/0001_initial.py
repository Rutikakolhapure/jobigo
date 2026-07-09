from django.db import migrations, models
import django.db.models.deletion
import uuid

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(unique=True, verbose_name='User ID')),
                ('headline', models.CharField(blank=True, max_length=255, verbose_name='Headline')),
                ('summary', models.TextField(blank=True, verbose_name='Summary')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='Location')),
                ('profile_completion_percentage', models.IntegerField(default=0, verbose_name='Profile Completion')),
                ('resume_url', models.URLField(blank=True, verbose_name='Resume URL')),
                ('portfolio_url', models.URLField(blank=True, verbose_name='Portfolio URL')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub URL')),
                ('linkedin_url', models.URLField(blank=True, verbose_name='LinkedIn URL')),
                ('website_url', models.URLField(blank=True, verbose_name='Website URL')),
                ('years_of_experience', models.IntegerField(default=0, verbose_name='Years of Experience')),
                ('current_job_title', models.CharField(blank=True, max_length=255, verbose_name='Current Job Title')),
                ('current_company', models.CharField(blank=True, max_length=255, verbose_name='Current Company')),
                ('is_open_to_opportunities', models.BooleanField(default=True, verbose_name='Open to Opportunities')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted At')),
            ],
            options={'db_table': 'candidate_profiles', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('school_name', models.CharField(max_length=255, verbose_name='School Name')),
                ('field_of_study', models.CharField(blank=True, max_length=255, verbose_name='Field of Study')),
                ('degree', models.CharField(blank=True, max_length=100, verbose_name='Degree')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('is_current', models.BooleanField(default=False, verbose_name='Currently Studying')),
                ('grade', models.CharField(blank=True, max_length=10, verbose_name='Grade')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('profile', models.ForeignKey(on_delete=models.CASCADE, related_name='education', to='profiles.candidateprofile')),
            ],
            options={'db_table': 'education', 'ordering': ['-start_date']},
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=255, verbose_name='Job Title')),
                ('company_name', models.CharField(max_length=255, verbose_name='Company Name')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='Location')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('is_current', models.BooleanField(default=False, verbose_name='Currently Working')),
                ('employment_type', models.CharField(blank=True, max_length=50, verbose_name='Employment Type')),
                ('industry', models.CharField(blank=True, max_length=100, verbose_name='Industry')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('profile', models.ForeignKey(on_delete=models.CASCADE, related_name='experience', to='profiles.candidateprofile')),
            ],
            options={'db_table': 'experience', 'ordering': ['-start_date']},
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('skill_name', models.CharField(max_length=100, verbose_name='Skill Name')),
                ('proficiency_level', models.CharField(choices=[('BEGINNER', 'Beginner'), ('INTERMEDIATE', 'Intermediate'), ('ADVANCED', 'Advanced'), ('EXPERT', 'Expert')], default='INTERMEDIATE', max_length=20, verbose_name='Proficiency Level')),
                ('years_of_experience', models.IntegerField(default=1, verbose_name='Years of Experience')),
                ('endorsements_count', models.IntegerField(default=0, verbose_name='Endorsements')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('profile', models.ForeignKey(on_delete=models.CASCADE, related_name='skills', to='profiles.candidateprofile')),
            ],
            options={'db_table': 'candidate_skills', 'ordering': ['-created_at'], 'unique_together': {('profile', 'skill_name')}},
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255, verbose_name='File Name')),
                ('file_url', models.URLField(verbose_name='File URL')),
                ('file_size', models.IntegerField(blank=True, null=True, verbose_name='File Size')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Primary Resume')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('profile', models.ForeignKey(on_delete=models.CASCADE, related_name='resumes', to='profiles.candidateprofile')),
            ],
            options={'db_table': 'resumes', 'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='skill',
            index=models.Index(fields=['profile'], name='candidate_s_profile_idx'),
        ),
        migrations.AddIndex(
            model_name='resume',
            index=models.Index(fields=['profile'], name='resumes_profile_idx'),
        ),
        migrations.AddIndex(
            model_name='experience',
            index=models.Index(fields=['profile'], name='experience_profile_idx'),
        ),
        migrations.AddIndex(
            model_name='experience',
            index=models.Index(fields=['start_date'], name='experience_start_d_idx'),
        ),
        migrations.AddIndex(
            model_name='education',
            index=models.Index(fields=['profile'], name='education_profile_idx'),
        ),
        migrations.AddIndex(
            model_name='candidateprofile',
            index=models.Index(fields=['user_id'], name='candidate_p_user_id_idx'),
        ),
        migrations.AddIndex(
            model_name='candidateprofile',
            index=models.Index(fields=['location'], name='candidate_p_locatio_idx'),
        ),
        migrations.AddIndex(
            model_name='candidateprofile',
            index=models.Index(fields=['created_at'], name='candidate_p_created_idx'),
        ),
    ]
