from django.shortcuts import render, HttpResponse, redirect
from .models import Week, Gap, Appointment, Servicio, Brecha
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from datetime import date, time, datetime, timedelta
from django.conf import settings
from django.utils.timezone import make_aware, localtime
from .forms import WeekForm
from authenticate.forms import NewUserForm
from django.urls import reverse
from urllib.parse import urlencode
from django.utils.translation import gettext as _
from .tools import Bubble, Label, SemiGap, get_str_values, approximate_time, index_addition, gap_step, gap_duration


# Classes, functions and variables

# class Bubble:   # Global class
#         def __init__(self, start, end):
#             self.start = start
#             self.end = end
        
#         def __str__(self):
#             return str(self.start.time())

# class SemiGap:   # Global class
#     def __init__(self, start, end, index):
#         self.start = start
#         self.end = end
#         self.index = index
    
#     def __str__(self):
#         return str(self.start.time().strftime('%I:%M %p'))
       
# class Label:
#     def __init__(self, date):
#         self.date = date.strftime('%d')
#         self.day = date.strftime('%a')

# def get_str_values(post):  
#     values = {}
#     for key, value in post.items():
#         values[key] = value
#     return(values)

# def approximate_time(t):  # create_new_gaps GET
#     a = t.minute
#     appr_a = round(a/5)*5
#     if appr_a == 60:
#         return time(t.hour + 1, 0)
#     else:
#         return time(t.hour, appr_a)
    
# def index_addition(index, num): # create_gaps
#     elements = index.split(':')
#     last = int(elements[-1])
#     elements[-1] = str(last+num)
#     return ':'.join(elements)
              
def make_semigaps(week, n_days, start_date):    # returns semigap list // doesn't use the last item in the days of week
        wdn = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        semigaps = []
        for i in range(n_days):
            d = start_date + timedelta(days=i) 
            t1 = week[wdn.index(d.strftime('%A'))][0]
            t2 = week[wdn.index(d.strftime('%A'))][1]
            start = make_aware(datetime(d.year, d.month, d.day, t1.hour, t1.minute))
            end = make_aware(datetime(d.year, d.month, d.day, t2.hour, t2.minute))
            n = (end-start) // gap_step
            for j in range(n):
                index = ':'.join([str(i), str(j)])
                end = start + gap_step
                semigaps.append(SemiGap(start, end, index))
                start = end
        return semigaps 
    
def delete_expired_gaps():  # Deletes expired_gaps // used in gaps
        cont = 0
        for gap in Gap.objects.filter(date_and_time__lte=make_aware(datetime.today())):
        # for gap in Gap.objects.filter(date_and_time__lte=datetime.today()):
            gap.delete()
            cont += 1
        print(cont, 'expired gaps deleted')

def get_next_start_date():
    try:
        x = Gap.objects.last().date_and_time.date() + timedelta(days=1)
        print(x)
    except:
        x = date.today()
    return x

# gap_step = timedelta(minutes=5) 

# gap_duration = timedelta(minutes=30) # Can be modified in select_period.html, when that input is not hidden


# Views

@login_required()
def home(request):
    form = NewUserForm(instance=request.user)
    context = {'user': request.user, 'form': form, 'message': _('first text to be translated')}
    return render(request, 'appointments/home.html', context)

@login_required()
def personal_info(request):
    if request.method == 'GET':
        form = NewUserForm(instance=request.user)
        context = {'form': form}
        return render(request, 'appointments/personal_info.html', context)
    if request.method == 'POST':
        print(request.POST)
        user = request.user
        form = NewUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            occupation = form.cleaned_data['occupation']
            if email != '' and email is not None:
                user.email = email
            if first_name != '' and first_name is not None:
                user.first_name = first_name
            if last_name != '' and last_name is not None:
                user.last_name = last_name
            if date_of_birth != '' and date_of_birth is not None:
                user.date_of_birth = date_of_birth
            if occupation != '' and occupation is not None:
                user.occupation = occupation
            user.save()
            return redirect('appointments:home')
        else:
            return redirect('appointments:personal_info')

@login_required()
def select_period(request): 
    if request.method == 'GET':
        form = WeekForm()  
        context = {'form': form, 'min': date.today().strftime("%Y-%m-%d"), 'value': get_next_start_date().strftime("%Y-%m-%d")}
        return render(request, 'appointments/select_period.html', context)
        
    if request.method == 'POST':
        str_values = get_str_values(request.POST)
        str_values.pop('csrfmiddlewaretoken')
        start_date = datetime.strptime(str_values['start_date'], '%Y-%m-%d').date()
        
        try:
            if Gap.objects.last().__dict__['date_and_time'].date() >= start_date:
                context = str_values
                context['start_date_name'] = start_date.strftime('%A, %B %d')
                return render(request, 'appointments/select_overwrite.html', context)
            else:
                base_url = reverse('appointments:create_gaps')
                str_values['option'] = '1'
                query_string = urlencode(str_values)
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
        except:
            base_url = reverse('appointments:create_gaps')
            str_values['option'] = '1'
            query_string = urlencode(str_values)
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
          
@login_required()        
def create_gaps(request): 
    
    def make_semigaps(week, n_days, start_date):    # returns semigap list // doesn't use the last item in the days of week
        wdn = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        semigaps = []
        for i in range(n_days):
            d = start_date + timedelta(days=i) 
            t1 = week[wdn.index(d.strftime('%A'))][0]
            t2 = week[wdn.index(d.strftime('%A'))][1]
            start = make_aware(datetime(d.year, d.month, d.day, t1.hour, t1.minute))
            end = make_aware(datetime(d.year, d.month, d.day, t2.hour, t2.minute))
            n = (end-start) // gap_step
            for j in range(n):
                index = ':'.join([str(i), str(j)])
                end = start + gap_step
                semigaps.append(SemiGap(start, end, index))
                start = end
        return semigaps 
            
    def remove_equivalent_gaps_in_used(semigaps):  # returns semigap list // compare_and_delete_semigaps
        used_gaps = Gap.objects.exclude(appointment=None)
        used_dts = [gap.date_and_time for gap in used_gaps]
        us_dt_semi = [semigap.start for semigap in semigaps]  
        for dt in used_dts:
            if dt in us_dt_semi:
                semigaps.pop(us_dt_semi.index(dt))
                us_dt_semi.remove(dt)
        return semigaps
           
    def make_bubbles_after_semigaps(semigaps):  # returns bubble list
        bubbles = []
        start = semigaps[0].start
        for i in range(len(semigaps)-1):
            if semigaps[i].end != semigaps[i+1].start:
                end = semigaps[i].end
                bubbles.append(Bubble(start, end))
                start = semigaps[i+1].start
            if i == len(semigaps)-2:
                end = semigaps[i+1].end
                bubbles.append(Bubble(start, end))
        return bubbles
    
    def make_bubbles_after_gaps():  # returns bubble list
        start_datetime = make_aware(datetime(start_date.year, start_date.month, start_date.day, 0, 0))
        end_datetime = start_datetime + timedelta(days=n_days)
        gaps = Gap.objects.filter(date_and_time__gte=start_datetime).filter(date_and_time__lte=end_datetime)
        bubbles = []
        try:
            start = gaps[0].date_and_time
        except:
            pass
        for i in range(len(gaps)-1):
            if gaps[i].date_and_time + gap_step != gaps[i+1].date_and_time:
                end = gaps[i].date_and_time + gap_step
                bubbles.append(Bubble(start, end))
                start = gaps[i+1].date_and_time
            if i == len(gaps)-2:
                end = gaps[i+1].date_and_time + gap_step
                bubbles.append(Bubble(start, end))
        return bubbles
    
    def get_base_semigap_pack(bubbles, semigaps):  # returns semigap list of lists
        used_dts = [semigap.start for semigap in semigaps]
        semigap_pack = []
        semigaps_of_day = []
        if len(bubbles) == 1:
            n = (bubbles[0].end-bubbles[0].start) // gap_duration
            start = bubbles[0].start
            for j in range(n):
                semigaps_of_day.append(semigaps[used_dts.index(start)])
                start += gap_duration
            semigap_pack.append(semigaps_of_day)
        for i in range(len(bubbles)-1):
            n = (bubbles[i].end-bubbles[i].start) // gap_duration
            bubble_semigaps = []
            start = bubbles[i].start
            for j in range(n):
                bubble_semigaps.append(semigaps[used_dts.index(start)])
                start += gap_duration
            if start.date() != bubbles[i+1].start.date():
                semigaps_of_day += bubble_semigaps
                semigap_pack.append(semigaps_of_day)
                semigaps_of_day = []
            if start.date() == bubbles[i+1].start.date():
                semigaps_of_day += bubble_semigaps
            if i == len(bubbles)-2:
                n = (bubbles[-1].end-bubbles[-1].start) // gap_duration
                bubble_semigaps = []
                start = bubbles[-1].start
                for j in range(n):
                    bubble_semigaps.append(semigaps[used_dts.index(start)])
                    start += gap_duration
                semigaps_of_day += bubble_semigaps
                semigap_pack.append(semigaps_of_day)
        for day in semigap_pack:
            label = Label(day[0].start.date())
            day.insert(0, label)
                
        return semigap_pack
  
    def get_base_gap_pack():  # returns list of gap lists
        bubbles = make_bubbles_after_gaps()
        start_datetime = make_aware(datetime(start_date.year, start_date.month, start_date.day, 0, 0))
        end_datetime = start_datetime + timedelta(days=n_days)
        gaps = Gap.objects.filter(date_and_time__gte=start_datetime).filter(date_and_time__lte=end_datetime)
        
        used_dts = [gap.date_and_time for gap in gaps]
        gap_pack = []
        gaps_of_day = []
        
        if len(bubbles) == 1:
            n = (bubbles[0].end-bubbles[0].start) // gap_duration
            start = bubbles[0].start
            for j in range(n):
                gaps_of_day.append(gaps[used_dts.index(start)])
                start += gap_duration
            gap_pack.append(gaps_of_day)
        for i in range(len(bubbles)-1):
            n = (bubbles[i].end-bubbles[i].start) // gap_duration
            bubble_gaps = []
            start = bubbles[i].start
            for j in range(n):
                bubble_gaps.append(gaps[used_dts.index(start)])
                start += gap_duration
            if start.date() != bubbles[i+1].start.date():
                gaps_of_day += bubble_gaps
                gap_pack.append(gaps_of_day)
                gaps_of_day = []
            if start.date() == bubbles[i+1].start.date():
                gaps_of_day += bubble_gaps
            if i == len(bubbles)-2:
                n = (bubbles[-1].end-bubbles[-1].start) // gap_duration
                bubble_gaps = []
                start = bubbles[-1].start
                for j in range(n):
                    bubble_gaps.append(gaps[used_dts.index(start)])
                    start += gap_duration
                gaps_of_day += bubble_gaps
                gap_pack.append(gaps_of_day)
        for day in gap_pack:
            label = Label(day[0].date_and_time.date())
            day.insert(0, label)
                
        return gap_pack
        
    def delete_available_gaps_out_of_range(week, n_days, start_date):  # Deletes gaps for either being avalibale and out of range o just for being out of range
        wdn = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cont = 0
        for i in range(n_days):
            d = start_date + timedelta(days=i) 
            t1 = week[wdn.index(d.strftime('%A'))][0]
            t2 = week[wdn.index(d.strftime('%A'))][1]
            start = make_aware(datetime(d.year, d.month, d.day, t1.hour, t1.minute))
            end = make_aware(datetime(d.year, d.month, d.day, t2.hour, t2.minute))
            for gap in Gap.objects.filter(appointment=None).filter(date_and_time__year=start.year).filter(date_and_time__month=start.month).filter(date_and_time__day=start.day):
                if gap.date_and_time.time() < start.time() or gap.date_and_time.time() >= end.time():
                    
                    gap.delete()
                    cont += 1
        print(cont, 'available out of range gaps deleted')
        
    def delete_gaps_and_appointments_out_of_range(week, n_days, start_date):
        wdn = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cont = 0
        for i in range(n_days):
            d = start_date + timedelta(days=i) 
            t1 = week[wdn.index(d.strftime('%A'))][0]
            t2 = week[wdn.index(d.strftime('%A'))][1]
            start = make_aware(datetime(d.year, d.month, d.day, t1.hour, t1.minute))
            end = make_aware(datetime(d.year, d.month, d.day, t2.hour, t2.minute))
            for gap in Gap.objects.filter(date_and_time__year=start.year).filter(date_and_time__month=start.month).filter(date_and_time__day=start.day):
                if gap.date_and_time.time() < start.time() or gap.date_and_time.time() >= end.time():
                    try:
                        gap.appointment.delete()
                    except:
                        pass
                    gap.delete()
                    cont += 1
        print(cont, 'out of range gaps deleted')  
    
    def delete_selected_gaps_if_existing(semigaps, indexes): # and afected appointments, All equivalent gaps to indexes if existing
        all_gaps = list(Gap.objects.all())
        all_gap_dts = [gap.date_and_time for gap in all_gaps]
        all_indexes = []
        for index in indexes:
            for i in range(gap_duration//gap_step):
                all_indexes.append(index)
                index = index_addition(index, 1)
        all_selected_dts = [semigap.start for semigap in semigaps if semigap.index in all_indexes]
        cont = 0
        for dt in all_selected_dts:
            if dt in all_gap_dts:
                try:
                    all_gaps[all_gap_dts.index(dt)].appointment.delete()
                except:
                    pass
                all_gaps[all_gap_dts.index(dt)].delete()
                cont += 1
        print(cont, 'existing gaps deleted')
             
    def remove_selected_semigaps(semigaps, indexes):  # returns semigap list
        semigap_indexes = [semigap.index for semigap in semigaps]
        for index in indexes:
            if index in semigap_indexes:
                for i in range(gap_duration//gap_step):
                    semigaps.pop(semigap_indexes.index(index))
                    semigap_indexes.remove(index)
                    index = index_addition(index, 1)
        return semigaps
    
    def Create_gaps_if_missing(semigaps): # Creates gaps after checking whether they exist or not
        gap_dts = [gap.date_and_time for gap in Gap.objects.all()]
        for semigap in semigaps:
            if not semigap.start in gap_dts:
                gap = Gap(date_and_time=semigap.start, time_period=gap_step)
                gap.save()
    
    if request.GET:
        str_values = get_str_values(request.GET)
    if request.POST:
        str_values = get_str_values(request.POST)
        
    n_days = int(str_values['n_days'])
    gap_duration = timedelta(minutes=int(str_values['minutes_per_appointment']))
    start_date = datetime.strptime(str_values['start_date'], '%Y-%m-%d').date()
    monday = [str_values['monday_start'], str_values['monday_end'], 0]
    tuesday = [str_values['tuesday_start'], str_values['tuesday_end'], 1]
    wednesday = [str_values['wednesday_start'], str_values['wednesday_end'], 2]
    thursday = [str_values['thursday_start'], str_values['thursday_end'], 3]
    friday = [str_values['friday_start'], str_values['friday_end'], 4]
    saturday = [str_values['saturday_start'], str_values['saturday_end'], 5]
    sunday = [str_values['sunday_start'], str_values['sunday_end'], 6]
    days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
    
    week = []
    for i in days:
        day = [0, 0, 0]
        for j in range(2):
            try:
                day[j] = approximate_time(datetime.strptime(i[j],'%H:%M:%S').time())
            except:
                day[j] = approximate_time(datetime.strptime(i[j],'%H:%M').time())
        day[2] = i[2]
        week.append(day)  
    
    if request.method == 'GET':
                                
        if str_values['option'] == '0':
            
            return redirect('appointments:select_period')
        
        elif str_values['option'] == '1' or str_values['option'] == '3':
            
            semigaps = make_semigaps(week, n_days, start_date)
            
            bubbles = make_bubbles_after_semigaps(semigaps)
            
            semigap_pack = get_base_semigap_pack(bubbles, semigaps)
                  
        elif str_values['option'] == '2':
            
            semigaps = make_semigaps(week, n_days, start_date)
            
            semigaps = remove_equivalent_gaps_in_used(semigaps)
            
            bubbles = make_bubbles_after_semigaps(semigaps)
            
            semigap_pack = get_base_semigap_pack(bubbles, semigaps)
                
        str_values['semigap_pack'] = semigap_pack
        return render(request, 'appointments/create_gaps.html', str_values)
    
    if request.method == 'POST':
        
        try:
            indexes = dict(request.POST.lists())['indexes']
        except:
            indexes = []
        
        if str_values['option'] == '1':
            
            semigaps = make_semigaps(week, n_days, start_date)
            
            semigaps = remove_selected_semigaps(semigaps, indexes)
            
            Create_gaps_if_missing(semigaps)
             
        elif str_values['option'] == '2':
            
            delete_available_gaps_out_of_range(week, n_days, start_date) #available out of range gaps deleted
            
            semigaps = make_semigaps(week, n_days, start_date)
            
            semigaps = remove_equivalent_gaps_in_used(semigaps)
            
            delete_selected_gaps_if_existing(semigaps, indexes) # existing gaps deleted
            
            semigaps = remove_selected_semigaps(semigaps, indexes)
            
            Create_gaps_if_missing(semigaps)
            
        elif str_values['option'] == '3':
            
            delete_gaps_and_appointments_out_of_range(week, n_days, start_date)
            
            semigaps = make_semigaps(week, n_days, start_date)
        
            delete_selected_gaps_if_existing(semigaps, indexes)
            
            semigaps = remove_selected_semigaps(semigaps, indexes)
            
            Create_gaps_if_missing(semigaps)
        
        gap_pack = get_base_gap_pack()
        
        str_values['gap_pack'] = gap_pack
            
        return render(request, 'appointments/created_gaps.html', str_values)
          
@login_required()
def gaps(request):
    if request.method == 'GET':
        delete_expired_gaps()
        min_date = date.today().strftime("%Y-%m-%d")
        try:
            max_date = Gap.objects.order_by('date_and_time').last().date_and_time.strftime("%Y-%m-%d")
        except:
            max_date = min_date
        services = Servicio.objects.all()
        context = {'services': services, 'min': min_date, 'max': max_date}
        return render(request, 'appointments/select_service.html', context)

    if request.method == 'POST':
        service_pk = int(request.POST['service'])
        d = request.POST['date']
        service_duration = Servicio.objects.get(pk=service_pk).duracion
        available_gaps = Gap.objects.filter(date_and_time__date=d).filter(appointment=None).filter(date_and_time__gte=date.today())
        gap_pack = []
        if len(available_gaps) == 0:
            messages.error(request, (_('There are no available timeslots for this date or service, please select another date')))
            return redirect('appointments:gaps')
        else:
            bubbles = []
            start = available_gaps[0].date_and_time
            for i in range(len(available_gaps)-1):
                if available_gaps[i].date_and_time + available_gaps[i].time_period != available_gaps[i+1].date_and_time:
                    end = available_gaps[i].date_and_time + available_gaps[i].time_period
                    bubbles.append(Bubble(start, end))
                    start = available_gaps[i+1].date_and_time
                if i == len(available_gaps)-2:
                    end = available_gaps[i+1].date_and_time + available_gaps[i+1].time_period
                    bubbles.append(Bubble(start, end))
            
            for bubble in bubbles:
                start = bubble.start
                n = (bubble.end - bubble.start) // service_duration
                for i in range(n):
                    gap_pack.append(available_gaps[[gap.date_and_time for gap in available_gaps].index(start)])
                    start += service_duration
                if len(gap_pack) == 0:
                    messages.error(request, (_('There are no available timeslots for this date or service, please select another date')))
                    return redirect('appointments:gaps')
                  
            context = {'gap_pack': gap_pack, 'service_pk': service_pk, 'title': _('Book an appointment')}
        return render(request, 'appointments/select_time.html', context)

@login_required()
def success(request):
    gap_pk = int(request.POST['gap_pk'])
    service_pk = int(request.POST['service_pk'])
    service_duration = Servicio.objects.get(pk=service_pk).duracion
    available_gaps = list(Gap.objects.filter(appointment=None))
    n = service_duration // gap_step
    base_gap = Gap.objects.get(pk=gap_pk)
    start = base_gap.date_and_time
    for i in range(n):
        gap = Gap.objects.get(date_and_time=start)
        if gap in available_gaps:
            pass
        else:
            messages.error(request, (_('This gap is no longer available, please select anotherone')))
            print('Not all gaps were available')
            'messagge: this gap is no longer available, try again'
            return redirect('appointments:gaps')
        start += gap.time_period
    
    appointment = Appointment(user=request.user)
    appointment.save()
    start = base_gap.date_and_time
    for i in range(n):
        gap = Gap.objects.get(date_and_time=start)
        if gap in available_gaps:
            appointment.gap_set.add(gap)
        else:
            appointment.delete()
            messages.error(request, (_('This gap is no longer available, please try again')))
            print('Not all gaps were available at the second check')
            return redirect('appointments:gaps')
        start += gap.time_period
    return redirect('appointments:appointments')

@login_required()
def appointments(request):
    appoints = list(Appointment.objects.filter(user=request.user))
    for appoint in appoints:
        try:
            if appoint.gap_set.last().date_and_time + appoint.gap_set.last().time_period < make_aware(datetime.today()):
            # if appoint.gap_set.last().date_and_time + appoint.gap_set.last().time_period < datetime.today():    # for naive date_and_times
                appoints.remove(appoint)
        except:
            appoints.remove(appoint)
    try:
        appoint_beginnings = [appoint.gap_set.first() for appoint in appoints]
        appoint_beginnings.sort(key=lambda gap: gap.date_and_time)
    except:
        appoint_beginnings = []
    context = {'list': appoint_beginnings, 'title': _('My appointments')}
    return render(request, 'appointments/appointments.html', context)

@login_required()
def outlook(request):
    appoints = list(Appointment.objects.all())
    for appoint in appoints:
        try:
            if appoint.gap_set.last().date_and_time + appoint.gap_set.last().time_period < make_aware(datetime.today()):
                appoints.remove(appoint)
        except:
            appoints.remove(appoint)
    try:
        appoint_beginnings = [appoint.gap_set.first() for appoint in appoints]
        appoint_beginnings.sort(key=lambda gap: gap.date_and_time)
    except:
        appoint_beginnings = []
    context = {'list': appoint_beginnings, 'title': _('Upcoming appointments')}
    return render(request, 'appointments/appointments.html', context)

@login_required()
def create_week(request):
    if request.method == 'GET':
        form = WeekForm
        context = {'form': form}
        return render(request, 'appointments/create_week.html', context)
    if request.method == 'POST':
        form = WeekForm(request.POST)
        if form.is_valid():
            form.save()
            return(redirect('appointments:home'))
        else:
            return redirect('appointments:create_week')

@login_required()  
def success_2(request):
    print(request.POST)
    pk = dict(request.POST.lists())['pk'][0]
    duration = timedelta(minutes=int(dict(request.POST.lists())['duration'][0]))
    # In order to replace the use of pk for date_and_time //// maybe is also good to replace index for pk for selecting a indexing gap
    
    # bgdt = Gap.objects.get(index=index).date_and_time
    # n_gaps = duration//gap_step
    # available_gaps = list(Gap.objects.filter(appointment=None))
    # for i in range(n_gaps):
    #     if Gap.objects.get(date_and_time=bgdt+(gap_step*i)) in available_gaps:
    #         pass
    #     else:
    #         print('Not all gaps were available')
    #         'messagge: this gap is no longer available, try again'
    #         return redirect('appointments:new_gaps')
    
    # Keep changing the code in appointment = 
    
    
    
    base_gap_pk = Gap.objects.get(pk=pk).pk
    gap_step = timedelta(minutes=5)
    n_gaps = duration // gap_step
    available_gaps = list(Gap.objects.filter(appointment=None))
    for i in range(n_gaps):
        if Gap.objects.get(pk=base_gap_pk+i) in available_gaps:
            pass
        else:
            print('Not all gaps were available')
            'messagge: this gap is no longer available, try again'
            return redirect('appointments:gaps')
        
        
    appointment = Appointment(user=request.user)
    appointment.save()
    for i in range(n_gaps):
        gap = Gap.objects.get(pk=base_gap_pk+i)
        if gap in available_gaps:
            appointment.gap_set.add(gap)
        else:
            appointment.delete()
            print('Not all gaps were available')
            'messagge: this gap is no longer available, try again'
            return redirect('appointments:gaps')
    'display message'
    return redirect('appointments:appointments')

@login_required()   
def gaps_2(request):
           
    if request.method == 'GET':
        delete_expired_gaps()
        limit_date = datetime.today().date() + timedelta(days=7)
        limit_datetime = make_aware(datetime(limit_date.year, limit_date.month, limit_date.day, 0, 0))
             
        available_gaps = Gap.objects.filter(appointment=None).order_by('date_and_time').filter(date_and_time__lte=limit_datetime)
        if len(available_gaps) == 0:
            gap_pack = []
            context = {'gap_pack': gap_pack, 'title': _('There are no available timeslots')}
        else:
            bubbles = []
            start = available_gaps[0].date_and_time
            for i in range(len(available_gaps)-1):
                if available_gaps[i].date_and_time + available_gaps[i].time_period != available_gaps[i+1].date_and_time:
                    end = available_gaps[i].date_and_time + available_gaps[i].time_period
                    bubbles.append(Bubble(start, end))
                    start = available_gaps[i+1].date_and_time
                if i == len(available_gaps)-2:
                    end = available_gaps[i+1].date_and_time + available_gaps[i+1].time_period
                    bubbles.append(Bubble(start, end))
            
            for gap in Gap.objects.all():
                if gap.is_limit == True:
                    gap.is_limit = False              
                    gap.save()       
                    
            indexing_gaps = []
            for i in range(len(bubbles)):
                n = (bubbles[i].end-bubbles[i].start) // gap_duration
                start = bubbles[i].start
                for i in range(n):
                    gap = Gap.objects.get(date_and_time=start)
                    if i == n-1:
                        gap.is_limit = True
                        gap.save()
                    indexing_gaps.append(gap)
                    start += gap_duration
                    
            gap_pack = []
            date = indexing_gaps[0].date_and_time.date()
            daily_gaps = []
            for i in range(len(indexing_gaps)):
                if indexing_gaps[i].date_and_time.date() == date:
                    daily_gaps.append(indexing_gaps[i])
                else:
                    gap_pack.append(daily_gaps)
                    daily_gaps = []
                    daily_gaps.append(indexing_gaps[i])
                    date = indexing_gaps[i].date_and_time.date()
                if i == len(indexing_gaps)-1:
                    gap_pack.append(daily_gaps)
            for day in gap_pack:
                label = Label(day[0].date_and_time.date())
                day.insert(0, label)
            context = {'gap_pack': gap_pack, 'title': _('Available timeslots')}
        return render(request, 'appointments/gaps.html', context)
    
    if request.method == 'POST': 
        pk = dict(request.POST.lists())['pk'][0]
        gap = Gap.objects.get(pk=pk)
        context = {'gap': gap}
        return render(request, 'appointments/schedule.html', context)