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
	print(timezone.now(),'timezone.now().date()')
	before_5_days = timezone.now().date() + timedelta(days=5)
	print(before_5_days,'before_5_days')
	posts = AddUsers.objects.filter(Q(membership_end_date = before_5_days)).order_by('membership_start_date')
	# a = AddUsers.objects.get(id=7)
	# print(a.membership_end_date)
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

    # def form_valid(self, form):
	#     context = self.get_context_data()
	#     titles = context['titles']
	#     dict_df = pd.DataFrame(columns=['item_name', 'item_quantity','item_amount'])
	#     with transaction.atomic():
	# 	    self.object = form.save()
	# 	    print(self.object.id)
	# 	    if titles.is_valid():
	# 		    titles.instance = self.object
	# 		    titles.save()
	# 	    customer_name = form.cleaned_data['customer_name']
	# 	    item_date = form.cleaned_data['purchased_date']
	# 	    for data in titles.cleaned_data:
	# 		    item_name = data.get('item_name')
	# 		    item_quantity = data.get('item_quantity')
	# 		    item_amount = data.get('item_amount')
	# 		    dict_df = dict_df.append({'item_name': str(data.get('item_name')), 'item_quantity': str(data.get('item_quantity')),'item_amount': str(data.get('item_amount'))}, ignore_index=True)
	# 	    dict_df['item_quantity'] = dict_df['item_quantity'].astype(int)
	# 	    dict_df['item_amount'] = dict_df['item_amount'].astype(int)
	# 	    dict_df['total_amount'] = dict_df['item_quantity'] * dict_df['item_amount']
	# 	    dict_df['total_amount'].sum()
	# 	    # dict_df.ignore_index(inplace=True)
	# 	    dict_df.to_csv('dict_df.csv')
	# 	    total = dict_df['total_amount'].sum()
	# 	    if titles.is_valid():
	# 		    titles.instance = self.object
	# 		    titles.save()
	# 		    print('save')
	# 		# total_amount = float(item_quantity)*float(item_amount)
	# 	    pd.set_option('colheader_justify', 'center')
	# 	    data = {
	# 	    'dict_df':dict_df,
	# 		'customer_name':customer_name,
	# 		'item_date':item_date,
	# 	    'total':total,
	# 	    }
	# 	    pdff = render_to_pdf('invoice.html', data)
	# 	    print(pdff)
	# 	    # f = open('assets/templates/in.html', 'w')
	# 	    # print(f)
	# 	    # # f.write('<div style="page-break-before: always;">')
	# 	    # k = dict_df.to_html()
	# 	    # f.write(k)
	# 	    # pdfkit.from_file('assets/templates/in.html','summary.pdf')
	# 	    # return HttpResponse(pdff, content_type='application/pdf')
	#     return super(GenerateInvoiceView, self).form_valid(form)''
    # def download_summary(self,data):
	#     pdf = render_to_pdf('in.html', data)
	#     print('Summary')
	#     return HttpResponse(pdf, content_type='application/pdf')

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
			    dict_df['item_quantity'] = dict_df['item_quantity'].astype(int)
			    dict_df['item_amount'] = dict_df['item_amount'].astype(int)
			    dict_df['total_amount'] = dict_df['item_quantity'] * dict_df['item_amount']
			    # dict_df.ignore_index(inplace=True)
			    total = dict_df['total_amount'].sum()
			    self.object.grand_total = total
			    titles.save()
			    dict_df.to_csv('dict_df.csv')
			    item_date = str(item_date)
			    total = str(total)


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

			    # dict_df = dict_df.to_json()
			    # item_date = str(item_date)
			    # total = str(total)
			    # data = {
			    # 'dict_df':dict_df,
			    # 'customer_name':customer_name,
			    # 'item_date':item_date,
			    # 'total':total,
			    # }
			    # data1 = {
			    # 'customer_name':customer_name,
			    # 'item_date':item_date,
			    # 'total':total,
			    # }
			    # with open("sample.json", "w") as outfile:
				#     json.dump(data1, outfile)
			    # pdf = render_to_pdf('in.html', data)
			    # new_hand = GenerateInvoice(customer_name=customer_name, purchased_date=item_date, customer_address=customer_address, grand_total='grand_total')
			    # new_hand.grand_total = total
			    # new_hand.save()

			    # print(GenerateInvoice.objects.exclude(grand_total=''))
			    # self.download_summary(data)
		    # return HttpResponse(pdf, content_type='application/pdf')
	    return super(GenerateInvoiceView, self).form_valid(form)


    def get_success_url(self):
	    return reverse_lazy('download_summary')

    # def download_summary(self,request):
	#     pdf = render_to_pdf('in.html', self.data)
	#     return HttpResponse(pdf, content_type='application/pdf')

    # def dispatch(self, request, *args, **kwargs):
	#     self.custom_save_session(request)
	#     return super(GenerateInvoiceView, self).dispatch(request, *args, **kwargs)

def download_summary(request):
    # with open("sample.json","r") as outfile:
	#     data = json.load(outfile)
    # print(data)
    # f = open('assets/templates/temp.html', 'w')
	#
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

    dict_df = pd.read_csv('dict_df.csv').drop(columns='Unnamed: 0')

    data = {
    'customer_name':customer_name,
    'item_date':item_date,
    'customer_address':customer_address,
    'total':total,
    'dict_df':dict_df,
    }
    pdf = render_to_pdf('temp.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
    # return render(request,'temp.html',{'data':data})

	# pdfkit.from_file(
	# 	'master/templates/master/inter.html',
	# 	'summaries/pdf/summary' + timestr + '.pdf')
    # final_data = {
    # 'data':data,
    # 'dict_df_p':dict_df_p,
    # }
    # dict_df_p = dict_df_p.to_dict()
    # result = merge(data, dict_df_p)
    # pdf = render_to_pdf('in.html', data,dict_df_p)
    # return HttpResponse(pdf, content_type='application/pdf')
