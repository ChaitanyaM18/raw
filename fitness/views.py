from django.shortcuts import render
from .models import AddUsers
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



class HomeView(TemplateView):
	template_name = "base.html"

class AddUsersCreate(CreateView):
	model = AddUsers
	template_name = 'add_users.html'
	fields = '__all__'

	def get_success_url(self):
		return reverse_lazy('list')

class UsersListView(ListView):
	model = AddUsers
	template_name = 'users_list.html'

	def get_context_data(self, **kwargs):
		context = super(UsersListView, self).get_context_data(**kwargs)
		return context

class UsersUpdateView(UpdateView):
	model = AddUsers
	template_name = "add_users.html"
	fields = '__all__'
	success_url ="/"

	def get_success_url(self):
		return reverse_lazy('home')

class UsersDeleteView(DeleteView):
	model = AddUsers
	template_name = "users_delete.html"

	def get_success_url(self):
		return reverse_lazy('list')
