from rest_framework import serializers
from .models import House, Employee, Logger, Point
from rest_framework import filters,generics

# class House_Serializer(serializers.Serializer):
#     name = serializers.CharField(max_length=50)
#     # points = serializers.IntegerField(default=0)
#     # rank = serializers.IntegerField(default=0)
#     pic = serializers.ImageField(default='default.jpg')

#     def create(self,validated_data):
#         return House.objects.create(validated_data)

#     def update(self, instace, validated_data):
#         instace.name = validated_data.get('name', instace.name)
#         # instace.points = validated_data.get('points', instace.points)
#         # instace.name = validated_data.get('name', instace.name) 
#         instace.pic = validated_data.get('pic', instace.pic)
#         return instace

class House_Serializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['name', 'point','pic']

class Emp_Serializer(serializers.ModelSerializer):
    # house = House_Serializer()
    class Meta:
        model = Employee
        fields = ['id','name', 'designation', 'points','house']

class Emp_SerializerForPatch(serializers.ModelSerializer):
    # house = House_Serializer()
    class Meta:
        model = Employee
        fields = ['name', 'designation','house']


class Logger_Serializer(serializers.ModelSerializer):
    # emp = Emp_Serializer()
    class Meta:
        model = Logger
        fields = ['emp', 'remarks','date_and_time']

class Point_Serializer(serializers.ModelSerializer):
    class Meta: 
        model = Point
        fields = ['employee','value','remarks']