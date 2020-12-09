from django.db import models
from PIL import Image
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.db.models.signals import post_save
from django.dispatch import receiver  
from django.shortcuts import get_object_or_404
from django.db.models import Sum

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=30)
    # points = models.IntegerField(default=0)
    house = models.ForeignKey('House',on_delete=models.CASCADE)
    # remarks =  models.CharField(max_length=100, default="no remarks now")

    def __str__(self):
        return self.name

    # not needed
    

    # @property
    # def own_ponits(self):
    #     employees = Employee.objects.filter(house=self)
    #     for e in employees:
    #         det = [self.name, self.points,self.house, self.designation]
    #     return det
        
class Point(models.Model):
    employee = models.ForeignKey(Employee,on_delete= models.CASCADE)
    value = models.IntegerField(default=0)
    remarks = models.TextField(max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        # is_new = True if not self.id else False
        h=self.employee.house
        before = h.get_rank()
        # print(before)
        super(Point, self).save(*args, **kwargs)
        after = h.get_rank()
        # print(after)
        log = Logger(emp=self.employee, remarks=f"Point changed: {self.value} {self.remarks} Before point update house rank was {before}, after points update house rank is {after}")
        log.save()


class House(models.Model):
    name = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    pic = models.ImageField(default='default.jpg', upload_to ='profile_pics')

    def __str__(self):
        return self.name
    
    def get_rank(self) -> int:
        houses = House.objects.annotate(point=Sum("employee__point__value")).order_by('-point').values_list("id", flat=True)

        house_list = []
        for x in houses:
            house_list.append(x)
    
        rank = house_list.index(self.id)
        
        return rank + 1

    
    # @property
    # def point(self) : 
    #     employees = Employee.objects.filter(house=self)
    #     points = 0
    #     for employee in employees:
    #         points += employee.points
    #     self.points=points
    #     self.save()
        
    #     return points
class Logger(models.Model):
    emp = models.ForeignKey('Employee', on_delete= models.CASCADE)
    remarks =  models.CharField(max_length=100, default="no remarks now")
    date_and_time = models.DateTimeField(auto_now=True)
    # house_rank =  models.IntegerField(default=0)
    # house_updated_points = models.IntegerField(default=0)


    def __str__(self):
        return self.remarks

    # @property
    # def taking_log(self, Employee):
    #     emp_obj = Employee.objects.filter(id=self.emp)
    #     # logger_obj = Logger.objects.filter(self.emp=emp_obj.id)
    #     # logger_obj.remarks=emp_obj.remarks
    #     self.remarks = emp_obj.remarks
    #     self.save()

    #     return self.remarks

    # def save(self, *args, **kwargs):
    #     if self.pk is None:  
    #         e = Employee()
    #         self.emp = e.id
    #         self.remarks = e.remarks
    #     super(self).save(*args, **kwargs)  
