from django import forms
from .models import AddUsers,GenerateInvoice,GenerateItems
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django.forms.models import inlineformset_factory
from .custom_obj import *



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
        model = GenerateItems
        fields = '__all__'
        widgets = {
            'purchased_date': DateInput(),
        }

ItemFormSet = inlineformset_factory(
    GenerateInvoice,GenerateItems, form=GenerateInvoiceForm, fields=[
        'item_name', 'item_quantity','item_amount'], extra=1, can_delete=True)

class CollectionForm(forms.ModelForm):

    class Meta:
        model = GenerateInvoice
        fields = '__all__'
        widgets = {
            'purchased_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('customer_name'),
                Field('purchased_date'),
                Field('customer_address'),
                Fieldset('Add Particulars',
                    Formset('titles')),
                Field('note'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
                )
            )
