from tkinter import CASCADE
from django.db import models
from django.forms import CharField, DateTimeField, Textarea
from django.contrib.auth.models import User 
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    images = models.ImageField(null=True, blank=True, upload_to="static/images/news")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

class Contact(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=400)
    message = models.TextField()

    def __str__(self):
        return self.subject[0:50]   