from django.db import models
from django.utils import timezone 

class ReportProblem(models.Model):
    name = models.CharField(max_length=25)

    email = models.EmailField()

    problem = models.TextField()
    
    date_reported = models.DateTimeField(default=timezone.now)

