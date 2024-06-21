from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.take_and_view_attendance, name='take_and_view_attendance'),
]

