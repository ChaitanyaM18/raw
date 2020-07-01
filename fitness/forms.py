from django import forms 
from .models import AddUsers


class AddUsersForm(forms.ModelForm):
	class Meta:
		model = AddUsers
		fields = '__all__'