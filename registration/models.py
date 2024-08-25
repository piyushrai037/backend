from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from firebase_admin import storage
from django.db import models
from django.core.files.base import ContentFile
import tempfile
from django.contrib.auth.models import AbstractUser

class Blog(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()  # This will store the content as text
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to='students/')
    branch = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

class Classroom(models.Model):
    code = models.CharField(max_length=100, blank=True)
    students = models.ManyToManyField(Student, blank=True)
    name = models.CharField(max_length=255, null=True)    # rest of the fields
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(length=10)
        super().save(*args, **kwargs)

class Resource(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

class Lecture(models.Model):
    name = models.CharField(max_length=255)
    response = models.JSONField()
    date_time = models.DateTimeField(auto_now_add=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

class Attendance(models.Model):
    date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    status = models.BooleanField()