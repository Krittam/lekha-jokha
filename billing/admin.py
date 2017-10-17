from django.contrib import admin
from billing.models import Client, Challan ,Bill, Organization,Job

# Register your models here.
admin.site.register(Client)
admin.site.register(Challan)
admin.site.register(Bill)
admin.site.register(Organization)
admin.site.register(Job)
