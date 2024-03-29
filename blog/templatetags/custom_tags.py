from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from taggit.models import Tag
import time
import readtime
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import Post, Admin
register = template.Library()


@register.simple_tag
def total_posts(author):
    return Post.published.filter(author=author).count()


@register.filter
def read(html):
    return readtime.of_html(html)


@register.simple_tag
def get_title():
    admin = Admin.objects.first()
    if admin.title:
        return admin.title
    return "ahampriyanshu"


@register.simple_tag
def get_desc():
    admin = Admin.objects.first()
    if admin.desc:
        return admin.desc
    return "Language is humanity's most spectacular open-source project"


@register.simple_tag
def get_author():
    admin = Admin.objects.first()
    if admin.owner:
        return admin.owner
    return "Priyanshu Tiwari"


@register.filter
def highlight_search(text, search):
    text = text.lower()
    highlighted = text.replace(
        search, '<span class="text-teal-500">{}</span>'.format(search))
    return mark_safe(highlighted)


@register.inclusion_tag('trending.html')
def show_trending_posts(count=4):
    trending_posts = Post.published.filter(publish__gte=datetime.now(
        tz=timezone.utc) - timedelta(days=7)).order_by('views')[:count]
    return {'trending_posts': trending_posts}


@register.inclusion_tag('latest.html')
def show_latest_posts(count=4):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('footer_about.html')
def get_about():
    admin = Admin.objects.order_by('pk')[:1]
    return {'admin': admin}


@register.inclusion_tag('popular.html')
def common_tags(count=5):
    tags = Post.tags.most_common()[:count]
    return {'tags': tags}


@register.inclusion_tag('discussed.html')
def show_commented_posts(count=4):
    commented_posts = Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'commented_posts': commented_posts}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
