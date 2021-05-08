from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
import time
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Q
from taggit.models import Tag
from .models import Post, Comment, Author, Viewer, Contact, About, Subscriber
from .forms import CommentForm
from rest_framework import viewsets
from .serializers import PostSerializer
import logging
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.templatetags.static import static
from ojas import version
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import email.mime.application
from django.utils.html import strip_tags
import re
from django.contrib import messages
import base64
import logging
import traceback
from django.conf import settings
import logging, traceback
from django.urls import reverse
import requests
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
import secrets
import string

logger = logging.getLogger('ojas.pwa.views')

def offline(request):
    return render(request, 'offline.html')

def fill_dynamic_cache(request, id):
    return render(request, 'fill_dynamic_cache.html', context={'id': id})


@never_cache
def must_not_cache(request):
    return render(request, 'must_not_cache.html', context={'requested_at': timezone.now()})



def validate_email(email):    
    if email is None:
        return "Email is required."
    elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        return "Invalid Email Address !"
    else:
        return None


def send_confirmation_mail(email, confirmation_url, site_url):
    ctx = {
        'confirmation_url': confirmation_url,
        'site_url':site_url,    
    }
    message = get_template('subscription.html').render(ctx)
    msg = EmailMessage(
        'Please Confirm Your Subscription',
        message,
        'contactahampriyanshu@gmail.com',
        [email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    try:
        msg.send()
        print("Mail successfully sent")
        return True
    except Exception as e:
        print(e)
        return False

def subscription_confirmation(request):
    if "POST" == request.method:
        return render(request, 'offline.html', {})

    token = request.GET.get("token", None)

    if token:
        try:
            subscribe_model_instance = Subscriber.objects.get(token=token)
            new_token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(128))
            subscribe_model_instance.confirmed = True
            subscribe_model_instance.token = str(new_token)
            subscribe_model_instance.save()
            messages.success(request, "Subscription Confirmed. Thank you.")
        except Subscriber.DoesNotExist as e:
            logging.getLogger("warning").warning(traceback.format_exc())
            messages.error(request, "Invalid Link")
    else:
        logging.getLogger("warning").warning("Invalid token ")
        messages.error(request, "Invalid Link")

    return render(request, 'offline.html', {})


def unsubscribe(request):
    if "POST" == request.method:
        return render(request, 'offline.html', {})
        
    token = request.GET.get("token", None)
    email = request.GET.get("email", None)

    print(token, email)

    if token and email:
        try:
            subscribe_model_instance = Subscriber.objects.get(token=token,email=email)
            subscribe_model_instance.delete()
            messages.success(request, "Unsubscribed successfully.Sorry to see you go.")
        except Subscriber.DoesNotExist as e:
            logging.getLogger("warning").warning(traceback.format_exc())
            messages.error(request, "Invalid Link")
    else:
        logging.getLogger("warning").warning("Invalid token or email")
        messages.error(request, "Invalid Link")

    return render(request, 'offline.html', {})

    # This is the main subscription view

def subscribe(request):
    post_data = request.POST.copy()
    email = post_data.get("email", None)
    token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(128))
    try:
        subscribe_model_instance = Subscriber.objects.get(email=email)
        print('\n\n\nEmail already exist\n\n\n')
    except Subscriber.DoesNotExist:
        site_url = request.build_absolute_uri
        confirmation_url = request.build_absolute_uri(reverse('blog:subscription_confirmation')) + "?token=" + token
        status = send_confirmation_mail(email, confirmation_url, site_url)
        if status:
            subscribe_model_instance = Subscriber()
            subscribe_model_instance.email = email
            subscribe_model_instance.token = str(token)
            subscribe_model_instance.save()
            print('\n\n\nEmail added\n\n\n')
            msg = "Mail sent to '" + email + "'. Please confirm your subscription by clicking on " \
                                                    "confirmation link provided in email. " \
                                                    "Please check your spam folder as well."
            messages.success(request, msg)
        else:
            msg = "Error while sending confirmation mail"
            messages.error(request, msg)
            print(msg)
    except Exception as e: 
        msg = "Email already exist"
        messages.error(request, msg)
        print(e)
        return False
    return render(request, 'offline.html', {})


class ServiceWorkerView(TemplateView):
    template_name = 'sw.js'
    content_type = 'application/javascript'
    name = 'sw.js'

    def get_context_data(self, **kwargs):
        return {
            'version': version,
            'icon_url': static('img/android-icon-512x512.png'),
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
