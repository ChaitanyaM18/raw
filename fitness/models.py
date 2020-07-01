from django.db import models
import datetime
from phone_field import PhoneField

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
	membership_start_date = models.DateField()
	membership_end_date = models.DateField()
	blood_group =  models.CharField(max_length=20)
	medical_history =  models.CharField(max_length=300)

	def __str__(self):
		return self.first_name