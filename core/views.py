from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import calendar, datetime, holidays, time
from datetime import timedelta
from .models import Project, Timesheet

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


class SaveTimesheetView(APIView):

    permission_classes = (IsAuthenticated,) 

    def post(self, request, *args, **kwargs):

        data = request.data
        user=request.user

        #{"data":[{"name":"TEST","_id":1,"week":45,"hours":[2,0,0,0,0,0,0]}]}
        now = datetime.datetime.now()
        year = now.year

        for item in data['data']:
            index = 0
            all_days = get_start_and_end_date_from_calendar_week(year, item['week'])

            for hour in item['hours']:
                day = all_days[index]
                t, created = Timesheet.objects.get_or_create(
                    user=user,
                    week=item['week'],
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
                "is_weekend": day.weekday() in [5,6]
            })

        return Response(content)


class GetWeekDataView(APIView):

    permission_classes = (IsAuthenticated,) 

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        year = now.year
        week = now.isocalendar()[1]
        it_holidays = holidays.Italy(years=[now.year]) 
        user = request.user

        week_delta = int(kwargs.get('week_delta', 0))
        week += week_delta
        all_days = get_start_and_end_date_from_calendar_week(year, week )

        # Print all the holidays in UnitedKingdom in year 2018 
        content = []
        for prj in Project.objects.all():
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
        

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

