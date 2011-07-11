from django.shortcuts import render
from django.views.generic.create_update import create_object
from django.views.generic.create_update import update_object
from django.views.generic.create_update import delete_object
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.core.urlresolvers import reverse

from wallet.models import Transaction

def list(request):
    """List all transactions."""
    queryset = Transaction.objects.all()
    # TODO: filter transactions
    return object_list(request, queryset=queryset,
                       template_name='wallet/transaction/list.html')

def detail(request, object_id):
    """Show transaction details."""
    queryset = Transaction.objects.all()
    return object_detail(request, queryset=queryset, object_id=object_id,
                         template_name='wallet/transaction/detail.html',
                         template_object_name='transaction')

def update(request, object_id):
    """Update transaction."""
    return update_object(request, model=Transaction, object_id=object_id,
                         template_name='wallet/transaction/create_update.html')

def create(request):
    """Create transaction."""
    return create_object(request, model=Transaction,
                         template_name='wallet/transaction/create_update.html')

def delete(request, object_id):
    """Delete transaction."""
    return delete_object(request, model=Transaction, object_id=object_id,
                         post_delete_redirect=reverse('wallet.views.transaction.list'),
                         template_object_name='transaction',
                         template_name='wallet/transaction/delete.html')
