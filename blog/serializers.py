from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.CharField()
    body = serializers.CharField()
    author = serializers.CharField()
    publish = serializers.CharField()
    views = serializers.CharField()
    unique_visitor = serializers.CharField()
    hidden = serializers.HiddenField(default = 1)