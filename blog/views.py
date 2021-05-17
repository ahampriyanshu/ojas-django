from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Author, Viewer, Admin, Subscriber
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.template.loader import get_template
from django.views.generic import TemplateView
from django.templatetags.static import static
from django.core.exceptions import BadRequest
from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from .serializers import PostSerializer
from django.db.models import Count, Q
from django.contrib import messages
from rest_framework import viewsets
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .forms import CommentForm
from taggit.models import Tag
from ojas import version
import logging
import traceback
import secrets
import string
logger = logging.getLogger(__name__)
domain = settings.ALLOWED_HOSTS[0]
logo_url = settings.LOGO_URL


def offline(request):
    """
    Returns offline/fallback page whenever user's internet connection is broken
    """
    return render(request, 'offline.html')


def get_ip(request):
    """
    Returns the IP of the user
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def error_400(request, exception):
    """
    Returns the custom Bad Request Error view
    """
    err = {
        'code': 'Error 400',
        'msg': exception,
    }
    return render(request, 'error.html', {'err': err})


def error_404(request, exception):
    """
    Returns the custom Not Found Error view
    """
    data = {}
    return render(request, 'error_404.html', data)


def error_403(request, exception):
    """
    Returns the custom PermissionDenied Error view
    """
    err = {
        'code': 'Error 403',
        'msg': 'Permission Denied',
    }
    return render(request, 'error.html', {'err': err})


def error_500(request):
    """
    Returns the custom Server Error view
    """
    err = {
        'code': 'Error 500',
        'msg': 'Server Error',
    }
    return render(request, 'error.html', {'err': err})


def about_page(request):
    """
    Returns the about page
    """
    data = {}
    return render(request, 'about.html', data)


def contact_page(request):
    """
    Returns the contact page
    """
    admin = Admin.objects.first()
    return render(request, 'contact.html', {'admin': admin})


def me(request):
    """
    Returns the know your details page
    """
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
        'device_name': request.user_agent.device.family,
    }

    return render(request, 'me.html', {'me': me})


def send_subscription_mail(email, confirmation_url):
    """
    Sends an email to the reader containing the confirmation link
    """
    ctx = {
        'confirmation_url': confirmation_url,
        'logo_url': logo_url,
        'domain': domain,
    }
    message = get_template('admin/subscription.html').render(ctx)
    msg = EmailMessage(
        'Please Confirm Your Subscription',
        message,
        'contactahampriyanshu@gmail.com',
        [email],
    )
    msg.content_subtype = "html"
    try:
        msg.send()
        logger.info("Email " + email + " successfully")
        return True
    except Exception as e:
        logger.error("Error ocuured while sending email to " +
                     email + " : " + e)
        return False


def send_confirmation_mail(email, unsubsrcibe_url):
    """
    Sends an email to the reader thanking him/her for confirmimng the subscription
    """
    ctx = {
        'unsubsrcibe_url': unsubsrcibe_url,
        'logo_url': logo_url,
        'domain': domain,
    }
    message = get_template('admin/confirmation.html').render(ctx)
    msg = EmailMessage(
        'Thank you for the confirmation',
        message,
        'contactahampriyanshu@gmail.com',
        [email],
    )
    msg.content_subtype = "html"
    try:
        msg.send()
        logger.info("Email " + email + " successfully")
        return True
    except Exception as e:
        logger.error("Error ocuured while sending email to " +
                     email + " : " + e)
        return False


def send_unsubscription_confirmation_mail(email):
    """
    Sends a farewell email to the reader after he/she unsubscribes
    """
    ctx = {
        'logo_url': logo_url,
        'domain': domain,
    }
    message = get_template('admin/unsubscribe.html').render(ctx)
    msg = EmailMessage(
        'Unsubscribed Successfully',
        message,
        'contactahampriyanshu@gmail.com',
        [email],
    )
    msg.content_subtype = "html"
    try:
        msg.send()
        logger.info("Email " + email + " successfully")
        return True
    except Exception as e:
        logger.error("Error ocuured while sending email to " +
                     email + " : " + e)
        return False


def subscription_confirmation(request):
    """
    Handle all the event after user click the confirmation link
    """
    message = dict()
    if "POST" == request.method:
        ip = get_ip(request)
        logger.warn(
            "User with IP : " + str(ip) + " made an inavlid request")
        raise BadRequest('Bad Request Method')
    token = request.GET.get("token", None)
    if token:
        try:
            subscribe_model_instance = Subscriber.objects.get(token=token)
            new_token = ''.join(secrets.choice(
                string.ascii_uppercase + string.digits) for i in range(128))
            subscribe_model_instance.confirmed = True
            subscribe_model_instance.token = str(new_token)
            email = subscribe_model_instance.email
            unsubsrcibe_url = request.build_absolute_uri(
                reverse('blog:unsubscribe')) + "?token=" + new_token + "&email=" + email
            send_confirmation_mail(email, unsubsrcibe_url)
            subscribe_model_instance.save()
            messages.success(request, "Subscription Confirmed. Thank you.")
            message['status'] = 'Yeah! Subscription Confirmed'
            message['msg'] = 'I will be sending you the latest articles once or twice a month.'
            message['instruction'] = 'Thank you'
            logger.info(email + " subscribed successfully")
        except Subscriber.DoesNotExist as e:
            message['status'] = 'Unknown error occured'
            message['msg'] = 'Check your internet connection'
            message['instruction'] = 'Please try reopening the link'
            logger.warning(traceback.format_exc())
    else:
        message['status'] = 'Invalid token'
        message['msg'] = 'Check your internet connection'
        message['instruction'] = 'Please try reopening the link'
        logger.warning("Invalid token ")
        messages.error(request, "Invalid Link")

    return render(request, 'admin/status.html', {'message': message})


def unsubscribe(request):
    """
    Handle all the event after user click the unsubscribe link
    """
    message = dict()

    if "POST" == request.method:
        ip = get_ip(request)
        logger.warn(
            "User with IP : " + str(ip) + " made an inavlid request")
        raise BadRequest('Bad Request Method')

    token = request.GET.get("token", None)
    email = request.GET.get("email", None)

    if token and email:
        try:
            subscribe_model_instance = Subscriber.objects.get(
                token=token, email=email)
            subscribe_model_instance.delete()
            send_unsubscription_confirmation_mail(email)
            message['status'] = 'Unsubscribed successfully'
            message['msg'] = 'Sorry to see you go :('
            message['instruction'] = 'Bye'
            logger.info(email + " unsubscribed successfully")
            messages.success(
                request, "Unsubscribed successfully. Sorry to see you go.")
        except Subscriber.DoesNotExist as e:
            message['status'] = 'Unknown error occured'
            message['msg'] = 'Check your internet connection'
            message['instruction'] = 'Please try reopening the link'
            logger.warning(traceback.format_exc())
            messages.error(request, "Invalid Link")
    else:
        logger.error("Error occured while " + email + " was unsubscribing")
        messages.error(request, "Invalid Link")
        message['status'] = 'Invalid token or email'
        message['msg'] = 'Check your internet connection'
        message['instruction'] = 'Please try reopening the link'
    return render(request, 'admin/status.html', {'message': message})


def subscribe(request):
    """
    Handle all the event once the user has entered a valid email address
    """
    message = dict()
    post_data = request.POST.copy()
    email = post_data.get("email", None)
    token = ''.join(secrets.choice(string.ascii_uppercase +
                    string.digits) for i in range(128))
    try:
        subscribe_model_instance = Subscriber.objects.get(email=email)
        message['status'] = 'Email entered already exist'
        message['msg'] = 'Search your inbox for confirmation mail'
        message['instruction'] = 'You may also contact the admin'
    except Subscriber.DoesNotExist:
        confirmation_url = request.build_absolute_uri(
            reverse('blog:subscription_confirmation')) + "?token=" + token
        status = send_subscription_mail(email, confirmation_url)
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
            logger.info("Confirmation link send to " + email)
            messages.success(request, msg)
        else:
            msg = "Error while sending confirmation mail"
            messages.error(request, msg)
            message['status'] = "Error occured while sending confirmation mail"
            message['msg'] = 'Please check your input for typo'
            message['instruction'] = 'And then try again'
    except Exception as e:
        messages.error(request, e)
        logger.error(e + " occured while " + email + " was subscribing")
        message['status'] = 'Some unknown error occured'
        message['msg'] = ' Please try after some time'
        message['instruction'] = 'Meanwhile we are looking into it'
        return False
    return render(request, 'admin/status.html', {'message': message})


class ServiceWorkerView(TemplateView):
    """
    Enabling the service worker for the PWA
    """
    template_name = 'sw.js'
    content_type = 'application/javascript'
    name = 'sw.js'

    def get_context_data(self, **kwargs):
        return {
            'version': version,
            'icon_url': static('img/logo.png'),
            'manifest_url': static('manifest.json')
        }


class PostViewSet(viewsets.ModelViewSet):
    """
    View fot the Rest API
    """
    queryset = Post.published.all()
    serializer_class = PostSerializer


def search(request):
    """
    Returns the search result for the given query
    """
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


def most_viewed(request):
    """
    Returns top 9 most viewed articles
    """
    posts = Post.published.order_by('views')[:9]
    return render(request, 'index.html', {'posts': posts})


def post_list(request, tag_slug=None):
    """
    Returns top 9 published articles
    """
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
    """
    Returns the author profile
    """
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
    """
    Returns the detail view for the post
    """
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


def preview(request, id):
    """
    Returns preview of a post for the author from admin panel
    """
    if not request.user.is_staff:
        ip = get_ip(request)
        logger.warn(
            "Unauthenticated User with IP : " + str(ip) + " tried to preview post with ID : " + str(id))
        raise PermissionDenied
    post = get_object_or_404(Post, pk=id)
    if not post.author == request.user.author:
        logger.warn(str(request.user.author) +
                    " tried to preview post with ID : " + str(id))
        raise BadRequest('You must be the author of this post')
    return render(request, 'admin/preview.html', {'post': post})
