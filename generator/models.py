from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    email = models.EmailField()
    date_added = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name + ' '+ self.course