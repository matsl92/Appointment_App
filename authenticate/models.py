from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class NewUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    REQUIRED_FIELDS = ['email', 'phone_number']
    
class PhoneVal(models.Model):
    phone_number = PhoneNumberField(blank=False, null=False)