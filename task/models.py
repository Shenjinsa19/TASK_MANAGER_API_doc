from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.db import models

class Task(models.Model):
    STATUS_CHOICES=[
        ('Pending','Pending'),
        ('Completed','Completed')
    ]
    title=models.CharField(max_length=100)
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='Pending')
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    class Meta:
        verbose_name="Task"
        verbose_name_plural="Task"

    def __str__(self):
        return self.title

        
