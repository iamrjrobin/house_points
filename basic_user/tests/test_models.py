from mixer.backend.django import mixer
from django.contrib.auth.models import User
from basic_user.models import Employee, House, Logger, Point
import pytest
pytestmark = pytest.mark.django_db

class TestModels:
    def test_employee(self):
        obj = mixer.blend('auth.User', is_superuser = False)
        # emp_obj = mixer.blend('basic_user.Employee')
        object = mixer.blend('basic_user.House')
        # point_obj = mixer.blend('basic_user.Point')
        assert (obj.employee.__str__()== obj.username)
        assert obj.pk == 1, 'Should create a post instance'


        # def own_ponits(self):
        #     employees = Point.objects.filter(employee=self)
        # points = 0
        # for e in employees:
        #     points += e.value
        # self.points=points
        # self.save()