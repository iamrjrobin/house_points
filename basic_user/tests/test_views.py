import json

import pytest
from basic_user import views
from basic_user.models import Employee, House, Logger, Point
from basic_user.serializers import (Emp_Serializer, Emp_SerializerForPatch,
                                    House_Serializer, Logger_Serializer,
                                    Point_Serializer, SignUp_Serializer)
from django.contrib.auth.models import AnonymousUser, User
from django.shortcuts import redirect, render
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 force_authenticate)

pytestmark = pytest.mark.django_db


# class TestViews(TestCase):
    
#     # def setUp(self):
#     #     self.client = Client()
#         # self.display_url = reverse('show')
#         # self.details_url = reverse('details', args=['trial'])
#         # self.trial = Employee.objects.create(
#         #     user = 999,
#         #     name = 'trial',
#         #     designation = 'student',
#         #     points = 0,
#         #     house = 'trial_house' 
#         # )

#     def test_display_GET(self):
#         client = Client()
#         response = client.get(reverse('show'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'basic_user/show.html')
    
    # def test_details_GET(self):
    #     # req = RequestFactory().get('basic_user/details.html')
    #     client = Client()
    #     # trial = Employee.objects.create(
    #     #     user = 1,
    #     #     name = 'trial',
    #     #     designation = 'student',
    #     #     points = 0,
    #     #     house = 1
    #     # )
        
    #     # house_id = 1
    #     response = client.get(reverse('details', kwargs={'house_id':1}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'basic_user/1/details.html')
    #     # assert (house.objects.all().count() == 1, "Has house")
    #     # resp = views.details(req)
    #     # assert response.status_code == 200, '....'

class TestViews(TestCase):

    def test_login(self, username='testclient', password='password'):
        resp = self.client.post('/login/', {
            'username': username,
            'password': password,
        })
        

    def test_display(self):
        req = RequestFactory().get('basic_user/show.html')
        obj = mixer.blend('basic_user.House')
        resp = views.display(req)
        assert resp.status_code == 200, 'Should be callable by anyone'

    def test_details(self):
        req = RequestFactory().get('basic_user/details.html')
        obj = mixer.blend('basic_user.House')
        resp = views.details(req, house_id=obj.pk)
        assert resp.status_code == 200, 'Should show all emp points in that house'

    def test_taking_logs(self):
        req = RequestFactory().get('basic_user/logs.html')
        resp = views.taking_logs(req)
        assert resp.status_code == 200, 'Should be called by anyone'

    def test_single_log(self):
        req = RequestFactory().get('basic_user/single_log.html')
        obj = mixer.blend('auth.User', is_superuser = False)
        o = mixer.blend('basic_user.House')
        # ob = mixer.blend('basic_user.Employee')
        resp = views.single_log(req, employee_id=obj.pk)
        assert resp.status_code == 200, 'Should show all log of that employee'

#
#
#
#
#api tests


class TestApi(APITestCase):
    
    
    def test_api_display(self):
        req = APIRequestFactory().get('/')
        Ob = mixer.blend('auth.User', is_superuser = True)
        obj = mixer.blend('basic_user.House')
        req.user = AnonymousUser()
        resp = views.api_display(req)
        assert resp.status_code == 200, 'Should be callable by anyone'

        data = {"name": "testHouseName", "point": 0}
        user = User.objects.filter().first()
        req = APIRequestFactory().post('/',data, format = 'json')
        force_authenticate(req, user=user, token=user.auth_token)
        resp = views.api_display(req)
        assert resp.status_code == 201, 'Should create new house'

        data2 = {}
        req = APIRequestFactory().post('/',data2, format = 'json')
        force_authenticate(req, user=user, token=user.auth_token)
        resp = views.api_display(req)
        assert resp.status_code == 400, 'Invaild info'



    def test_api_signup(self):
        obj = mixer.blend('basic_user.House')
        data = {"username": "testusername", "first_name": "testname", "email": "test@loc.com", "password": "testing321", "password2": "testing321"}
        req = APIRequestFactory().post("api/signup", data, format='json')
        resp = views.api_signup(req)
        assert resp.status_code == 201, 'Should create a new user'
        # obj = mixer.blend('basic_user.House')
        data = {"username": "testusername", "first_name": "testname", "email": "test@loc.com", "password": "testing3321", "password2": "testing321"}
        req = APIRequestFactory().post("api/signup", data, format='json')
        resp = views.api_signup(req)
        assert resp.status_code == 400, 'Bad request. Both password must match'
        # data = {}
        # req = APIRequestFactory().post("api/signup", data, format='json')
        # resp = views.api_signup(req)
        # assert resp.status_code == 422, 'invalid data'
    
    def test_api_details(self):
        obj = mixer.blend('basic_user.House')
        req = APIRequestFactory().get('api/details/<obj.pk>')
        resp = views.api_details(req,house_id=obj.pk)
        assert resp.status_code == 200, 'Should be callable by belonging house'

    def test_api_all_emp(self):
        user = mixer.blend('auth.User')
        Employee.objects.first().delete()
        # ob = mixer.blend('basic_user.Employee')
        house = mixer.blend('basic_user.House')
        req = APIRequestFactory().get('api/show_all_emp/')
        resp = views.api_all_emp(req)
        assert resp.status_code == 200, 'Should be callable by anyone'

        data = {"user": user.pk, "name": "testNameEmp", "designation": "student", "points": 0, "house": house.pk}
        data=json.dumps(data)
        print(data)
        req = APIRequestFactory().post("api/show_all_emp/",data, content_type= "application/json")
        force_authenticate(req, user=user, token=user.auth_token)
        resp = views.api_all_emp(req)
        assert resp.status_code == 201, 'Should create new emp'   

        data = {}
        req = APIRequestFactory().post("api/show_all_emp/",data)
        force_authenticate(req, user=user, token=user.auth_token)
        resp = views.api_all_emp(req)
        assert resp.status_code == 400, 'Invalid data'


    def test_api_all_emp_update(self):
        user = mixer.blend('auth.User')
        o = mixer.blend('basic_user.House')
        data = {"user":user.pk,"name": "testHouseName","designation": "student", "points": 0, "house": o.pk}
        # user = User.objects.filter().first()
        req = APIRequestFactory().put('api/api_all_emp_update/<ob.pk>', data, format = 'json')
        force_authenticate(req, user=user,token=user.auth_token)
        resp = views.api_all_emp_update(req,employee_id=1)
        assert resp.status_code == 201, 'Should update'
   
    def test_api_all_emp_partial_update(self):
        user = mixer.blend('auth.User', )
        house = mixer.blend('basic_user.House')
        # employee = mixer.blend('basic_user.Employee', user=user, house=house)
        data = {"name": "testname", "designation": "Student", "house": house.id}
        req = APIRequestFactory().patch('api/api_all_emp_partial_update/<house.pk>/<employee.pk>', data)
        # print(req)
        force_authenticate(req, user=user, token= user.auth_token)
        resp = views.api_all_emp_partial_update(req, house_id=house.id, employee_id=1)
        assert resp.status_code == 201, "Should update"


    def test_api_taking_logs(self):
        user = mixer.blend('auth.User')
        house = mixer.blend('basic_user.House')
        logger = mixer.blend('basic_user.Logger', emp = Employee.objects.first())
        req = APIRequestFactory().get('api/logs')
        force_authenticate(req, user=user, token=user.auth_token)
        resp = views.api_taking_logs(req)
        assert resp.status_code == 200, "Should show all logs"

    def test_api_single_log(self):
        user = mixer.blend('auth.User')
        house = mixer.blend('basic_user.House')
        logger = mixer.blend('basic_user.Logger', emp = Employee.objects.first())
        req = APIRequestFactory().get('api/logs/single_logs/<employee.pk>')
        force_authenticate(req, user=user, token=user.auth_token)
        resp = views.api_single_log(req, employee_id=1)
        assert resp.status_code == 200, 'Should show log of an user'

    def test_api_points(self):
        user = mixer.blend('auth.User')
        house = mixer.blend('basic_user.House')
        points = mixer.blend('basic_user.Point', employee = Employee.objects.first())
        req = APIRequestFactory().get('api/api_points/')
        resp = views.api_points(req)
        assert resp.status_code == 200, 'Should show points'

        data = {"employee": user.pk, "value": 10, "remarks": "good employee"}
        req = APIRequestFactory().post("api/api_points/",data)
        force_authenticate(req, user=user, token=user.auth_token)
        resp = views.api_points(req)
        assert resp.status_code == 400, 'Invalid data'

        data = {"employee": user.pk, "value": 10, "remarks": "good employee"}
        data=json.dumps(data)
        print(data)
        req = APIRequestFactory().post("api/api_points/",data,content_type= "application/json")
        force_authenticate(req, user=user, token=user.auth_token)
        resp = views.api_points(req)
        assert resp.status_code == 201, 'Should add points'   

       
