from django.db import models
from datetime import datetime    

from django.contrib.auth.models import User

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=500, blank=False)
    address = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=30, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=False)
    def __str__(self):
        return self.name

class Bill (models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(blank=False)
    def __str__(self):
        return "{}#{}#{}#{}".format(self.organization,self.client,self.amount,self.date)

class Challan (models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    job = models.TextField(max_length=128, blank=False)
    quantity = models.IntegerField(blank=False)
    date = models.DateField(default=datetime.now, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return "{}#{}#{}#{}#{}#{}#{}".format(self.organization,self.client,self.job,self.quantity,self.rate,self.date,self.bill)
