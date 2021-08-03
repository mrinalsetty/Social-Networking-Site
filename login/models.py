from django.db import models
from django.db.models.fields import AutoField, IntegerField

# Create your models here.
class users(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    name =  models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_no = models.CharField(max_length=15)
    dob = models.DateField()
    password = models.CharField(max_length=300)
    date_joined =models.DateField()
    otp = models.IntegerField(default=000000)
    image = models.ImageField(upload_to='img/%y',default='/media/default-profile-picture.jpg')
    bio = models.TextField(default="")

class posts(models.Model):
    image_id=AutoField(primary_key=True)
    image= models.ImageField(upload_to='img/%y',default='')
    username=models.ForeignKey(users,on_delete=models.CASCADE)
    upload_time=models.DateTimeField()
    des=models.TextField(null=True)

class friends(models.Model):
    f_id=AutoField(primary_key=True)
    username=models.ForeignKey(users,on_delete=models.CASCADE)
    f_username=models.CharField(max_length=100)
    


