from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from billing.forms import ChallanForm, ClientForm, RateForm, OrganizationForm
from billing.models import Client, Organization, Challan, Bill
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from easy_pdf.views import PDFTemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse


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
    return render(request, 'billing/challans.html',context={'challans': challans,'form':form, 'rate_form':rate_form})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = OrganizationForm(request.POST or None,instance=request.user.organization)
    if request.method == 'POST':    
        if form.is_valid():                    
            form.save()                                
    return render(request, 'billing/profile.html',context={'form':form})

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
        else:
           JsonResponse({'error':True, 'msg':'Please enter a correct rate!'})             
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
            bill = Bill.objects.create(organization=request.user.organization, client=client)
            for c in challans:                
                c.bill = bill 
                c.save()           

    bills = Bill.objects.filter(organization=request.user.organization)    
    return render(request, 'billing/bills.html',context={'bills': bills})

class InvoiceView(PDFTemplateView):    
    template_name = 'billing/invoice.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InvoiceView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        bill = Bill.objects.get(id=self.request.GET['id'])
        if not bill.organization==self.request.user.organization:
            return None
        organization = bill.organization
        context['organization'] = organization.name 
        context['pan'] = organization.pan
        context['gst_no'] = organization.gst_no
        context['bill'] = bill
        return context

def invoice_test(request):
    if not request.user.is_authenticated:
        return redirect('login')
    bill = Bill.objects.get(id=request.GET['id'])
    if not bill.organization==request.user.organization:
        return None
    organization = bill.organization
    context = {}
    context['organization'] = organization.name 
    context['pan'] = organization.pan
    context['gst_no'] = organization.gst_no
    context['bill'] = bill
    
    bills = Bill.objects.filter(organization=request.user.organization)    
    return render(request, 'billing/invoice.html',context=context)

class BillUpdate(UpdateView):
    model = Bill
    fields = ['cgst_rate','sgst_rate', 'igst_rate']
    template_name_suffix = '_update_form'
    def get_success_url(self):
            return reverse('update-bill', kwargs={'pk': self.object.id})    
    def get_context_data(self, **kwargs):
        context = super(BillUpdate, self).get_context_data(**kwargs)
        context['bill'] = self.object        
        context['challans'] = self.object.challan_set.all()
        context['date'] = self.object.date
        return context

