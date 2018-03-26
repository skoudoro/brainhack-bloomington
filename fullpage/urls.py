from django.conf.urls import url
from fullpage import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
