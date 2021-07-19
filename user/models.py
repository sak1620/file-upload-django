from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserData(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False)
    
    title = models.CharField(max_length=150,blank=True)
    body = models.CharField(max_length=800)
    datetime = models.DateTimeField(auto_now_add=True)
    
    

    class Meta:
        db_table = 'user_data'

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    date_uploaded = models.DateTimeField(auto_now=True)
