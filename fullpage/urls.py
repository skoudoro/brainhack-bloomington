from django.conf.urls import url
from fullpage import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registration/$', views.registration, name='registration')
]
