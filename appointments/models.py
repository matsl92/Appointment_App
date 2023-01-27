from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from authenticate.models import NewUser
from datetime import date, time, datetime, timedelta
from .tools import approximate_time, approximate_timedelta, gap_step, gap_duration

class Brecha(models.Model):
    fecha = models.DateField()
    inicio = models.TimeField()
    final = models.TimeField()
    
    def save(self, *args, **kwargs):
        self.inicio = approximate_time(self.inicio)
        self.final = approximate_time(self.final)
        if self.final > self.inicio:
            if self.pk:
                for gap in Brecha.objects.get(pk=self.pk).gap_set.all():
                    gap.delete()
            super().save()
            date = self.fecha
            start = datetime(date.year, date.month, date.day, self.inicio.hour, self.inicio.minute)
            n = (datetime(2020, 1, 1, self.final.hour, self.final.minute) - datetime(2020, 1, 1, self.inicio.hour, self.inicio.minute)) // gap_step
            for i in range(n):
                gap = Gap(
                    date_and_time=datetime(date.year, date.month, date.day, start.hour, start.minute), 
                    time_period = gap_step, 
                    brecha=self)
                gap.save()
                start += gap_step
    
    def __str__(self):
        return ''.join([self.fecha.strftime('%A %d '), self.inicio.strftime('(%I:%M %p - '), self.final.strftime('%I:%M %p)')])
        
class Servicio(models.Model):
    nombre = models.CharField(max_length=30)
    duracion = models.DurationField()
    valor = models.BigIntegerField()
    
    def save(self, *args, **kwargs):
        self.duracion = approximate_timedelta(self.duracion)
        super().save()
        
    def __str__(self):
        return self.nombre

class Appointment(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pk)
  
class Gap(models.Model):
    date_and_time = models.DateTimeField(unique=True)
    time_period = models.DurationField()
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_DEFAULT, default=None, null=True)
    brecha = models.ForeignKey(Brecha, on_delete=models.CASCADE)
    is_limit = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.date_and_time.time().strftime('%I:%M %p'))
    

class Week(models.Model):
    minutes_per_appointment = models.IntegerField(default=30)
    start_date = models.DateField()
    monday_start = models.TimeField(default=time(7), blank=True, null=True)
    monday_end = models.TimeField(default=time(22), blank=True, null=True)
    tuesday_start = models.TimeField(default=time(7), blank=True, null=True)
    tuesday_end = models.TimeField(default=time(22), blank=True, null=True)
    wednesday_start = models.TimeField(default=time(7), blank=True, null=True)
    wednesday_end = models.TimeField(default=time(22), blank=True, null=True)
    thursday_start = models.TimeField(default=time(7), blank=True, null=True)
    thursday_end = models.TimeField(default=time(22), blank=True, null=True)
    friday_start = models.TimeField(default=time(7), blank=True, null=True)
    friday_end = models.TimeField(default=time(22), blank=True, null=True)
    saturday_start = models.TimeField(default=time(7), blank=True, null=True)
    saturday_end = models.TimeField(default=time(22), blank=True, null=True)
    sunday_start = models.TimeField(default=time(7), blank=True, null=True)
    sunday_end = models.TimeField(default=time(22), blank=True, null=True)
