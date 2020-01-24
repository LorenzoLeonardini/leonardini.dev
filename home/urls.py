from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    url(r'^contact/', views.contact, name='contact'),
    url(r'^', views.index, name='index'),
]
