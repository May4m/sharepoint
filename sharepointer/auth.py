from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages

from django.core.mail import send_mail
from django.core.validators import validate_email

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.shortcuts import loader


# setup email
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'codegeek77@gmail.com'
SERVER_EMAIL = 'codegeek77@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'codegeek77@gmail.com'
EMAIL_HOST_PASSWORD = 'sizwE123$'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


def register_user(firstname, lastname, email, password):
    user = User.objects.create_user(email, email, password)
    user.first_name = firstname
    user.last_name = lastname
    user.save()
    return user


def change_password(email, oldpass, newpass):
    user = User.objects.get(email=email)
    if user.password == oldpass:
        user.set_password(newpass)
        user.save()
        return True
    return False


def authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    return user if user else False


def does_account_exist(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        user = None


def reset_password(request, cred):
    user = does_account_exist(cred)
    if user:
        c = {
            'email': user.email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'your site',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
            }
        subject_template_name='password_reset_subject.txt' 
        email_template_name='password_reset_email.html'    
        subject = loader.render_to_string(subject_template_name, c)
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
        return True
    return False