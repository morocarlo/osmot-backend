import calendar, datetime, holidays, time
from datetime import timedelta
from core.models.timesheet import Project, Timesheet
from django.conf import settings
from django.contrib.auth import get_user_model


def get_start_and_end_date_from_calendar_week(year, calendar_week):
    try:
        startdate = time.asctime(time.strptime('%d %d 0' % (year, calendar_week-2), '%Y %W %w')) 
    except:
        # GOTO NEXT YEAR
        last_week_array = []
        for i in range(0, 7):
            last_week_array.append( datetime.date(year, 12, 31-i).isocalendar()[1])
        last_week = max(last_week_array)
        calendar_week = calendar_week - last_week
        print (calendar_week)
        startdate = time.asctime(time.strptime('%d %d 0' % (year+1, calendar_week-2), '%Y %W %w')) 
    startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y') 
    dates = [startdate  + datetime.timedelta(days=1)] 
    for i in range(2, 8): #start from monday 
        day = startdate + datetime.timedelta(days=i)
        dates.append(day) 
    return dates

def get_start_and_end_date_from_month(year, month):
    nb_days = calendar.monthrange(year, month)[1]

    return [datetime.date(year, month, day) for day in range(1, nb_days+1)]

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def get_user(request, kwargs):
    user = request.user
    if request.user.is_superuser or request.user.is_staff:
        user_id = kwargs.get('user_id', None)
        if not user_id:
            user_id = request.GET.get('user_id', None)
        if not user_id:
            user_id = request.META.get('user_id', None)
        if user_id:
            User = get_user_model()
            user = User.objects.get(pk=user_id)

    return user

def get_accesible_projects(user, start_date, end_date):
    if user.is_superuser or user.is_staff:
        projects = Project.objects.filter(start_date__lte=end_date, end_date__gte=start_date).distinct()
    else:
        projects = Project.objects.filter(start_date__lte=end_date, end_date__gte=start_date, users__in=[user]).distinct()
    return projects