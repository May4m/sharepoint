
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout


def register_user(firstname, lastname, email, password, username=None):
    if not username:
        username = email.split('@')[0]
    user = User.objects.create_user(username, email, password)
    user.firs_tname = firstname
    user.last_name = lastname
    user.save()
    return user


def change_password(username, oldpass, newpass):
    user = User.objects.get(username)
    if user.password == oldpass:
        user.set_password(newpass)
        user.save()
        return True
    return False


def authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        return User
    return None


def does_account_exist(username):
    if User.objects.get(username):
        return True
    return False

def reset_password(username):
    user = User.objects.get(username)