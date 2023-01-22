from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser

fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'points', 'date_of_birth', 'occupation', 'email')})
                                    # only 'date_of_birth', 'occupation' and 'phone_number' belong to our new user model
UserAdmin.fieldsets = tuple(fields)

admin.site.register(NewUser, UserAdmin)