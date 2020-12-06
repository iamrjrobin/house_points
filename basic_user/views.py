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

def details(request, house_name):
    house= get_object_or_404(House, name=house_name)
    employees = Employee.objects.filter(house=house).annotate(points=Sum("point__value")).order_by('-points')
    print(employees.query)
    # employees= house.employee_set.all().order_by('-points')
    context= {
        'emp' : employees
    }
    return render(request, 'basic_user/details.html',context)

def taking_logs(request):
    # emps= get_object_or_404(Employee)
    # logs= get_object_or_404(Logger)
    # super().taking_logs(Employee, Logger)
    context={
        'log' : Logger.objects.all()
    }
    return render(request, 'basic_user/logs.html', context)