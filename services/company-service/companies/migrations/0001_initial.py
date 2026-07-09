from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('website', models.URLField(blank=True, verbose_name='Website')),
                ('logo_url', models.URLField(blank=True, verbose_name='Logo URL')),
                ('cover_image_url', models.URLField(blank=True, verbose_name='Cover Image URL')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Phone')),
                ('industry', models.CharField(blank=True, max_length=100, verbose_name='Industry')),
                ('company_size', models.CharField(blank=True, choices=[('STARTUP', 'Startup'), ('SMALL', 'Small'), ('MEDIUM', 'Medium'), ('LARGE', 'Large'), ('ENTERPRISE', 'Enterprise')], max_length=20, verbose_name='Company Size')),
                ('founded_year', models.IntegerField(blank=True, null=True, verbose_name='Founded Year')),
                ('headquarters', models.CharField(blank=True, max_length=255, verbose_name='Headquarters')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Is Verified')),
                ('created_by', models.UUIDField(verbose_name='Created By')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted At')),
            ],
            options={'db_table': 'companies', 'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['name'], name='companies_name_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['industry'], name='companies_industry_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['is_verified'], name='companies_verified_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['created_at'], name='companies_created_idx'),
        ),
    ]
