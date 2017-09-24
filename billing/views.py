from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from billing.forms import ChallanForm, ClientForm, RateForm
from billing.models import Client, Organization, Challan, Bill
from django.http import JsonResponse
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

def clients(request):    
    if not request.user.is_authenticated:
        return redirect('login')
    form = ClientForm(request.POST or None)
    if request.method == 'POST':    
        if form.is_valid():                    
            client = form.save(commit=False)            
            client.organization = request.user.organization
            client.save()
    clients = Client.objects.filter(organization=request.user.organization)    
    return render(request, 'billing/clients.html',{'clients': clients, 'form':form})

# @csrf_exempt
def challan(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = ChallanForm(request.POST or None)
    if request.method == 'POST':    
        if form.is_valid():                    
            challan = form.save(commit=False)            
            challan.organization = request.user.organization
            challan.save()
    form.fields['client'].queryset = Client.objects.filter(organization=request.user.organization)
    rate_form = RateForm()
    rate_form.fields['challan'].queryset = Challan.objects.filter(organization=request.user.organization, rate=None)
    challans = Challan.objects.filter(organization=request.user.organization)   
    print(challans) 
    return render(request, 'billing/challans.html',context={'challans': challans,'form':form, 'rate_form':rate_form})

@csrf_exempt
def rate_challan(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error':True, 'msg':'You need to login first'})
    print(request.POST)
    if request.method == 'POST':    
        if request.POST['rate'] and request.POST['id']:            
            challan = Challan.objects.get(id=int(request.POST['id']))            
            challan.rate = int(request.POST['rate'])
            challan.save()            
    return JsonResponse({'error':False, 'msg':'Success!'})


def bills(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':    
        pending_challans = Challan.objects.filter(organization=request.user.organization, bill=None).exclude(rate=None)
        client_challans = {}        
        for challan in pending_challans:
            if not challan.client in client_challans:
                client_challans[challan.client] = []
            client_challans[challan.client].append(challan)
        for client, challans in client_challans.items():            
            amount = sum ([c.quantity*c.rate for c in challans])
            bill = Bill.objects.create(organization=request.user.organization, client=client, amount=amount)
            for c in challans:                
                c.bill = bill 
                c.save()           

    bills = Bill.objects.filter(organization=request.user.organization)    
    return render(request, 'billing/bills.html',context={'bills': bills})
