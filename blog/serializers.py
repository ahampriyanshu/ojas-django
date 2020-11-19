from rest_framework import serializers


# class Geeks(object):
#     def __init__(self, name,hidden):
#         self.title = title
#         self.slug = slug
#         self.body = body
#         self.author = hidden
#         self.tags = tags
#         self.views = hidden
#         self.unique_visitor = hidden


class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = serializers.CharField()
    body = serializers.CharField()
    author = serializers.CharField()
    publish = serializers.CharField()
    views = serializers.CharField()
    unique_visitor = serializers.CharField()
    hidden = serializers.HiddenField(default = 1)