from django.urls import path
from core.views import timesheet, auth

urlpatterns = [
    path('get_week/<slug:week_delta>/', timesheet.GetWeekView.as_view(), name='get_week'),
    path('get_week_data/<slug:week_delta>/', timesheet.GetWeekDataView.as_view(), name='get_week_data'),

    path('save_timesheet/', timesheet.SaveTimesheetView.as_view(), name='save_timesheet'),

    path('get_month/<slug:month_delta>/', timesheet.GetMonthView.as_view(), name='get_month'),
    path('get_month_data/<slug:month_delta>/', timesheet.GetMonthDataView.as_view(), name='get_month_data'),

    path('login/', auth.login, name='login'),
]