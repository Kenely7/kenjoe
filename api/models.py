from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender,instance,reset_password_token,**args):
    email_plaintext_message ='{}?token={}'.format(reverse('password_reset:reset-password-request'),reset_password_token.key)
    send_mail(
     #Title
     "Password Reset for{title}".format(title = 'Kenjoe'),
     #message
     email_plaintext_message,
     # from
     "noreply@homehost.local",
     # to
     [reset_password_token.user.email]

    )