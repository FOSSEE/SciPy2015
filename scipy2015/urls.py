from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scipy2015.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^2015/', include('website.urls', namespace='website')),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('django.contrib.auth.urls', namespace='auth')),
)
