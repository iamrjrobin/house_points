from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Max, Min, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from basic_user.forms import SignUpForm

from .models import Employee, House, Logger, Point
from .serializers import (Emp_Self_Patch_Serializer, Emp_Serializer, Emp_SerializerForPatch,
                          House_Serializer, Logger_Serializer,
                          Login_Serializer, Point_Serializer,
                          SignUp_Serializer)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, f'Account created for {username}!')
            return redirect('show')
    else:
        form = SignUpForm()
    return render (request, 'basic_user/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            return redirect ('show')
    else:
        form = AuthenticationForm()
    return render(request, 'basic_user/login.html', {'form':form})



def display(request):
    house = House.objects.annotate(pnt=Sum("employee__point__value")).order_by('-pnt')
    for h in house:
        h.points()
    query = request.GET.get("q")
    if query:
        house =house.filter(name__icontains=query)
    context = {
        'house' : house
    }
    return render (request, 'basic_user/show.html',context)

def details(request, house_id):
    house= get_object_or_404(House, id=house_id)
    employees = Employee.objects.filter(house=house)
    for employee in employees:
        employee.own_ponits()
    employees = Employee.objects.filter(house=house).annotate(p=Sum("point__value")).order_by('-p')
    query = request.GET.get("q")
    query_min = request.GET.get("q_min")
    query_max = request.GET.get("q_max")
    if query:
        employees =employees.filter(name__icontains=query)

    if query_max:
        employees = employees.filter(points__lte= query_max)
    if query_min:
        employees = employees.filter(points__gte=query_min)
    context= {
        'emp' : employees
    }
    return render(request, 'basic_user/details.html',context)

def taking_logs(request):
    log = Logger.objects.all().order_by('-date_and_time')
    house =  House.objects.all().order_by('-point')
    context={
        'log' : log,
        'house' : house
    }
    return render(request, 'basic_user/logs.html', context)

def single_log(request, employee_id):
    emps = get_object_or_404(Employee, id=employee_id)
    logs = Logger.objects.filter(emp=emps.id).order_by('-date_and_time')
    house = House.objects.annotate(pnt=Sum("employee__point__value")).order_by('-point')
    context = {
        'logs' : logs,
        'house' : house
    }
    return render(request, 'basic_user/single_log.html', context)


#api section
#
#
#

@api_view(['POST',])
@permission_classes((AllowAny,))
def api_signup(request):
    if request.method == 'POST':
        ser = SignUp_Serializer(data=request.data)
        data = {}
        if ser.is_valid():
            account = ser.save()
            token = Token.objects.get(user=account).key
            data['username'] = ser.data.get('username')
            data['first_name'] = ser.data.get('first_name')
            data['email'] = ser.data.get('email')
            data['token'] = token
            return JsonResponse(data, status = status.HTTP_201_CREATED)
        return Response(ser.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_display(request):
    if request.method == 'GET':
        house = House.objects.all().order_by('-point')
        ser = House_Serializer(house, many= True)
        return Response(ser.data)

    elif request.method == 'POST':
        if not request.user.is_superuser:
            return Response('You are not allowed to add new house')
        ser = House_Serializer(data=request.data)

        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status = status.HTTP_201_CREATED)
        return Response(ser.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_details(request, house_id):
    if request.method == 'GET':
        house= get_object_or_404(House, id=house_id)
        employees = Employee.objects.filter(house=house).order_by('-points')
        ser = Emp_Serializer(employees, many = True)
        return Response(ser.data)

class Emp_list_view(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = Emp_Serializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = {
        'points': ['lte','gte']
    }
    search_fields = ['name']

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_all_emp(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        ser = Emp_Serializer(employees, many = True)
        return JsonResponse(ser.data, safe=False)

    elif request.method =='POST':
        if not request.user.is_superuser:
            return Response('You are not allowed to add new employee')
        ser = Emp_Serializer(data=request.data)

        if ser.is_valid():
            print(ser.validated_data)
            ser.save()
            return JsonResponse(ser.data, status = 201)
        return JsonResponse(ser.errors, status = 400)


@api_view(['PUT','PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_all_emp_update(request,employee_id):
    try:
        employees = Employee.objects.get(id = employee_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        ser = Emp_Serializer(employees,data = request.data)
        data = {}
        if ser.is_valid():
            ser.save()
            data["success"]= "update successful"
            return JsonResponse(ser.data, status =201)
        return JsonResponse(ser.errors,status=400)

@api_view(['PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_all_emp_partial_update(request, house_id,employee_id):
    if not request.user.is_superuser:
        return Response('You are not allowed to update employee')
    try:
        employees = Employee.objects.get(id = employee_id,house = house_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        ser = Emp_SerializerForPatch(employees,data=request.data, partial=True)
        data = {}
        if ser.is_valid():
            ser.save()
            data["success"]= "patch successful"
            return JsonResponse(ser.data, status =201)
        return JsonResponse(ser.errors,status=400)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_points(request):
    if request.method == 'GET':
        if not request.user.is_superuser:
            return Response("You are not allowed see everyone's points")
        points = Point.objects.all()
        ser = Point_Serializer(points, many=  True)
        return JsonResponse(ser.data, safe =False)

    elif request.method == 'POST':
        if not request.user.is_superuser:
            return Response("You are not allowed assign points")
        # data = JSONParser().parse(request)
        ser = Point_Serializer(data=request.data)

        if ser.is_valid():
            print(ser.validated_data)
            point_update = Point.objects.filter(
                employee=ser.validated_data.get('employee').id)
            new_point = 0
            house_id = 0
            for p in point_update:
                new_point = p.value + new_point
                house_id = p.employee.house.id
            Employee.objects.filter(id=ser.validated_data.get(
                'employee').id).update(points=new_point)

            house_emps = Employee.objects.filter(house=house_id)
            new_house_point = 0
            for rank in house_emps:
                new_house_point = rank.points + new_house_point

            House.objects.filter(id=house_id).update(point=new_house_point)
            ser.save()

            return JsonResponse(ser.data, status = status.HTTP_201_CREATED)
        return Response(ser.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def api_taking_logs(request):
    if request.method == 'GET':
        if not request.user.is_superuser:
            return Response("You are not allowed see logs")
        log = Logger.objects.all().order_by('-date_and_time')
        ser = Logger_Serializer(log, many = True)
        return JsonResponse(ser.data,safe = False)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def api_single_log(request):
    if request.method == 'GET':
        emps = get_object_or_404(Employee, id=request.user.employee.id)
        logs = Logger.objects.filter(emp=emps.id).order_by('-date_and_time')
        ser = Logger_Serializer(logs, many = True)
        return JsonResponse(ser.data, safe = False)

@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def api_emp_self_patch(request):
    if request.method == 'PATCH':
        emps = get_object_or_404(Employee, id=request.user.employee.id)
        ser = Emp_Self_Patch_Serializer(emps, data=request.data, partial = True)
        data = {}
        if ser.is_valid():
            ser.save()
            data["success"] = "patch successful"
            return JsonResponse(ser.data, status=201)
        return JsonResponse(ser.errors, status=400)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def api_single_log_admin(request, employee_id: int):
    if request.method == 'GET':
        if not request.user.is_superuser:
            return Response("Normal users cannot see logs like this")
        emps = get_object_or_404(Employee, id=employee_id)
        logs = Logger.objects.filter(emp=emps.id).order_by('-date_and_time')
        ser = Logger_Serializer(logs, many=True)
        return JsonResponse(ser.data, safe=False)
