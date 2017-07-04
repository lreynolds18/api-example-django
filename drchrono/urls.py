from django.conf.urls import include, url
from django.views.generic import TemplateView
# from django.views.generic.simple import redirect_to
import views


urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # url(r'^index/$', views.index, name="index"),
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login, name="login"),
    url(r'^success/$', views.success, name="success"),
    url(r'^accounts/profile/$', views.success, name="index"),
    url(r'^complete/drchrono/$', views.drchrono, name="i"),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
