from django import forms
from django.forms import ModelForm
from billing.models import Challan, Client

class ChallanForm(ModelForm):  
    job = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}))  
    class Meta:
        model = Challan
        fields = ['date','client','job', 'quantity','rate']

class RateForm(ModelForm):  
    challan = forms.ChoiceField(required=True)  
    class Meta:
        model = Challan
        fields = ['challan','rate']

class ClientForm(ModelForm):    
    class Meta:
        model = Client
        exclude = ['organization']

    # def save(self, commit=True):
        
    #     return super(PointForm, self).save(commit=commit)