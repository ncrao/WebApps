from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=200)

class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    description = models.CharField(max_length=200)
    account = models.ForeignKey(Account)
