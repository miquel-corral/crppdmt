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

    # url to copy request
    url(r'^copy_request/(?P<expert_request_id>\d+)/$', 'crppdmt.views.copy_request', name='copy_request'),

    # url to extend request
    url(r'^extend_request/(?P<expert_request_id>\d+)/$', 'crppdmt.views.extend_request', name='extend_request'),

    # url to reject request
    url(r'^reject_request/(?P<expert_request_id>\d+)/$', 'crppdmt.views.reject_request', name='reject_request'),

    # url to new user registration page
    url(r'^user_registration/', 'crppdmt.views.user_registration', name='user_registration'),

    # url to user registration informative page
    url(r'^user_registered/', 'crppdmt.views.user_registered', name='user_registered'),

    # url to inactive users list
    url(r'^inactive_users/', 'crppdmt.views.inactive_users', name='inactive_users'),

    # url to validate / reject user form
    url(r'^validate_user/(?P<person_id>\d+)/$', 'crppdmt.views.validate_user', name='validate_user'),

    # url to candidate approval form
    url(r'^candidate_approval/(?P<expert_request_id>\d+)/$', 'crppdmt.views.candidate_approval', name='candidate_approval'),

    # url to link candidate form
    url(r'^link_candidate/(?P<expert_request_id>\d+)/$', 'crppdmt.views.link_candidate', name='link_candidate'),

    # url to expert_profile
    url(r'^expert_profile/', 'crppdmt.views_expert.expert_profile', name='expert_profile'),

    # url to upload personal info form
    url(r'^upload_personal_info/', 'crppdmt.views_expert.upload_personal_info', name='upload_personal_info'),

    # url to communication form
    url(r'^communicate/', 'crppdmt.views_expert.communicate', name='communicate'),
    url(r'^report_issue/(?P<expert_request_id>\d+)/$', 'crppdmt.views_expert.communicate', name='report_issue'),

    # url to deployment date form
    url(r'^deployment_date/(?P<expert_request_id>\d+)/$', 'crppdmt.views_expert.deployment_date', name='deployment_date'),

    # url to deployment date form
    url(r'^inception_report/(?P<expert_id>\d+)/(?P<expert_request_id>\d+)/$', 'crppdmt.views_expert.inception_report', name='inception_report'),

    # url to per form
    url(r'^per/(?P<expert_id>\d+)/(?P<expert_request_id>\d+)/$', 'crppdmt.views_expert.per', name='per'),

    #url to error page
    #url(r'^error/', 'crppdmt.views.error', name='error'),

    #url to test page
    url(r'^test/', 'crppdmt.views.test', name='test'),

    # url to admin app
    url(r'^admin/', include(admin.site.urls)),

    # Necessary to get widgets from admin running OK
    (r'^crppdmt/jsi18n/', 'django.views.i18n.javascript_catalog'),

    # url for captcha application
    url(r'^captcha/', include('captcha.urls')),
)

