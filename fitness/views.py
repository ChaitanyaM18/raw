from django.shortcuts import render
from .models import AddUsers,GenerateInvoice
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
from django.db import transaction
import pandas as pd

from .forms import GenerateInvoiceForm,AddUsersForm,ItemFormSet, CollectionForm


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

class GenerateInvoiceView(CreateView):
    model = GenerateInvoice
    template_name = 'generate_invoice.html'
    form_class = CollectionForm
    success_url = None

    '''formset to choose signal types and respective description'''

    def get_context_data(self, **kwargs):
        data = super(GenerateInvoiceView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = ItemFormSet(self.request.POST)
        else:
            data['titles'] = ItemFormSet()
        return data

    def form_valid(self, form):
	    context = self.get_context_data()
	    titles = context['titles']
	    dict_df = pd.DataFrame(columns=['item_name', 'item_quantity','item_amount'])
	    with transaction.atomic():
		    self.object = form.save()
		    if titles.is_valid():
			    titles.instance = self.object
			    titles.save()
			    customer_name = form.cleaned_data['customer_name']
			    item_date = form.cleaned_data['purchased_date']
			    for data in titles.cleaned_data:
				    item_name = data.get('item_name')
				    item_quantity = data.get('item_quantity')
				    item_amount = data.get('item_amount')
				    dict_df = dict_df.append({'item_name': str(data.get('item_name')), 'item_quantity': str(data.get('item_quantity')),'item_amount': str(data.get('item_amount'))}, ignore_index=True)
			    dict_df.to_csv('dict_df.csv')
			    print(customer_name)
				# total_amount = float(item_quantity)*float(item_amount)
			    data = {
			    'customer_name':customer_name,
			    'item_name':item_name,
			    'item_quantity':item_quantity,
			    'item_amount':item_amount,
			    'item_date':item_date,
				# 'total_amount':total_amount,
			    }
			    pdf = render_to_pdf('invoice.html', data)
			    return HttpResponse(pdf, content_type='application/pdf')
	    return super(GenerateInvoiceView, self).form_valid(form)
