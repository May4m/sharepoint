

from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'$^', views.index, name='index'),
    url(r'^register', views.register, name='regitser'),
    url(r'^login', views.login, name="login")
]