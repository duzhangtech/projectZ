from django.shortcuts import render, get_object_or_404
# Create your views here
from django.utils import timezone;
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views import generic
from meetings.models import Meeting, Choice
from datetime import date

class DetailView(generic.DetailView):
    model = Meeting
    template_name = 'meetings/details.html'

class ResultsView(generic.DetailView):
    model = Meeting
    template_name = 'meetings/results.html'

class NameView(generic.DetailView):
    model = Meeting
    template_name = 'meetings/nameMtn.html'

#index page
def index(request):
    return render(request, 'meetings/index.html');

#create the mtn and organizer name
def createMtn (request):
    return render(request, 'meetings/createMtn.html');

def create(request):
    a = Meeting(name = request.POST['meeting_name'], pub_date=timezone.now());
    a.save();
    return HttpResponseRedirect(reverse('meetings:nameMtn', args=(a.id,)))

def name(request, meeting_id):
    p = get_object_or_404(Meeting, pk=meeting_id)
    p.user_name = request.POST['user_name'];
    p.save();
    return HttpResponseRedirect(reverse('meetings:availability_organizer', args=(p.id,)))
 
def giveDate(num):
    if num == 0: return 'Sunday'
    if num == 1: return 'Monday'
    if num == 2: return 'Tuesday'
    if num == 3: return 'Wednesday'
    if num == 4: return 'Thursday'
    if num == 5: return 'Friday'
    if num == 6: return 'Saturday'
#organizer_availability
def availability_organizer(request, meeting_id):
    p = get_object_or_404(Meeting, pk=meeting_id);
    today_date = date.today().weekday()
    global display
    display = [giveDate(today_date),\
                giveDate((today_date+1)%7),\
                giveDate((today_date+2)%7),\
                giveDate((today_date+3)%7),\
                giveDate((today_date+4)%7),\
                giveDate((today_date+5)%7),\
                giveDate((today_date+6)%7)]
    morningRange = [8,9,10,11]
    afternoonRange = [12,1,2,3,4,5,6,7,8,9,10]
    return render(request, 'meetings/availability_organizer.html', {'date': display, 'meeting': p, 'morningRange':morningRange, 'afternoonRange': afternoonRange,})

def availability_organizer_handler(request, meeting_id):
    p = get_object_or_404(Meeting, pk=meeting_id);
    if request.POST["gap"] == "60mins":
        availability_organizer = "2";
    if request.POST["gap"] == "30mins":
        availability_organizer = "1";
    
    for date in display:
        for num in range(8,12):
            availability_organizer=availability_organizer+str(request.POST.get(date+str(num)+'am', 0))
        for num in range(1,11):
            availability_organizer=availability_organizer+str(request.POST.get(date+str(num)+'pm', 0))
        availability_organizer=availability_organizer+str(request.POST.get(date+'12pm', 0))

    p.choice_set.create(choice_text=availability_organizer, votes=0, name=p.user_name)
    return HttpResponseRedirect(reverse('meetings:share', args=(p.id,)))

#share the link
class ShareView(generic.DetailView):
    model = Meeting
    template_name = 'meetings/share.html'

def Availability(request, meeting_id):
    p = get_object_or_404(Meeting, pk=meeting_id);
    today_date = date.today().weekday()

    display = [giveDate(today_date),\
                giveDate((today_date+1)%7),\
                giveDate((today_date+2)%7),\
                giveDate((today_date+3)%7),\
                giveDate((today_date+4)%7),\
                giveDate((today_date+5)%7),\
                giveDate((today_date+6)%7)]
    return render(request, 'meetings/availability_general.html', {'date': display, 'meeting': p,})

def availability_general_handler(request, meeting_id):
    p = get_object_or_404(Meeting, pk=meeting_id);
    availability_organizer = \
        str(request.POST.get('monday8am', 0)) + \
        str(request.POST.get('monday9am', 0)) + \
        str(request.POST.get('monday10am', 0)) +\
        str(request.POST.get('monday11am', 0)) +\
        str(request.POST.get('monday12pm', 0)) +\
        str(request.POST.get('monday1am', 0)) +\
        str(request.POST.get('monday2am', 0)) +\
        str(request.POST.get('monday3am', 0)) +\
        str(request.POST.get('monday4am', 0)) +\
        str(request.POST.get('monday5am', 0)) +\
        str(request.POST.get('monday6am', 0)) +\
        str(request.POST.get('monday7am', 0)) +\
        str(request.POST.get('monday8am', 0)) +\
        str(request.POST.get('monday9am', 0)) +\
        str(request.POST.get('monday10am', 0))

    p.choice_set.create(choice_text=availability_organizer, votes=0, name=request.POST['participant_name'],)
    return HttpResponse('Thanks for your response! Please contact the organizer for the result.')

#result
def result(request):
    p = get_object_or_404(Meeting, pk=request.POST['meeting_id']);
    availability = [0,0,0];
    for index in range(0,3):
        for choice in p.choice_set.all():
            if choice.choice_text[index] == '0':
                availability[index] = availability[index]+1;
    result=''
    if availability[0] == 0:
        result = result + 'Friday, '
    if availability[1] == 0:
        result = result + 'Saturday, '  
    if availability[2] == 0:
        result = result + 'Sunday'
    if availability[0] != 0 and availability[1] != 0 and availability[2] != 0:
        result = 'no date'
    return render(request, 'meetings/result.html', {'meeting':p, 'result': result,});

def vote(request, meeting_id):
    p = get_object_or_404(Meeting, pk=meeting_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the meeting voting form.
        return render(request, 'meetings/detail.html', {
            'meeting': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('meetings:results', args=(p.id,)))