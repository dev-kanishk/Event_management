from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from bootstrap_datepicker_plus import DateTimePickerInput
from datetime import date, datetime
from pytz import timezone
from .models import Event
from django.db.models import Q



def signup(request):
    if request.method == 'POST':
        print("got request")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        print("get request")
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    else:
        print("get request")
        
    return render(request, 'login.html', {})

@login_required
def user_logout(request):
    logout(request)
    print("logout")
    return redirect('user_login')


def home(request):
    Active_Events, Past_Events = get_all_events()
    return render(request, 'home.html', {'Active_Events':Active_Events, 'Past_Events':Past_Events})

@login_required
def event(request):
    
    form = EventForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            print("saved")
            return redirect('home')

    form = EventForm()
    
    return render(request, 'event.html', {'form':form})


def search_event(request):
    if request.method =='POST':
        Active_Events, Past_Events = get_events(request.POST.get("search"))
        print(request.POST.get("search"))
    else:
        Active_Events, Past_Events = get_all_events()
    return render(request, 'search_event.html', {'Active_Events':Active_Events, 'Past_Events':Past_Events})

def get_all_events():
    intz = timezone('Asia/Kolkata')
    fmt_date = "%Y-%m-%d"
    fmt_time = "%H:%M"
    time = datetime.now(intz)
    print("Today's date:", time.strftime(fmt_date))
    print("Time:", time.strftime(fmt_time))
    events = Event.objects.all().order_by('id').reverse()
    Active_Events = []
    Past_Events = []
    print(events[0].date)
    for event in events:
        if(cmpdateTime(str(event.date) , time.strftime(fmt_date), str(event.time) , time.strftime(fmt_time)) ):
            Active_Events.append(event)
        else:
            Past_Events.append(event)

    return Active_Events,Past_Events

def cmpdateTime(date, currdate, time, currtime):
    lis_date = list(map(int, date.split('-')))
    print(lis_date)
    lis_currdate = list(map(int, currdate.split('-')))
    lis_time = list(map(int, time.split(':')))
    lis_currtime = list(map(int, currtime.split(':')))
    for i in range(len(lis_date)):
        if lis_date[i] < lis_currdate[i]:
            return False
        elif lis_date[i] > lis_currdate[i]:
            return True

    for i in range(len(lis_time)):
        if lis_time[i] < lis_currtime[i]:
            return False
        elif lis_time[i] > lis_currtime[i]:
            return True

        return True



def get_events(to_search):
    intz = timezone('Asia/Kolkata')
    fmt_date = "%Y-%m-%d"
    fmt_time = "%H:%M:%S"
    time = datetime.now(intz)
    print("Today's date:", time.strftime(fmt_date))
    print("Time:", time.strftime(fmt_time))
    events = Event.objects.filter(Q(title__icontains=to_search) | Q(city__icontains=to_search)).order_by('id').reverse()
    Active_Events = []
    # eventsBY_city = Event.objects.filter(city=to_search)
    Past_Events = []
    # print(type(events[0].time))
    for event in events:
        if(cmpdateTime(str(event.date) , time.strftime(fmt_date), str(event.time) , time.strftime(fmt_time))):
            Active_Events.append(event)
        else:
            Past_Events.append(event)

    return Active_Events,Past_Events