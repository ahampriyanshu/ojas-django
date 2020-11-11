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


# class UrlHit(models.Model):
#     url     = models.URLField()
#     hits    = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return str(self.url)

#     def increase(self):
#         self.hits += 1
#         self.save()


# class HitCount(models.Model):
#     url_hit = models.ForeignKey(UrlHit, editable=False, on_delete=models.CASCADE)
#     ip      = models.CharField(max_length=40)
#     session = models.CharField(max_length=40)
#     date    = models.DateTimeField(auto_now=True)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user', blank = True, null = True)
    joined = models.DateTimeField(default=timezone.now)
    bio = RichTextField(max_length=100, blank = True, null = True)
    email = models.EmailField(blank = True, null = True)


    def __str__(self):
        return self.user.username


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    author = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    body = RichTextField(max_length=1500,blank = True, null = True)
    cover = models.ImageField(upload_to='blog', blank = True, null = True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() 
    published = PublishedManager()
    tags = TaggableManager()
    video = EmbedVideoField(blank = True, null = True)
    views = models.PositiveIntegerField(default=0)



    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        print(self.publish)
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE,)
    name = models.CharField(max_length=80)
    email = models.EmailField(blank = True, null = True)
    body = RichTextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
