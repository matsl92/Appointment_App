from django.contrib import admin
from .models import Week, Gap, Appointment, Servicio, Brecha

admin.site.register([Appointment, Servicio, Brecha])