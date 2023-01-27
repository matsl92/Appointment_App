from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from authenticate.models import NewUser
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
            date = self.fecha
            start = self.inicio
            n = (self.final-self.inicio) // gap_step
            for i in range(n):
                gap = Gap(
                    date_and_time=datetime(date.year, date.month, date.day, start.hour, start.minute), 
                    time_period = gap_step, 
                    brecha=self)
                gap.save()
                start += gap_step
            super().save()
        

class Servicio(models.Model):
    nombre = models.CharField(max_length=30)
    duracion = models.DurationField()
    valor = models.BigIntegerField()
    
    def save(self, *args, **kwargs):
        self.duracion = approximate_timedelta(self.duracion)
        super().save()

class Appointment(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pk)
  
class Gap(models.Model):
    date_and_time = models.DateTimeField(unique=True)
    time_period = models.DurationField()
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_DEFAULT, default=None, null=True)
    brecha = models.ForeignKey(Brecha, on_delete=models.CASCADE, default=None)
    is_limit = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.date_and_time.time().strftime('%I:%M %p'))
    

class Week(models.Model):
    minutes_per_appointment = models.IntegerField(default=30)
    start_date = models.DateField()
    monday_start = models.TimeField(default=datetime.time(7), blank=True, null=True)
    monday_end = models.TimeField(default=datetime.time(22), blank=True, null=True)
    tuesday_start = models.TimeField(default=datetime.time(7), blank=True, null=True)
    tuesday_end = models.TimeField(default=datetime.time(22), blank=True, null=True)
    wednesday_start = models.TimeField(default=datetime.time(7), blank=True, null=True)
    wednesday_end = models.TimeField(default=datetime.time(22), blank=True, null=True)
    thursday_start = models.TimeField(default=datetime.time(7), blank=True, null=True)
    thursday_end = models.TimeField(default=datetime.time(22), blank=True, null=True)
    friday_start = models.TimeField(default=datetime.time(7), blank=True, null=True)
    friday_end = models.TimeField(default=datetime.time(22), blank=True, null=True)
    saturday_start = models.TimeField(default=datetime.time(7), blank=True, null=True)
    saturday_end = models.TimeField(default=datetime.time(22), blank=True, null=True)
    sunday_start = models.TimeField(default=datetime.time(7), blank=True, null=True)
    sunday_end = models.TimeField(default=datetime.time(22), blank=True, null=True)
