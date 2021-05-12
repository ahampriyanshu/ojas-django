from django.dispatch import receiver
from django.db.models import signals
from .models import Post, Subscriber
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.conf import settings


@receiver(signals.post_save, sender=Post)
def send_mail(sender, instance, created, **kwargs):
    if  instance.status.lower() == "published":
        domain = settings.ALLOWED_HOSTS[0]
        subscribers = Subscriber.objects.filter(confirmed = True)
        for subscriber in subscribers.iterator():
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
                print("Mail successfully sent")
            except Exception as e:
                print(e)