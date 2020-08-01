from django.db import models
import datetime
from phone_field import PhoneField
from django.utils import timezone

class AddUsers(models.Model):
	first_name = models.CharField(max_length=300)
	last_name = models.CharField(max_length=300)
	date_of_birth = models.DateField()
	age = models.IntegerField(max_length=2)
	sex = models.CharField(max_length=10)
	height = models.CharField(max_length=20)
	weight = models.CharField(max_length=20)
	full_address = models.TextField(max_length=None)
	phone_number = models.CharField(max_length=20)
	alternate_phone = models.CharField(max_length=20)
	membership_start_date = models.DateField(default=timezone.now)
	membership_end_date = models.DateField(default=timezone.now)
	blood_group =  models.CharField(max_length=20)
	medical_history =  models.CharField(max_length=300)
	# paid = models.BooleanField(default=False)

	def __str__(self):
		return self.first_name


class GenerateInvoice(models.Model):
	customer_name = models.CharField(max_length=300)
	item_name = models.CharField(max_length=300)
	item_quantity = models.CharField(max_length=300)
	item_amount = models.CharField(max_length=300)
	item_date = models.DateField(default=timezone.now)

	def __str__(self):
		return self.item_name
