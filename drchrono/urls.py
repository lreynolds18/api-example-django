from django.conf.urls import include, url
from django.views.generic import TemplateView
# from django.views.generic.simple import redirect_to
import views


urlpatterns = [
    url(r'^$', views.login, name="login"),
    url(r'^drchrono/$', views.drchrono, name="home"),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
