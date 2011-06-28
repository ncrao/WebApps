from django.db import models
from django.core.urlresolvers import reverse

class Account(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __get_url_for(self, viewname):
        kwargs = {
            'object_id': self.id,
        }
        return reverse(viewname, kwargs=kwargs)

    def get_absolute_url(self):
        return self.__get_url_for('wallet.views.account.detail')

    def get_update_url(self):
        return self.__get_url_for('wallet.views.account.update')

    def get_delete_url(self):
        return self.__get_url_for('wallet.views.account.delete')

class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    description = models.CharField(max_length=200)
    account = models.ForeignKey(Account)

    def __unicode__(self):
        # TODO: should this be float?
        return 'TXN: %s' % self.amount

    def __get_url_for(self, viewname):
        kwargs = {
            'object_id': self.id,
        }
        return reverse(viewname, kwargs=kwargs)

    def get_absolute_url(self):
        return self.__get_url_for('wallet.views.transaction.detail')

    def get_update_url(self):
        return self.__get_url_for('wallet.views.transaction.update')

    def get_delete_url(self):
        return self.__get_url_for('wallet.views.transaction.delete')
