from django.contrib import admin
from .models import Employee, House, Logger, Point

admin.site.register(House)
admin.site.register(Employee)
admin.site.register(Logger)
admin.site.register(Point)