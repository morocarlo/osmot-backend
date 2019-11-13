from django.urls import path
from core import views

urlpatterns = [
    path('get_week/', views.GetWeekView.as_view(), name='get_week'),
    path('get_week_data/', views.GetWeekDataView.as_view(), name='get_week_data'),
    path('login/', views.login, name='login'),
]