from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count, Q
from taggit.models import Tag
from .models import Post, Comment, Author, Viewer
from .forms import CommentForm
import time
import datetime


def error_404(request, exception):
        data = {}
        return render(request,'error_404.html', data)


def error_500(request):
        data = {}
        return render(request,'error_500.html', data)


def setup_tour(request):
        data = {}
        return render(request,'setup/step_1.html', data)


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
    posts = Post.objects.filter(author__username=post_author)
    authors = Author.objects.filter(user__username=post_author)
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'author.html', {'page': page, 'posts': posts, 'authors' : authors })


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 9
    template_name = 'index.html'
    

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)

    if not request.session.exists(request.session.session_key):
        request.session.create() 
        yup = datetime.datetime.now()
        request.session['member_id'] = yup
        post.views=post.views+1
        post.save()
    else:
        print(request.session['member_id'])
        post.views=post.views+1
        post.save()

    
    def get_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        print(x_forwarded_for)
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    ip = get_ip(request)
    print(ip)
    u = Viewer(viewer=ip)
    result = Viewer.objects.filter(Q(viewer__icontains = ip))
    if len(result) == 1:
        print("USER EXIST")
    elif len(result)>1:
        print("AGAIN NOT AN UNIQUE VISITOR")
    else:
        u.save()
        print("unique visitor")

    views_t = Viewer.objects.all().count()
    print(views_t)
    

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

