from django.conf.urls.defaults import *

urlpatterns = patterns('wallet.views',
    ('^account/list$', 'account.list'),
    ('^account/create$', 'account.create'),
    ('^account/detail/(?P<object_id>\d+)/$', 'account.detail'),
    ('^account/delete/(?P<object_id>\d+)/$', 'account.delete'),
    ('^account/update/(?P<object_id>\d+)/$', 'account.update'),
    ('^transaction/list$', 'transaction.list'),
    ('^transaction/create$', 'transaction.create'),
    ('^transaction/detail/(?P<object_id>\d+)/$', 'transaction.detail'),
    ('^transaction/delete/(?P<object_id>\d+)/$', 'transaction.delete'),
    ('^transaction/update/(?P<object_id>\d+)/$', 'transaction.update'),
    ('^upload/$', 'upload.upload_statement'),
)
