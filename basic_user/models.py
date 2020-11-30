from django.db import models
from PIL import Image

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=30)
    points = models.IntegerField(default=0)
    house = models.ForeignKey('House',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # @property
    # def own_ponits(self):
    #     employees = Employee.objects.filter(house=self)
    #     for e in employees:
    #         det = [self.name, self.points,self.house, self.designation]
    #     return det
        


class House(models.Model):
    name = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    pic = models.ImageField(default='default.jpg', upload_to ='profile_pics')

    def __str__(self):
        return self.name
    
    @property
    def point(self) : 
        employees = Employee.objects.filter(house=self)
        points = 0
        for employee in employees:
            points += employee.points
        self.points=points
        self.save()
        
        return points
