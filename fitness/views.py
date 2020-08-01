from django.shortcuts import render
from .models import AddUsers
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
import datetime
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from fitness.utils import render_to_pdf
from .forms import GenerateInvoiceForm,AddUsersForm


class HomeView(TemplateView):
	template_name = "base.html"


class AddUsersCreate(CreateView):
	model = AddUsers
	form_class = AddUsersForm
	template_name = 'add_users.html'

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
	form_class = AddUsersForm
	template_name = "add_users.html"
	# fields = '__all__'
	success_url ="/"

	def get_success_url(self):
		return reverse_lazy('home')


class UsersDeleteView(DeleteView):
	model = AddUsers
	template_name = "users_delete.html"

	def get_success_url(self):
		return reverse_lazy('list')

def get_alerts(request):
	before_5_days = timezone.now() + timedelta(days=5)
	print(before_5_days,'before_5_days')
	posts = AddUsers.objects.filter(membership_end_date__gte= before_5_days).order_by('membership_start_date')
	return render(request,'alerts.html',{'posts':posts})

def generate_invoice(request):
	if request.method == "POST":
		form = GenerateInvoiceForm(request.POST)
		if form.is_valid():
			form.save()
			customer_name = form.cleaned_data['customer_name']
			item_name = form.cleaned_data['item_name']
			item_quantity = form.cleaned_data['item_quantity']
			item_amount = form.cleaned_data['item_amount']
			item_date = form.cleaned_data['item_date']
			total_amount = float(item_quantity)*float(item_amount)
			data = {
			'customer_name':customer_name,
			'item_name':item_name,
			'item_quantity':item_quantity,
			'item_amount':item_amount,
			'item_date':item_date,
			'total_amount':total_amount,
			}
			pdf = render_to_pdf('invoice.html', data)
			return HttpResponse(pdf, content_type='application/pdf')
	else:
		form = GenerateInvoiceForm()
	return render(request,'generate_invoice.html',{'form':form})
