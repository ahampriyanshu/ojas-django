from django.contrib import sitemaps
from .models import Post


class PostSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish
