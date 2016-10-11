

from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'$^', views.index, name='index'),
    url(r'^register', views.AuthCenter.register, name='register'),
    url(r'^login', views.AuthCenter.login, name="login"),
    url(r'^logout', views.AuthCenter.logout, name='logout'),
    url(r'^validate_login', views.AuthCenter.validate_login, name='validate_login0'),
    url(r'^forgotpassword', views.AuthCenter.forgot_password, name='forgot_password'),
    url(r'^changepassword', views.AuthCenter.change_password, name='change_password'),
    url(r'^verifyaccount', views.AuthCenter.verify_account, name='verify_account'),
    url(r'^does_user_exist', views.AuthCenter.does_user_exist),
    url(r'^home', views.home, name="home"),

]