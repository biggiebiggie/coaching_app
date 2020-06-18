from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    tagname = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.tagname}"

class Stat(models.Model):
    statname = models.CharField(max_length=200)
    statvalue = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.statname} {self.statvalue}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    stat = models.ManyToManyField(Stat)

    def __str__(self):
        return f"{self.user}"

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    def __str__(self):
        return f"{self.user}"

class Team(models.Model):
    name = models.CharField(max_length=200)
    student = models.ManyToManyField(Student)
    coach = models.ManyToManyField(Coach)

    def __str__(self):
        return f"Team {self.id}"

