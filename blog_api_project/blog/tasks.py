import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def log_user_registered(email):
    """
    Пример 1: обычная фоновая задача, вызывается через .delay().
    Логирует факт регистрации пользователя.
    """
    message = f'[Celery] Пользователь зарегистрирован: {email}'
    logger.info(message)
    print(message)
    return message


@shared_task
def cleanup_unpublished_posts():
    """
    Пример 2: периодическая задача (crontab через Celery Beat).
    Удаляет неопубликованные посты старше 7 дней.
    """
    from .models import Post

    threshold = timezone.now() - timedelta(days=7)
    deleted_count, _ = Post.objects.filter(
        is_published=False,
        created_at__lt=threshold,
    ).delete()
    message = f'[Celery Beat] Удалено неопубликованных постов: {deleted_count}'
    logger.info(message)
    print(message)
    return {'deleted': deleted_count}


@shared_task
def send_confirmation_email(email, code):
    """
    Пример 3: задача с SMTP.
    Отправляет код подтверждения на email пользователя.
    """
    subject = 'Код подтверждения аккаунта'
    message = (
        f'Ваш код подтверждения: {code}\n'
        f'Код действует 5 минут.'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    result = f'[Celery SMTP] Письмо отправлено на {email}'
    logger.info(result)
    print(result)
    return result
