from django.conf.urls import patterns, include, url
from django.contrib import admin
from crppdmt.settings import STATIC_ROOT
from django.contrib import auth
import django.views.i18n

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crppdmt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url to form login
    url(r'^accounts/login/$', 'crppdmt.views.my_login', name="my_login"),

    # url to logout page
    url(r'^logout/$', 'crppdmt.views.my_logout', name='logout'),

    # url to change password
    url(r'^accounts/change_password/$', 'crppdmt.views.my_change_password', name='my_change_password'),

    # urls to manage the forgot password link
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),

    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',name='password_reset_complete'),
    #(r'^admin/(.*)', admin.site.root),

    # base url
    url(r'^$', 'crppdmt.views.index', name='index'),

    # url to index page
    url(r'^index/', 'crppdmt.views.index', name='index'),

    # url to my_copyright page
    url(r'^my_copyright/$', 'crppdmt.views.my_copyright', name='my_copyright'),

    # url to request edit page
    url(r'^request/(?P<request_id>\d+)/$', 'crppdmt.views.edit_request', name='edit_request'),

    # url to new request page
    url(r'^create_request/', 'crppdmt.views.create_request', name='new_request'),

    #url to generate letter of request#  PDF
    url(r'^letter_of_request_pdf/(?P<expert_request_id>\d+)/$', 'crppdmt.views.generate_letter_of_request_pdf', name='generate_letter_pdf'),

    #url to generate ToR PDF
    url(r'^tor_pdf/(?P<expert_request_id>\d+)/$', 'crppdmt.views.generate_tor_pdf', name='generate_tor_pdf'),

    #url to retrieve file from ftp
    url(r'^retrieve_file/(?P<remote_folder>[^/]+)/(?P<remote_file>[^/]+)/', 'crppdmt.views.retrieve_file', name='retrieve_file'),

    # url to general checklist page
    url(r'^general_checklist/(?P<action>[^/]+)/(?P<expert_request_id>\d+)/$', 'crppdmt.views.general_checklist', name='general_checklist'),

    # url to summary checklist page
    url(r'^summary_checklist/(?P<expert_request_id>\d+)/$', 'crppdmt.views.summary_checklist', name='summary_checklist'),

    # url for static files
    #url(r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),


    # url entries for registration app
    #(r'^accounts/', include('registration.urls')),

    #url to error page
    #url(r'^error/', 'crppdmt.views.error', name='error'),

    #url to test page
    url(r'^test/', 'crppdmt.views.test', name='test'),

    # url to admin app
    url(r'^admin/', include(admin.site.urls)),

    # Necessary to get widgets from admin running OK
    (r'^crppdmt/jsi18n/', 'django.views.i18n.javascript_catalog'),
)

