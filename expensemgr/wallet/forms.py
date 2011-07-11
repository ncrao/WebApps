from django import forms

from wallet.models import Account

class UploadForm(forms.Form):
    """Form to upload statement."""
    file = forms.FileField()
    account = forms.ModelChoiceField(Account.objects.all())
