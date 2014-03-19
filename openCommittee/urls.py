from django.conf.urls import patterns, include, url
from committeeVotes import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'openCommittee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


    url(r'^$', views.index, name='index'),
    url(r'^(?P<bill_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<bill_id>\d+)/results/$', views.results, name='results'),
    url(r'^(?P<bill_id>\d+)/vote/$', views.vote, name='vote'),
)
