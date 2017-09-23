from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.signin, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^challan$', views.challan, name='challan'),
    # url(r'^save_challan$', views.save_challan, name='challan'),
]