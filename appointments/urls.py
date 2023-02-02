from django.urls import path
from . import views

app_name = 'appointments'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('personal_info/', views.personal_info, name = 'personal_info'), 
    path('create_gaps/', views.create_gaps, name='create_gaps'),
    path('create_gaps/select_period/', views.select_period, name='select_period'), 
    path('gaps/', views.gaps, name='gaps'),
    path('gaps/success/', views.success, name='succes'), 
    path('appointments/', views.appointments, name='appointments'),  
    path('outlook/', views.outlook, name='outlook'), 
    path('create_week/', views.create_week, name='create_week'), 
    path('detail/', views.appointment_detail, name='appointment, detail'), 
]
