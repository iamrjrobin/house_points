from django.contrib.auth.models import User
from rest_framework import filters, generics, serializers

from .models import Employee, House, Logger, Point


class SignUp_Serializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_time': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'password2',]
        extra_kwarge = {
            'password' :{'write_only':True}
        }
    def save(self):
        employee = User(
            first_name = self.validated_data['first_name'],
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        employee.set_password(password)
        employee.save()
        return employee

class Login_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password',]
        

class House_Serializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['name', 'point','pic']

class Emp_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'id','name', 'designation', 'points','house']

class Emp_SerializerForPatch(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'designation','house']


class Logger_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Logger
        fields = ['emp', 'remarks','date_and_time']

class Point_Serializer(serializers.ModelSerializer):
    class Meta: 
        model = Point
        fields = ['employee','value','remarks']
