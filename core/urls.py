from django.urls import path
from core import views

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
]