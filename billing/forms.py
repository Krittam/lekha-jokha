from django import forms
from django.forms import ModelForm
from billing.models import Challan, Client, Organization, Bill, Job

class ChallanForm(ModelForm):  
    
    class Meta:
        model = Challan
        fields = ['date','client']

class RateForm(ModelForm):  
    challan = forms.ChoiceField(required=True)  
    rate = forms.IntegerField(required=True)
    class Meta:
        model = Challan
        fields = ['challan','rate']

class ClientForm(ModelForm):    
    billing_address = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}))  
    shipping_address = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}))  
    class Meta:
        model = Client
        fields = ['name','contact_person', 'gst_no', 'billing_address', 'shipping_address']

class JobForm(ModelForm):    
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}))  
    class Meta:
        model = Job
        fields=['description','quantity','rate','cgst_rate','sgst_rate','igst_rate']

class OrganizationForm(ModelForm):    
    bank_details = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}))  
    address = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}))  
    class Meta:
        model = Organization
        fields=['name','pan','gst_no','address','bank_details']


