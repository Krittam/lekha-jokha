from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from billing.forms import ChallanForm
from billing.models import Client, Organization

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':          
        if form.is_valid():                    
            user = form.save()
            organization = Organization.objects.create(name=request.POST['organization'],address=request.POST['address'],user=user)            
            login(request, user)
            return redirect('dashboard')        
    return render(request, 'billing/register.html',context={'form':form})

@csrf_exempt
def signin(request):  
    form = AuthenticationForm(data=request.POST or None)     
    if request.method == 'POST':    
        if form.is_valid():         
            login(request, form.get_user())
            return redirect('dashboard')        
    return render(request, 'billing/login.html',context={'form':form})

def dashboard(request):    
    if not request.user.is_authenticated:
        return redirect('login')        
    return render(request, 'billing/dashboard.html')

# def add_challan(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     form = ChallanForm()
#     return render(request, 'billing/challan_form.html',{'form':form})

# @csrf_exempt
def challan(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = ChallanForm(request.POST or None)
    if request.method == 'POST':    
        if form.is_valid():        
            client = Client.objects.filter(id=form.data['client_id']).first()        
            challan = form.save(commit=False)
            challan.client = client
            challan.organization = User.objects.get(id=1).organization
            challan.save()
    return render(request, 'billing/challan_form.html',context={'form':form})