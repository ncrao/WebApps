from django.shortcuts import render
from django.views.generic.create_update import create_object
from django.views.generic.create_update import update_object
from django.views.generic.create_update import delete_object
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.core.urlresolvers import reverse

from wallet.models import Account

def list(request):
    """List all accounts."""
    queryset = Account.objects.all()
    return object_list(request, queryset=queryset,
                       template_name='account/list.html')

def detail(request, object_id):
    """Show account details."""
    queryset = Account.objects.all()
    return object_detail(request, queryset=queryset, object_id=object_id,
                         template_name='account/detail.html',
                         template_object_name='account')

def update(request, object_id):
    """Update account."""
    return update_object(request, model=Account, object_id=object_id,
                         template_name='account/create_update.html')

def create(request):
    """Create account."""
    return create_object(request, model=Account,
                         template_name='account/create_update.html')

def delete(request, object_id):
    """Delete account."""
    return delete_object(request, model=Account, object_id=object_id,
                         post_delete_redirect=reverse('wallet.views.account.list'),
                         template_object_name='account',
                         template_name='account/delete.html')
