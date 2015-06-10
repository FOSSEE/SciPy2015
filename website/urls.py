from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'website.views.home', name='home'),

    # ajax urls
    # url(r'^ajax/matching-books/$', 'tbc.views.ajax_matching_books', name='AjaxMatchingBooks'),

)
