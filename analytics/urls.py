from django.urls import path
from . import views

urlpatterns = [
    path('average_salary/', views.average_salary, name='average_salary'),
    path('turnover_rate/', views.turnover_rate, name='turnover_rate'),
    path('average_salary_by_department/', views.average_salary_by_department, name='average_salary_by_department'),
  path('turnover_prediction/', views.employee_turnover_prediction, name='turnover_prediction'), 
  path('dashboard/', views.dashboard, name='hr_dashboard'),
]