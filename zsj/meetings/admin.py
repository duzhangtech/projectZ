
# Register your models here.
from django.contrib import admin
from meetings.models import Meeting, Choice

class ChoiceInline(admin.StackedInline):
	"""docstring for ChoiceInline"""
	model = Choice;
	extra = 1;

	
class MeetingAdmin(admin.ModelAdmin):
	fieldsets=[(None,  {'fields':['name']}),
	('name of Organizer', {'fields':['user_name']}),
	('Date information', {'fields':['pub_date'], 'classes':['collapse']}),]
	inlines = [ChoiceInline]



admin.site.register(Meeting, MeetingAdmin)