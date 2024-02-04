from django.db import models
#this is used to create users (we will extend the user we make to this abstract user)
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    #django logs in with username and password but if we do this we can use email and password
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Task(models.Model):
    #on_delete=models.CASCADE means if a room gets deleted so does all the children (the messages)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField(null=True)
    isCompleted = models.BooleanField()
    completedBy = models.DateField()
    updated = models.DateTimeField(auto_now=True)#this means anytime the save method is called take a DateTime snapshot
    created = models.DateTimeField(auto_now_add=True) #this takes a snapshot when the instance of this class is created