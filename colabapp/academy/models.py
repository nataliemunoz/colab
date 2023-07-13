from django.db import models
from django.contrib.auth.models import User #importa las caracterisitcas del modelo user

# Create your models here.

class Teacher(User):
    #first_name=models.CharField(max_length=128)
    #last_name=models.CharField(max_length=128)
    bio = models.CharField(max_length=500)

class Course(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500)

class Student(User):
    #first_name = models.CharField(max_length=128)
    #last_name = models.CharField(max_length=128)
    #email = models.CharField(max_length=128)
    pass

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    start_date = models.DateField()

class Subscription(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)




