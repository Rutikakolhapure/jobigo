from django.db import migrations, models
import django.db.models.deletion
import uuid

class Migration(migrations.Migration):

    initial = True
    dependencies = ['companies']

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('icon_url', models.URLField(blank=True, verbose_name='Icon URL')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={'db_table': 'categories', 'verbose_name_plural': 'Categories'},
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=100, verbose_name='State')),
                ('country', models.CharField(max_length=100, verbose_name='Country')),
                ('country_code', models.CharField(blank=True, max_length=2, verbose_name='Country Code')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={'db_table': 'locations', 'unique_together': {('city', 'state', 'country')}},
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('category', models.CharField(blank=True, max_length=50, verbose_name='Category')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={'db_table': 'skills'},
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description')),
                ('requirements', models.TextField(blank=True, verbose_name='Requirements')),
                ('responsibilities', models.TextField(blank=True, verbose_name='Responsibilities')),
                ('benefits', models.TextField(blank=True, verbose_name='Benefits')),
                ('location', models.CharField(max_length=255, verbose_name='Location')),
                ('location_type', models.CharField(choices=[('ONSITE', 'On-site'), ('REMOTE', 'Remote'), ('HYBRID', 'Hybrid')], default='ONSITE', max_length=20, verbose_name='Location Type')),
                ('salary_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Salary Min')),
                ('salary_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Salary Max')),
                ('experience_level', models.CharField(choices=[('ENTRY', 'Entry'), ('MID', 'Mid'), ('SENIOR', 'Senior'), ('LEAD', 'Lead')], default='MID', max_length=20, verbose_name='Experience Level')),
                ('employment_type', models.CharField(choices=[('FULL_TIME', 'Full Time'), ('PART_TIME', 'Part Time'), ('CONTRACT', 'Contract'), ('INTERNSHIP', 'Internship')], max_length=20, verbose_name='Employment Type')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('CLOSED', 'Closed'), ('ARCHIVED', 'Archived')], default='DRAFT', max_length=20, verbose_name='Status')),
                ('views_count', models.IntegerField(default=0, verbose_name='Views Count')),
                ('applications_count', models.IntegerField(default=0, verbose_name='Applications Count')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Deadline')),
                ('posted_by', models.UUIDField(verbose_name='Posted By')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted At')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, to='jobs.category')),
                ('company', models.ForeignKey(on_delete=models.CASCADE, related_name='jobs', to='companies.company')),
            ],
            options={'db_table': 'jobs', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='JobSkill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('proficiency_level', models.CharField(choices=[('BEGINNER', 'Beginner'), ('INTERMEDIATE', 'Intermediate'), ('ADVANCED', 'Advanced'), ('EXPERT', 'Expert')], max_length=20, verbose_name='Proficiency Level')),
                ('years_required', models.IntegerField(default=1, verbose_name='Years Required')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('job', models.ForeignKey(on_delete=models.CASCADE, related_name='skills', to='jobs.job')),
                ('skill', models.ForeignKey(on_delete=models.CASCADE, to='jobs.skill')),
            ],
            options={'db_table': 'job_skills', 'unique_together': {('job', 'skill')}},
        ),
        migrations.AddIndex(
            model_name='skill',
            index=models.Index(fields=['name'], name='skills_name_idx'),
        ),
        migrations.AddIndex(
            model_name='skill',
            index=models.Index(fields=['category'], name='skills_category_idx'),
        ),
        migrations.AddIndex(
            model_name='location',
            index=models.Index(fields=['country'], name='locations_country_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['company'], name='jobs_company_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['title'], name='jobs_title_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['location'], name='jobs_location_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['status'], name='jobs_status_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['created_at'], name='jobs_created_idx'),
        ),
    ]
