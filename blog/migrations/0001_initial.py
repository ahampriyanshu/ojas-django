# Generated by Django 3.2.1 on 2021-05-09 08:33

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import embed_video.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=15, null=True)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('button1_title', models.CharField(blank=True, max_length=10, null=True)),
                ('button1_url', models.URLField(blank=True, null=True, unique=True)),
                ('button2_title', models.CharField(blank=True, max_length=10, null=True)),
                ('button2_url', models.URLField(blank=True, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('instagram', models.URLField(blank=True, null=True, unique=True)),
                ('twitter', models.URLField(blank=True, null=True, unique=True)),
                ('reddit', models.URLField(blank=True, null=True, unique=True)),
                ('telegram', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('github', models.URLField(blank=True, null=True, unique=True)),
                ('linkedin', models.URLField(blank=True, null=True, unique=True)),
                ('default_page', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default='Yes')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, default='default/author.png', null=True, upload_to='author')),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('bio', models.TextField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('instagram', models.URLField(blank=True, null=True, unique=True)),
                ('twitter', models.URLField(blank=True, null=True, unique=True)),
                ('reddit', models.URLField(blank=True, null=True, unique=True)),
                ('telegram', models.URLField(blank=True, null=True, unique=True)),
                ('github', models.URLField(blank=True, null=True, unique=True)),
                ('linkedin', models.URLField(blank=True, null=True, unique=True)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('sub_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('token', models.CharField(blank=True, max_length=128, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('created_date',),
            },
        ),
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.PositiveIntegerField(default=0)),
                ('ip', models.CharField(default=None, max_length=16)),
                ('session', models.CharField(default=None, max_length=50)),
                ('last_visited', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=100, unique_for_date='publish')),
                ('body', ckeditor.fields.RichTextField(blank=True, max_length=2000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/%Y/%m/%d/')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('video', embed_video.fields.EmbedVideoField(blank=True, null=True)),
                ('views', models.PositiveIntegerField(default=0, editable=False)),
                ('unique_visitor', models.PositiveIntegerField(default=0, editable=False)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='blog.author')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('body', models.TextField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
