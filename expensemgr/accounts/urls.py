from django.conf.urls.defaults import *

login_view_args = {
    'template_name': 'accounts/login.html',
}

logout_view_args = {
    'next_page': '/accounts/login/',
}

urlpatterns = patterns('',
    ('^login/$', 'django.contrib.auth.views.login', login_view_args),
    ('^logout/$', 'django.contrib.auth.views.logout', logout_view_args),
    ('^profile/$', 'accounts.views.profile'),
    ('^register/$', 'accounts.views.register'),
)
