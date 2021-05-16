from django.dispatch import receiver
from django.db.models import signals
from .models import Post, Subscriber
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
import logging, traceback


@receiver(signals.post_save, sender=Post)
def send_mail(sender, instance, created, **kwargs):
    reader_notified = 0
    domain = settings.ALLOWED_HOSTS[0]
    readers = Subscriber.objects.filter(confirmed = True)
    total_readers = readers.count()
    if not instance.notified and instance.status.lower() == "published":
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
                print("Newsletter send to" + email)
            except Exception as e:
                print(e)
    if reader_notified == total_readers:
        print("All " + str(total_readers) + " readers notified successfully")
    else:
        print("All " + str(total_readers) + " readers couldn't be notified")