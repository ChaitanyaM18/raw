from django import forms
from .models import AddUsers,GenerateInvoice
from django.forms import modelformset_factory

class DateInput(forms.DateInput):
    input_type = 'date'

class AddUsersForm(forms.ModelForm):
	class Meta:
		model = AddUsers
		fields = '__all__'
		widgets = {
            'date_of_birth': DateInput(),
			'membership_start_date':DateInput(),
			'membership_end_date':DateInput(),
        }

class GenerateInvoiceForm(forms.ModelForm):
    class Meta:
        model = GenerateInvoice
        fields = '__all__'
        widgets = {
            'item_date': DateInput(),
        }
