from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import calendar
import datetime
import holidays
from datetime import timedelta

def get_start_and_end_date_from_calendar_week(year, calendar_week):       
    monday = datetime.datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
    return monday, monday + datetime.timedelta(days=6.9)

class HelloView(APIView):

    #permission_classes = (IsAuthenticated,) 

    def get(self, request):
        uk_holidays = holidays.UnitedKingdom() 
  
        # Print all the holidays in UnitedKingdom in year 2018 
        for ptr in holidays.UnitedKingdom(years = 2018).items(): 
            print(ptr)
            
        content = {'message': 'Hello, World!'}
        return Response(content)