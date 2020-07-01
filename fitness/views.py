from django.shortcuts import render
from .models import AddUsers
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy



class HomeView(TemplateView):
	template_name = "base.html"

class AddUsersCreate(CreateView):
	model = AddUsers
	template_name = 'add_users.html'
	fields='__all__'
	# success_url = None

	def get_success_url(self):
		return reverse_lazy('home')
