from django.conf.urls import patterns, include, url
from boxes.views import BoxListView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'archiver1.views.home', name='home'),
    # url(r'^archiver1/', include('archiver1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'employee.views.LoginRequest'),
    url(r'^logout/$', 'employee.views.LogoutRequest'),

    url(r'^single/$', 'boxes.views.Single'),
    url(r'^batch/$', 'boxes.views.Batch'),
    url(r'^batch2/$', 'boxes.views.Batch2'),
    url(r'^archive/$', 'boxes.views.Archive'),
    url(r'^archive2/$', 'boxes.views.Archive2'),
    url(r'^view/$', 'boxes.views.BoxList'),
    url(r'^view/(?P<slug>\w+)/(?P<box_number>\d+)/$', BoxListView.as_view()),
)
