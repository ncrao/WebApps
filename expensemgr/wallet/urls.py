from django.conf.urls.defaults import *

urlpatterns = patterns('wallet.views',
    ('$', 'accounts.list'),
    ('accounts/$', 'accounts.list'),
)
