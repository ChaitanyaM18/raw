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
from django.db.models import Q
from .forms import GenerateInvoiceForm,AddUsersForm,ItemFormSet, CollectionForm
import pdfkit
import json
from jsonmerge import merge
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomeView(TemplateView):
	template_name = "base.html"


class AddUsersCreate(CreateView):
	model = AddUsers
	form_class = AddUsersForm
	template_name = 'add_users.html'

	def get_success_url(self):
		return reverse_lazy('filter')


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
		return reverse_lazy('filter')

def get_alerts(request):
	before_5_days = timezone.now().date() + timedelta(days=5)
	posts = AddUsers.objects.filter(Q(membership_end_date = before_5_days)).order_by('membership_start_date')
	return render(request,'alerts.html',{'posts':posts})

class GenerateInvoiceView(CreateView):
    model = GenerateInvoice
    template_name = 'generate_invoice.html'
    form_class = CollectionForm
    # success_url = None

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
			    titles.save(commit=False)
			    customer_name = form.cleaned_data['customer_name']
			    item_date = form.cleaned_data['purchased_date']
			    customer_address = form.cleaned_data['customer_address']
			    # grand_total = 0
			    for data in titles.cleaned_data:
				    item_name = data.get('item_name')
				    item_quantity = data.get('item_quantity')
				    item_amount = data.get('item_amount')
				    dict_df = dict_df.append({'item_name': str(data.get('item_name')), 'item_quantity': str(data.get('item_quantity')),'item_amount': str(data.get('item_amount'))}, ignore_index=True)
			    dict_df['item_quantity'] = dict_df['item_quantity'].astype(float)
			    dict_df['item_amount'] = dict_df['item_amount'].astype(float)
			    dict_df['total_amount'] = dict_df['item_quantity'] * dict_df['item_amount']
			    # dict_df.ignore_index(inplace=True)
			    total = dict_df['total_amount'].sum()
			    self.object.grand_total = total
			    id = self.object.id
			    titles.save()
			    dict_df.to_csv('dict_df.csv')
			    item_date = str(item_date)
			    total = str(total)
			    id = str(id)

			    invoice_id = open("media/invoice_id.txt", "w")
			    invoice_id.writelines(id)
			    invoice_id.close()


			    c = open("media/customer_name.txt", "w")
			    c.writelines(customer_name)
			    c.close()

			    i = open("media/item_date.txt", "w")
			    i.writelines(item_date)
			    i.close()

			    a = open("media/customer_address.txt", "w")
			    a.writelines(customer_address)
			    a.close()

			    t = open("media/total.txt", "w")
			    t.writelines(total)
			    t.close()
	    return super(GenerateInvoiceView, self).form_valid(form)


    def get_success_url(self):
	    return reverse_lazy('download_summary')

def download_summary(request):
    file1 = open("media/customer_name.txt", "r")
    customer_name = file1.read()
    file1.close()

    file2 = open("media/item_date.txt", "r")
    item_date = file2.read()
    file2.close()

    file3 = open("media/customer_address.txt", "r")
    customer_address = file3.read()
    file3.close()

    file4 = open("media/total.txt", "r")
    total = file4.read()
    file4.close()

    file5 = open("media/invoice_id.txt", "r")
    invoice_id = file5.read()
    file5.close()

    dict_df = pd.read_csv('dict_df.csv').drop(columns='Unnamed: 0')

    data = {
    'customer_name':customer_name,
    'item_date':item_date,
    'customer_address':customer_address,
    'total':total,
    'dict_df':dict_df,
	'invoice_id':invoice_id,
    }
    pdf = render_to_pdf('temp.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def filter(request):
    search_list = AddUsers.objects.all()
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    if first_name or last_name :
	    search_list = AddUsers.objects.filter(
        Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name)).distinct()

    paginator = Paginator(search_list, 5)
    page = request.GET.get('page')

    try:
        search_list = paginator.page(page)
    except PageNotAnInteger:
        search_list = paginator.page(1)
    except EmptyPage:
        search_list = paginator.page(paginator.num_pages)
    context = {
        'search_list': search_list
    }
    return render(request, 'users_list.html', context)


def handler404(request, *args, **argv):
    return render(request, '404.html', status=404)


def handler500(request, *args, **argv):
    return render(request, '500.html', status=404)
