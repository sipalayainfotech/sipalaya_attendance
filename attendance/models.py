from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username
    
    
    

class Instructor(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.employee.user.username
    
   
class Group(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Attendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'student')
    
    def __str__(self):
        return self.student.name
        
    

class StudentAttendanceSummary(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    total_present_days = models.PositiveIntegerField(default=0)
    total_absent_days = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.student.name
