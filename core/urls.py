from django.urls import path
from core.views import timesheet, auth

urlpatterns = [
    path('get_week/<slug:week_delta>/', timesheet.GetWeekView.as_view(), name='get_week'),
    path('get_week_data/<slug:week_delta>/', timesheet.GetWeekDataView.as_view(), name='get_week_data'),
    path('get_week_data/<slug:week_delta>/<slug:users>/', timesheet.GetWeekDataView.as_view(), name='get_week_data_by_users'),
    path('save_timesheet_week/<slug:week_delta>/', timesheet.SaveTimesheetView.as_view(), name='save_timesheet_week'),
    

    path('get_month/<slug:month_delta>/', timesheet.GetMonthView.as_view(), name='get_month'),
    path('get_month_data/<slug:month_delta>/', timesheet.GetMonthDataView.as_view(), name='get_month_data'),
    path('get_month_data/<slug:week_delta>/<slug:users>/', timesheet.GetMonthDataView.as_view(), name='get_month_data_by_users'),
    path('save_timesheet_month/<slug:month_delta>/', timesheet.SaveTimesheetView.as_view(), name='save_timesheet_month'),

    path('login/', auth.login, name='login'),
]