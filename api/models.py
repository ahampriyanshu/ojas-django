from django.db import models
from tastypie.resources import ModelResource
from blog.models import Post, Author

class PostResource(ModelResource):
    class Meta:
        queryset = Post.objects.all()
        resource_name = 'post'

class AuthorResource(ModelResource):
    class Meta:
        queryset = Author.objects.all()
        resource_name = 'author'