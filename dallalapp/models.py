from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Dhani(models.Model):
    Userid = models.AutoField(primary_key=True)  # post id
    fullname = models.CharField(max_length=50)
    address = models.CharField(max_length=50, default='')
    landimage = models.ImageField(upload_to='images/land_images', default='')
    phone_number = models.BigIntegerField()
    about = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    Type = models.CharField(max_length=20)
    quantity = models.FloatField()
    price = models.FloatField()

    created_at = models.CharField(max_length=50)

    User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname


class UserComments(models.Model):
    userid = models.AutoField(primary_key=True)  # actuall it is post id
    Comments = models.TextField()
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Dhani, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.Comments[:100]}...'
