from django.db import models
from datetime import datetime    
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from functools import reduce

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=30, blank=False)
    pan = models.CharField(max_length=10,blank=True)
    gst_no = models.CharField(max_length=15,blank=True) 
    bank_details = models.TextField(max_length=128, blank=True, default='')
    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=30, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=30, blank=True)
    billing_address = models.TextField(max_length=128, blank=True, default='')
    shipping_address = models.TextField(max_length=128, blank=True, default='')
    gst_no = models.CharField(max_length=15,blank=True)
    def __str__(self):
        return self.name

class Bill (models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)    
    
    @property
    def total(self):                
        return reduce(lambda x ,y:x+y.total,self.challan_set.all(),0)
    def __str__(self):
        return "{}#{}#{}#{}".format(self.organization,self.client,self.total,self.date)

class Challan (models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)        
    date = models.DateField(default=datetime.now, blank=True)    
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)    
    @property
    def total(self):                
        return reduce(lambda x, y:x+y.total,self.job_set.all(),0)
class Job (models.Model):
    challan = models.ForeignKey(Challan, on_delete=models.CASCADE)    
    description = models.TextField(max_length=128, blank=False)
    quantity = models.IntegerField(blank=False,validators=[MinValueValidator(0)])    
    rate = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    cgst_rate = models.IntegerField(blank=False, default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
    sgst_rate = models.IntegerField(blank=False, default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
    igst_rate = models.IntegerField(blank=False, default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
    @property
    def amount(self):                
        return self.quantity*self.rate
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
        return int(self.amount + self.cgst + self.sgst + self.igst)

    def __str__(self):
        return str(self.challan)
