from django import forms
from .models import AddUsers,GenerateInvoice


class AddUsersForm(forms.ModelForm):
	class Meta:
		model = AddUsers
		fields = '__all__'

class GenerateInvoiceForm(forms.ModelForm):
	class Meta:
		model = GenerateInvoice
		fields = '__all__'
