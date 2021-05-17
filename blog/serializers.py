from rest_framework import serializers
from .models import Post
from django.conf import settings
from django.utils.html import strip_tags
import readtime


class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.CharField()
    publish = serializers.CharField()
    url = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    author = serializers.CharField()
    body = serializers.SerializerMethodField()

    def get_url(self, instance):
        domain = settings.ALLOWED_HOSTS[0]
        post_url = domain + instance.get_absolute_url()
        return post_url

    def get_body(self, instance):
        return strip_tags(instance.body).replace("\r\n", "")

    def get_read_time(self, instance):
        return str(readtime.of_html(instance.body))

    class Meta:
        model = Post
        fields = '__all__'
