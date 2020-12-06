from django.db import models
from PIL import Image
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.db.models.signals import post_save
from django.dispatch import receiver  

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
        super(Point, self).save(*args, **kwargs)
        log = Logger(emp=self.employee, remarks= f"Point changed: {self.value}")
        log.save()


class House(models.Model):
    name = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    pic = models.ImageField(default='default.jpg', upload_to ='profile_pics')

    def __str__(self):
        return self.name
    

    
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
    # class ActionChoice(models.IntegerChoices):
    #     PointAction = 1   
    emp = models.ForeignKey('Employee', on_delete= models.CASCADE)
    remarks =  models.CharField(max_length=100, default="no remarks now")
    # action = models.IntegerField(choices=ActionChoice.choices)
    date_and_time = models.DateTimeField(auto_now=True)
    # house_updated_points = models.IntegerField(default=0)


    # def __str__(self):
    #     return self.emp

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
