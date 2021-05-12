from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment, Author, Viewer, Admin, Subscriber
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from django.templatetags.static import static
from datetime import datetime, timedelta
from rest_framework import viewsets
from .serializers import PostSerializer
from django.utils import timezone
from django.db.models import Count, Q
from django.utils.html import strip_tags
from django.conf import settings
from taggit.models import Tag
from .forms import CommentForm
from django.urls import reverse
from ojas import version
from django.contrib import messages
import logging, traceback
from django.urls import reverse
import requests
import secrets
import string
import re

logger = logging.getLogger('ojas.pwa.views')

def offline(request):
    return render(request, 'offline.html')


def send_subscription_mail(email, confirmation_url, request):
    ctx = {
        'confirmation_url': confirmation_url,
        'request':request,    
    }
    message = get_template('subscription.html').render(ctx)
    msg = EmailMessage(
        'Please Confirm Your Subscription',
        message,
        'contactahampriyanshu@gmail.com',
        [email],
    )
    msg.content_subtype = "html"
    try:
        msg.send()
        print("Mail successfully sent")
        return True
    except Exception as e:
        print(e)
        return False

def send_confirmation_mail(email, unsubsrcibe_url, request):
    ctx = {
        'unsubsrcibe_url': unsubsrcibe_url, 
        'request':request,    
    }
    message = get_template('confirmation.html').render(ctx)
    msg = EmailMessage(
        'Thank you for the confirmation',
        message,
        'contactahampriyanshu@gmail.com',
        [email],
    )
    msg.content_subtype = "html"
    try:
        msg.send()
        print("Mail successfully sent")
        return True
    except Exception as e:
        print(e)
        return False

def send_unsubscribe_mail(email, request):
    ctx = {  
         'request':request,    
    }
    message = get_template('unsubscribe.html').render(ctx)
    msg = EmailMessage(
        'Unsubscribed Successfully',
        message,
        'contactahampriyanshu@gmail.com',
        [email],
    )
    msg.content_subtype = "html"
    try:
        msg.send()
        print("Mail successfully sent")
        return True
    except Exception as e:
        print(e)
        return False

def subscription_confirmation(request):
    message = dict()
    if "POST" == request.method:
        message['status'] = 'Invalid request'
        message['instruction'] = 'Please send appropriate request'
        return render(request, 'status.html', {'message': message})

    token = request.GET.get("token", None)

    if token:
        try:
            subscribe_model_instance = Subscriber.objects.get(token=token)
            new_token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(128))
            subscribe_model_instance.confirmed = True
            subscribe_model_instance.token = str(new_token)
            email = subscribe_model_instance.email
            unsubsrcibe_url = request.build_absolute_uri(reverse('blog:unsubscribe')) + "?token=" + new_token + "&email=" + email
            send_confirmation_mail(email, unsubsrcibe_url, request )
            subscribe_model_instance.save()
            messages.success(request, "Subscription Confirmed. Thank you.")
            message['status'] = 'Yeah! Subscription Confirmed'
            message['msg'] = 'I will be sending you the latest articles once or twice a month.'
            message['instruction'] = 'Thank you'
        except Subscriber.DoesNotExist as e:
            message['status'] = 'Unknown error occured'
            message['msg'] = 'Check your internet connection'
            message['instruction'] = 'Please try reopening the link'
            logging.getLogger("warning").warning(traceback.format_exc())
            messages.error(request, e)
    else:
        message['status'] = 'Invalid token'
        message['msg'] = 'Check your internet connection'
        message['instruction'] = 'Please try reopening the link'
        logging.getLogger("warning").warning("Invalid token ")
        messages.error(request, "Invalid Link")

    return render(request, 'status.html', {'message': message})


def unsubscribe(request):
    message = dict()

    if "POST" == request.method:
        message['status'] = 'Invalid request'
        message['instruction'] = 'Please send appropriate request'
        return render(request, 'status.html', {'message': message})
        
    token = request.GET.get("token", None)
    email = request.GET.get("email", None)

    if token and email:
        try:
            subscribe_model_instance = Subscriber.objects.get(token=token,email=email)
            subscribe_model_instance.delete()
            send_unsubscribe_mail(email, request)
            message['status'] = 'Unsubscribed successfully'
            message['msg'] = 'Sorry to see you go :('
            message['instruction'] = 'Bye'
            messages.success(request, "Unsubscribed successfully. Sorry to see you go.")
        except Subscriber.DoesNotExist as e:
            message['status'] = 'Unknown error occured'
            message['msg'] = 'Check your internet connection'
            message['instruction'] = 'Please try reopening the link'
            logging.getLogger("warning").warning(traceback.format_exc())
            messages.error(request, "Invalid Link")
    else:
        logging.getLogger("warning").warning("Invalid token or email")
        messages.error(request, "Invalid Link")
        message['status'] = 'Invalid token or email'
        message['msg'] = 'Check your internet connection'
        message['instruction'] = 'Please try reopening the link'
    return render(request, 'status.html', {'message': message})

def subscribe(request):
    message = dict()
    post_data = request.POST.copy()
    email = post_data.get("email", None)
    token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(128))
    try:
        subscribe_model_instance = Subscriber.objects.get(email=email)
        message['status'] = 'Email entered already exist'
        message['msg'] = 'Search your inbox for confirmation mail'
        message['instruction'] = 'You may also contact the admin'
    except Subscriber.DoesNotExist:
        confirmation_url = request.build_absolute_uri(reverse('blog:subscription_confirmation')) + "?token=" + token
        status = send_subscription_mail(email, confirmation_url, request)
        if status:
            subscribe_model_instance = Subscriber()
            subscribe_model_instance.email = email
            subscribe_model_instance.token = str(token)
            subscribe_model_instance.save()
            message['status'] = "Mail sent to '" + email + "'"
            message['msg'] = 'Please confirm your subscription'
            message['instruction'] = 'Check your spam folder as well'
            msg = "Mail sent to '" + email + "'. Please confirm your subscription by clicking on " \
                                                    "confirmation link provided in email. " \
                                                    "Please check your spam folder as well."
            messages.success(request, msg)
        else:
            msg = "Error while sending confirmation mail"
            messages.error(request, msg)
            message['status'] = "Error occured while sending confirmation mail"
            message['msg'] = 'Please check your input for typo'
            message['instruction'] = 'And then try again'
    except Exception as e: 
        messages.error(request, e)
        message['status'] = 'Some unknown error occured'
        message['msg'] = ' Please try after some time'
        message['instruction'] = 'Meanwhile we are looking into it'
        return False
    return render(request, 'status.html', {'message': message})


class ServiceWorkerView(TemplateView):
    template_name = 'sw.js'
    content_type = 'application/javascript'
    name = 'sw.js'

    def get_context_data(self, **kwargs):
        return {
            'version': version,
            'icon_url': static('img/logo.png'),
            'manifest_url': static('manifest.json'),
            'style_url': static('css/tailwind.min.css'),
            'home_url': reverse('blog:most_viewed'),
            'offline_url': reverse('blog:offline'),
        }


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
    data = {}
    return render(request, 'about.html', data)

def contact_page(request):
    admin = Admin.objects.first()
    return render(request, 'contact.html', {'admin': admin})


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
        'device_name': request.user_agent.device.family ,
    }

    return render(request, 'me.html', {'me': me})


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
