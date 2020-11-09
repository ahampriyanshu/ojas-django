from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts(author):
    return Post.published.filter(author = author).count()


@register.inclusion_tag('latest.html')
def show_latest_posts(count=4):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('most_commented.html')
def show_commented_posts(count=5):
    commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'commented_posts': commented_posts}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
