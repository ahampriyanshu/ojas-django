from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
import time
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Q
from taggit.models import Tag
from .models import Post, Comment, Author, Viewer, Contact, About
from .forms import CommentForm
from rest_framework import viewsets
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.published.all()
    serializer_class = PostSerializer


def search(request):
    queryset = Post.published.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(author__author__username__icontains=query)).distinct()

    return render(request, 'search.html',  {
        'queryset': queryset,
        'query': query
    })


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def error_404(request, exception):
    data = {}
    return render(request, 'error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error_500.html', data)


def about_page(request):
    about = About.objects.order_by('pk')[:1]

    if about[0].default_page:
        data = {}
    else:
        data = {'about': about}

    return render(request, 'about.html', data)


def me(request):

    if request.user_agent.is_mobile:
        device = 'mobile'
    if request.user_agent.is_tablet:
        device = 'tablet'
    if request.user_agent.is_pc:
        device = 'pc'

    me = {
        'device': device,
        'bot': request.user_agent.is_bot,
        'touch': request.user_agent.is_touch_capable,
        'browser': request.user_agent.browser.family,
        'browser_version': request.user_agent.browser.version_string,
        'ip': get_ip(request),
        'os': request.user_agent.os.family,
        'time': datetime.now(),
    }

    return render(request, 'me.html', {'me': me})


def contact_page(request):
    contacts = Contact.objects.all()
    return render(request, 'contact.html', {'contacts': contacts})


def most_viewed(request):
    posts = Post.published.order_by('views')[:9]
    return render(request, 'index.html', {'posts': posts})


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'article.html', {'page': page, 'posts': posts, 'tag': tag})


def post_author(request, post_author):
    posts = Post.published.filter(
        author__author__username=post_author).order_by('-publish')
    author = Author.objects.filter(author__username=post_author)

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'author.html', {'page': page, 'posts': posts, 'author': author})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)

    ip = get_ip(request)
    if not request.session.exists(request.session.session_key):
        request.session.create()
        sess_key = request.session.session_key
        unique_visit = Viewer(post=post.pk, ip=ip, session=sess_key)
        post.views = post.views+1
        post.unique_visitor = post.unique_visitor+1
        unique_visit.save()
        post.save()
    else:
        sess_key = request.session.session_key
        view = Viewer.objects.filter(post=post.pk).filter(
            ip=ip).filter(session=sess_key)
        if not view:
            new_view = Viewer(post=post.pk, ip=ip, session=sess_key)
            new_view.save()
            post.views = post.views+1
            post.unique_visitor = post.unique_visitor+1
            post.save()
        else:
            view = Viewer.objects.filter(last_visited__lte=datetime.now(
                tz=timezone.utc) - timedelta(hours=1))
            print(view)
            if view:
                view[0].last_visited = datetime.now(tz=timezone.utc)
                view[0].save()
                post.views = post.views+1
                post.save()

    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.pk)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts})
