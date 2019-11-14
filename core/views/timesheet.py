from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import calendar, datetime, holidays, time
from datetime import timedelta
from core.models.timesheet import Project, Timesheet
from core.utils import get_start_and_end_date_from_calendar_week, get_start_and_end_date_from_month, add_months, get_user, get_accesible_projects
from django.conf import settings 
from django.db.models import Sum
from django.contrib.auth import get_user_model
    

WEEKEND_DAYS = [5,6]

class SaveTimesheetView(APIView):

    permission_classes = (IsAuthenticated,) 

    def post(self, request, *args, **kwargs):

        data = request.data
        user = get_user(request, kwargs)

        for item in data['data']:
            index = 0
            now = datetime.datetime.now()
            if 'week' in item:
                week = item['week']
                week_delta = int(kwargs.get('week_delta', 0))
                week += week_delta
                year = now.year
                all_days = get_start_and_end_date_from_calendar_week(year, week )
            else: # month view!
                month_delta = int(kwargs.get('month_delta', 0))
                now = add_months(now, month_delta)
                year = now.year
                month = now.month
                all_days = get_start_and_end_date_from_month(year, month)

            for hour in item['hours']:
                day = all_days[index]
                t, created = Timesheet.objects.get_or_create(
                    user=user,
                    project_id=item['_id'],
                    day=day,
                )
                index += 1
                t.hour=hour
                t.save()


        return Response({'message': 'saved'})

class GetWeekView(APIView):

    permission_classes = (IsAuthenticated,) 

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        year = now.year
        week = now.isocalendar()[1]
        it_holidays = holidays.Italy(years=[now.year]) 

        week_delta = int(kwargs.get('week_delta', 0))
        week += week_delta

        all_days = get_start_and_end_date_from_calendar_week(year, week )

        # Print all the holidays in UnitedKingdom in year 2018 
        content = []
        for day in all_days:
            content.append({
                "date":day.strftime("%d/%m/%Y"),
                "week": week,
                "is_festivity": day in it_holidays,
                "is_weekend": day.weekday() in WEEKEND_DAYS
            })

        return Response(content)

class GetWeekDataView(APIView):

    permission_classes = (IsAuthenticated,) 

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        year = now.year
        week = now.isocalendar()[1]
        user = get_user(request, kwargs)

        week_delta = int(kwargs.get('week_delta', 0))
        week += week_delta
        all_days = get_start_and_end_date_from_calendar_week(year, week )

        # Print all the holidays in UnitedKingdom in year 2018 
        content = []

        is_user_request = kwargs.get('users', None)
        if is_user_request:
            User = get_user_model()
            for user in User.objects.all():
                hours = []
                for day in all_days:
                    ts = Timesheet.objects.filter( day=day, user=user).aggregate(Sum('hour'))
                    print ('ts', ts)
                    if ts and 'hour__sum' in ts:
                        hours.append(ts['hour__sum'])
                    else:
                        hours.append(0)

                
                content.append({
                    "name": user.username,
                    "_id": user.pk,
                    "week": week,
                    "hours": hours
                },)
        else:
            for prj in get_accesible_projects(user, all_days[0], all_days[-1]):
                hours = []
                for day in all_days:
                    ts = Timesheet.objects.filter(project=prj, day=day, user=user).first()
                    if ts:
                        hours.append(ts.hour)
                    else:
                        hours.append(0)

                
                content.append({
                    "name": prj.name,
                    "_id": prj.pk,
                    "week": week,
                    "hours": hours
                },)

        return Response(content)
        
class GetMonthView(APIView):

    permission_classes = (IsAuthenticated,) 

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()

        month_delta = int(kwargs.get('month_delta', 0))
        now = add_months(now, month_delta)

        year = now.year
        month = now.month
        it_holidays = holidays.Italy(years=[now.year]) 

        all_days = get_start_and_end_date_from_month(year, month)

        # Print all the holidays in UnitedKingdom in year 2018 
        content = []
        for day in all_days:
            content.append({
                "date":day.strftime("%d/%m/%Y"),
                "is_festivity": day in it_holidays,
                "is_weekend": day.weekday() in WEEKEND_DAYS
            })

        return Response(content)

class GetMonthDataView(APIView):

    permission_classes = (IsAuthenticated,) 

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        user = get_user(request, kwargs)

        month_delta = int(kwargs.get('month_delta', 0))
        now = add_months(now, month_delta)

        year = now.year
        month = now.month

        all_days = get_start_and_end_date_from_month(year, month)

        # Print all the holidays in UnitedKingdom in year 2018 
        content = []
        is_user_request = kwargs.get('users', None)
        if is_user_request:
            User = get_user_model()
            for user in User.objects.all():
                hours = []
                for day in all_days:
                    ts = Timesheet.objects.filter( day=day, user=user).aggregate(Sum('hour'))
                    print ('ts', ts)
                    if ts and 'hour__sum' in ts:
                        hours.append(ts['hour__sum'])
                    else:
                        hours.append(0)
                
                content.append({
                    "name": user.username,
                    "_id": user.pk,
                    "hours": hours
                },)
        else:

            for prj in get_accesible_projects(user, all_days[0], all_days[-1]):
                hours = []
                for day in all_days:
                    ts = Timesheet.objects.filter(project=prj, day=day, user=user).first()
                    if ts:
                        hours.append(ts.hour)
                    else:
                        hours.append(0)
                
                content.append({
                    "name": prj.name,
                    "_id": prj.pk,
                    "hours": hours
                },)

        return Response(content)
        
