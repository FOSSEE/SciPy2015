from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'website.views.home', name='home'),
    url(r'^cfp/$', 'website.views.cfp', name='cfp'),
    url(r'^submit-cfp/$', 'website.views.submitcfp', name='submitcfp'),
    url(r'^accounts/register/$', 'website.views.userregister', name='userregister'),
    url(r'^accounts/login/$', 'website.views.userlogin', name='userlogin'),
    url(r'^accounts/forgot-password/$', 'website.views.forgotpassword', name='forgotpassword'),
    url(r'^accounts/update-password/$', 'website.views.updatepassword', name='updatepassword'),
)
