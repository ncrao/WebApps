from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from wallet.forms import UploadForm
from wallet.parser.base import ParserFactory
from wallet.models import Account

def upload_statement(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            account = Account.objects.get(id=form['account'].value())
            # parse data and add transactions here
            data = request.FILES['file'].read()
            parser = ParserFactory(account.parser, data, account)
            txn_list = parser.parse()
            for txn in txn_list:
                txn.account = account
                txn.save()
            account.save()
            return HttpResponseRedirect(reverse(
                'wallet.views.upload.upload_statement'))
    else:
        form = UploadForm()

    return render_to_response('wallet/upload.html', {
        'form': form,
    })
