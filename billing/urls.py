from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from billing.views import InvoiceView, BillUpdate
urlpatterns = [
    url(r'^$', views.signin, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^challan$', views.challan, name='challans'),
    url(r'^rate-challan$', views.rate_challan, name='rate-challan'),
    url(r'^clients$', views.clients, name='clients'),
    url(r'^bills$', views.bills, name='bills'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^generate-bill/$', InvoiceView.as_view(),name='generate-bill'),    
	url(r'^update-bill/(?P<pk>\d+)/$', BillUpdate.as_view(),name='update-bill'),
	# url(r'^pay/summary/(?P<value>\d+)/$', views.pay_summary, name='pay_summary'))
    # url(r'^generate-bill/$', views.invoice_test, name='generate-bill'),    
    # url(r'^save_challan$', views.save_challan, name='challan'),
]