from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
import time
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Q
from taggit.models import Tag
from .models import Post, Comment, Author, Viewer, Me
from .forms import CommentForm
from rest_framework import viewsets 
from .serializers import PostSerializer 


class PostViewSet(viewsets.ModelViewSet): 
    queryset = Post.objects.all() 
    serializer_class = PostSerializer 


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)  | 
            Q(body__icontains=query)   ).distinct()

    print(query)
    return render(request, 'search.html',  {
        'queryset': queryset,
        'query':query
    })


def error_404(request, exception):
        data = {}
        return render(request,'error_404.html', data)


def error_500(request):
        data = {}
        return render(request,'error_500.html', data)


def setup_tour(request):
        data = {}
        return render(request,'setup/step_1.html', data)


def about_page(request):
        data = {}
        return render(request,'about.html', data)


def contact_page(request):
        me = Me.objects.all()
        return render(request,'contact.html', {'me': me})


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
    return render(request, 'index.html', {'page': page, 'posts': posts, 'tag': tag})


def post_author(request, post_author):
    posts = Post.objects.filter(author__author__username = post_author).order_by('-publish')
    author = Author.objects.filter(author__username=post_author)

    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'author.html', {'page': page, 'posts': posts, 'author': author})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 9
    template_name = 'index.html'

def get_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)


    ip = get_ip(request)
    if not request.session.exists(request.session.session_key):
        request.session.create()
        sess_key = request.session.session_key
        unique_visit = Viewer(post = post.id, ip=ip, session = sess_key)
        post.views=post.views+1
        post.unique_visitor = post.unique_visitor+1
        unique_visit.save()
        post.save()
    else:
        sess_key = request.session.session_key
        view =  Viewer.objects.filter(post = post.id).filter(ip=ip).filter(session = sess_key)
        if not view:
            new_view = Viewer(post = post.id, ip=ip, session = sess_key)
            new_view.save()
            post.views=post.views+1
            post.unique_visitor = post.unique_visitor+1
            post.save()
        else:
            view =  Viewer.objects.filter(last_visited__lte= datetime.now(tz=timezone.utc)- timedelta(hours=1))
            if view:
                view[0].last_visited = datetime.now(tz=timezone.utc)
                view[0].save()
                post.views=post.views+1
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
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts})

