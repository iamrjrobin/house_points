from django.contrib import admin
from .models import Employee, House

admin.site.register(House)
admin.site.register(Employee)