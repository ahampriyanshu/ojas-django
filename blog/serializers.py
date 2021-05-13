from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.CharField()
    body = serializers.CharField()
    tags = serializers.CharField()
    author = serializers.CharField()
    publish = serializers.CharField()
    hidden = serializers.HiddenField(default = 1)