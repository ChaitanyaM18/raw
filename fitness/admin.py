from django.contrib import admin
from .models import *

class AddUsersAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'membership_start_date','membership_end_date']

admin.site.register(AddUsers,AddUsersAdmin)
