from django.contrib import admin
from .models import Week, Gap, Appointment, Servicio

admin.site.register([Week, Gap, Appointment, Servicio])