from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ad


@receiver(post_save, sender=Ad)
def ad_created(instance, created, **kwargs):
    if not created:
        return
    emails = User.objects.filter(
    ).values_list('email', flat=True)
    subject = f'Новое объявление на портале MMORPG'

    text_content = (
        f'В категории: {instance.category}\n'
        f'Новое объявление: {instance.text}\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'В категории: {instance.category}<br>'
        f'Новое объявление: {instance.text}<br>'

        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на объявление</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
