from django import forms
from django.forms import ModelForm
from billing.models import Challan, Client

class ChallanForm(ModelForm):
    client_id = forms.IntegerField()
    class Meta:
        model = Challan
        fields = ['client_id','job', 'quantity']

    # def save(self, commit=True):
        
    #     return super(PointForm, self).save(commit=commit)