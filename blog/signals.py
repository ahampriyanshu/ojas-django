from django.dispatch import receiver
from django.db.models import signals
from .models import Post, Subscriber
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
import logging, traceback
logger = logging.getLogger(__name__)


@receiver(signals.post_save, sender=Post)
def send_mail(sender, instance, created, **kwargs):
    """
    Notify all the subscribers(readers) when a new post is published
    """
    reader_notified = 0
    domain = settings.ALLOWED_HOSTS[0]
    readers = Subscriber.objects.filter(confirmed = True)
    total_readers = readers.count()
    if not instance.notified and instance.status.lower() == "published":
        logger.debug("Notiying " + str(total_readers) +" readers for the article : " +instance.title)
        for subscriber in readers.iterator():
            token = subscriber.token
            email = subscriber.email
            unsubsrcibe_url = domain + '/unsubscribe/' + "?token=" + token + "&email=" + email
            ctx = {
                'post_url':domain + instance.get_absolute_url(),   
                'title': instance.title,
                'body': instance.body,
                'unsubsrcibe_url': unsubsrcibe_url,
                'domain' : domain,
                'logo_url': settings.LOGO_URL,
            }
            message = get_template('newsletter.html').render(ctx)
            msg = EmailMessage(
                instance.title,
                message,
                'ahampriyanshu@gmail.com',
                [email],
            )
            msg.content_subtype = "html"
            try:
                msg.send()
                instance.notified = True
                instance.save()
                reader_notified += 1
                logger.info("Notified " + email + " successfully")
            except Exception as e:
                logger.error("Error ocuured while notiying" + email + " : " + e)
        if reader_notified == total_readers:
            logger.info("All " + str(total_readers) + " readers have been notified successfully")
        else:
            logger.warn("All " + str(total_readers) + " readers couldn't be notified")