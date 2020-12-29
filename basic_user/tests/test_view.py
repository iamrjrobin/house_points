from django.test import TestCase, Client
from django.urls import reverse
from basic_user.models import Employee, House, Logger
import json

# class TestViews(TestCase):

#     def test_emp_list_GET(self):
#         client = Client()

#         response = client.get(reverse)