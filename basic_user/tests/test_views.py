import pytest
from django.test import TestCase, Client
# from .serializers import House_Serializer, Emp_Serializer, Logger_Serializer, Point_Serializer,Emp_SerializerForPatch
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from basic_user.models import Employee, Point, House, Logger
import json
from django.shortcuts import render, redirect
from basic_user import views
from django.test import RequestFactory
from mixer.backend.django import mixer
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
        req = RequestFactory().get('/')
        obj = mixer.blend('basic_user.House')
        req.user = AnonymousUser()
        resp = views.api_display(req)
        assert resp.status_code == 200, 'Should be callable by anyone'
    
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