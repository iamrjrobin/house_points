from django.contrib import admin
from .models import Employee, House, Logger, Point


class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = ['user', 'name', 'house','points' ]




admin.site.register(House)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Logger)
admin.site.register(Point)
