from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee, House, Logger
from django.shortcuts import get_object_or_404
from django.db.models import Sum


# Create your views here.
def display(request):
    house = House.objects.annotate(point=Sum("employee__point__value")).order_by('-point')
    context = {
        'house' : house
    }
    print(house)
    return render (request, 'basic_user/show.html',context)

def details(request, house_id):
    house= get_object_or_404(House, id=house_id)
    employees = Employee.objects.filter(house=house).annotate(points=Sum("point__value")).order_by('-points')
    # print(employees.query)
    # employees= house.employee_set.all().order_by('-points')
    context= {
        'emp' : employees
    }
    return render(request, 'basic_user/details.html',context)

def taking_logs(request):
    # emps= get_object_or_404(Employee)
    # logs= get_object_or_404(Logger)
    # super().taking_logs(Employee, Logger)
    log = Logger.objects.all().order_by('-date_and_time')
    house = House.objects.annotate(point=Sum("employee__point__value")).order_by('-point')
    context={
        'log' : log, 
        'house' : house
    }
    return render(request, 'basic_user/logs.html', context)

def single_log(request, employee_id):
    emps= get_object_or_404(Employee, id=employee_id)
    logs = Logger.objects.filter(emp=emps.id).order_by('-date_and_time')
    house = House.objects.annotate(point=Sum("employee__point__value")).order_by('-point')
    context = {
        'logs' : logs,
        'house' : house
    }   
    return render(request, 'basic_user/single_log.html', context)
