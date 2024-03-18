from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from company.models import Users


@shared_task
def send_invitation_email_task(user_id):
    user = Users.objects.get(pk=user_id)
    registration_url = reverse('invite-registration') + f'?token={user.invite_token}'
    message = f"Link to complete the registration: {registration_url}"
    send_mail(
        'Registration invite',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


@shared_task
def send_password_reset_email_task(email, reset_link):
    send_mail(
        'Password reset',
        f'To reset your password, follow the link: {reset_link}',
        'from@example.com',
        [email],
        fail_silently=False,
    )
