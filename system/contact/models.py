from django.db import models

# Create your models here.
class Message(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=1000)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return self.firstname
    