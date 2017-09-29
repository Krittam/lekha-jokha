from django.db import models
from datetime import datetime    
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=30, blank=False)
    pan = models.CharField(max_length=10,blank=True)
    gst_no = models.CharField(max_length=15,blank=True)    

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=30, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=False)
    gst_no = models.CharField(max_length=15,blank=True)
    def __str__(self):
        return self.name

class Bill (models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    cgst_rate = models.IntegerField(blank=False, default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
    sgst_rate = models.IntegerField(blank=False, default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
    igst_rate = models.IntegerField(blank=False, default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
    @property
    def amount(self):                
        return sum ([ch.quantity*ch.rate for ch in self.challan_set.all()])
    @property
    def cgst(self):                
        return int(self.amount *(self.cgst_rate/100))
    @property
    def sgst(self):                
        return int(self.amount *(self.sgst_rate/100))
    @property
    def igst(self):                
        return int(self.amount *(self.igst_rate/100))
    @property
    def total(self):                
        return self.amount + self.cgst + self.sgst + self.igst
    def __str__(self):
        return "{}#{}#{}#{}".format(self.organization,self.client,self.amount,self.date)

class Challan (models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    job = models.TextField(max_length=128, blank=False)
    quantity = models.IntegerField(blank=False,validators=[MinValueValidator(0)])
    date = models.DateField(default=datetime.now, blank=True)
    rate = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return "{}#{}#{}#{}#{}#{}#{}".format(self.organization,self.client,self.job,self.quantity,self.rate,self.date,self.bill)
