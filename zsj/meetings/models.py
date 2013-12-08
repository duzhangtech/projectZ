from django.db import models
import datetime
from django.utils import timezone;


# Create your models here.
class Meeting (models.Model):
	name = models.CharField(max_length=20)
	user_name = models.CharField(max_length = 20)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.name;

class Choice(models.Model):
	Meeting = models.ForeignKey(Meeting)
	name = models.CharField(max_length = 20);
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default =0)
	def __str__(self):
		return self.choice_text