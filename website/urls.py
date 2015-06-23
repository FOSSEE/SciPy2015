from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'website.views.home', name='home'),
    url(r'^cfp/$', 'website.views.cfp', name='cfp'),
)
