from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^quotes$', views.quotes),
    url(r'^login$', views.login),
    url(r'^log_out$', views.log_out),
    url(r'^add_quote$', views.add_quote),
    url(r'^quote/(?P<quote_id>\d+)$', views.add_favorite),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove_favorite),
    url(r'^users/(?P<user_id>\d+)$', views.view_user),
]