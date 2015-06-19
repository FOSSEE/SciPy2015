from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'website.views.home', name='home'),
    url(r'^contact/', 'website.views.contact', name='contact'),
)
