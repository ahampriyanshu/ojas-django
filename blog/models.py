from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField
from ckeditor.fields import RichTextField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Admin(models.Model):
    title = models.CharField(help_text = "title of the blog",max_length=15, blank=True, null=True)
    owner = models.CharField(help_text = "full name of owner",max_length=100, blank=True, null=True)
    image = models.ImageField(help_text = "image preview in admin panel might look either condensed or pixelated, ignore that",upload_to='admin/', blank=True, null=True, default='default/admin.png')
    desc = models.TextField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100,  blank=True, null=True)
    number = models.PositiveIntegerField(help_text = "append 91 infront of your number eg 919917956610",blank=True, null=True)
    greeting = models.CharField(max_length=100,  blank=True, null=True, default='Hi%20there')
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    youtube = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    instagram = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    twitter = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    reddit = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    telegram = models.URLField(help_text = "https://t.me/username",blank=True, null=True)
    github = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    gitlab = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    quora = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    dribble = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    unsplash = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    linkedin = models.URLField(help_text = "URL of the profile",blank=True, null=True)

    def __str__(self):
        return self.owner


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(help_text = "image preview in admin panel might look either condensed or pixelated, ignore that",upload_to='author', blank=True, null=True, default='default/author.png')
    joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    instagram = models.URLField(help_text = "URL of the profile",blank=True, null=True, unique=True)
    youtube = models.URLField(help_text = "URL of the profile",blank=True, null=True)
    twitter = models.URLField(help_text = "URL of the profile",blank=True, null=True, unique=True)
    reddit = models.URLField(help_text = "URL of the profile",blank=True, null=True, unique=True)
    telegram = models.URLField(help_text = "https://t.me/username",blank=True, null=True, unique=True)
    github = models.URLField(help_text = "URL of the profile",blank=True, null=True, unique=True)
    linkedin = models.URLField(help_text = "URL of the profile",blank=True, null=True, unique=True)
    gitlab = models.URLField(help_text = "URL of the profile",blank=True, unique=True, null=True)
    quora = models.URLField(help_text = "URL of the profile",blank=True, unique=True, null=True)
    dribble = models.URLField(help_text = "URL of the profile",blank=True, unique=True, null=True)
    unsplash = models.URLField(help_text = "URL of the profile",blank=True, unique=True, null=True)

    def __str__(self):
        return self.author.username


class Viewer(models.Model):
    post = models.PositiveIntegerField(default=0)
    ip = models.CharField(max_length=16, default=None)
    session = models.CharField(max_length=50, default=None)
    last_visited = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.ip


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(help_text = "don't edit this, if you don't know what you are doing",max_length=100, unique_for_date='publish')
    author = models.ForeignKey(Author, editable=False, on_delete=models.CASCADE)
    body = RichTextField(max_length=10000, blank=True, null=True)
    image = models.ImageField(help_text = "image preview in admin panel might look either condensed or pixelated, ignore that", upload_to='blog/%Y/%m/%d/', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    notified = models.BooleanField(default=False)
    video = EmbedVideoField(blank=True, null=True)
    views = models.PositiveIntegerField(editable=False, default=0)
    unique_visitor = models.PositiveIntegerField(editable=False, default=0)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE,editable=False)
    name = models.CharField(max_length=80)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

class Subscriber(models.Model):
    sub_id = models.AutoField(primary_key=True, null=False, blank=True)
    email = models.EmailField(null=False, blank=False, max_length=200, unique=True)
    confirmed = models.BooleanField(default=False)
    token = models.CharField(max_length=128, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return self.email