from django.contrib import admin
from .models import *

class AddUsersAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'membership_start_date','membership_end_date']
	search_fields = ['first_name','last_name']

class GenerateInvoiceAdmin(admin.ModelAdmin):
	list_display = ['customer_name','purchased_date','grand_total']
	search_fields = ['customer_name','purchased_date']

class GenerateItemsAdmin(admin.ModelAdmin):
	list_display = ['customer_name', 'item_name', 'item_quantity','item_amount']

admin.site.register(AddUsers,AddUsersAdmin)
admin.site.register(GenerateInvoice,GenerateInvoiceAdmin)
admin.site.register(GenerateItems,GenerateItemsAdmin)
