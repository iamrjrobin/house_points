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
        response = self.client.post('/login/', {
            'username': username,
            'password': password,
        })
        return redirect ('/admin/')


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
        force_authenticate(req, user=user.pk, token=user.auth_token)
        resp = views.api_display(req)
        assert resp.status_code == 201, 'Should create new house'



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
        assert resp.status_code == 400, 'Both password must match'
    
    

    # def test_api_display_post(client):  
    #     client.login(username="foo", password="bar")
    #     response = client.get(url, follow=True)
    #     assert response.status_code == 200
    #     response = admin_client.get(url, follow=True)
    #     assert response.status_code == 200
    #     obj = mixer.blend('basic_user.House')
    #     data = {'name': 'tsetssdfa'}        
    #     req = RequestFactory().post('/', data=data)
    #     req.user = AnonymousUser()
    #     resp = views.api_display(req)
    #     assert resp.status_code == 302, 'Should be callable by anyone'
    #     obj.refresh_from_db()
    #     assert obj.name == 'tsetssdfa', 'Should be the new name'
