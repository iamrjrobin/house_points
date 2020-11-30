from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee, House
from django.shortcuts import get_object_or_404


# Create your views here.
def display(request):
    context ={
        'house': House.objects.all()
    }
    return render (request, 'basic_user/show.html',context)

def details(request,  house_name):
    house = get_object_or_404(House, name=house_name)
    employees = house.employee_set.all()
    context ={
        'emp' : employees
    }
    return render(request, 'basic_user/details.html',context)

   