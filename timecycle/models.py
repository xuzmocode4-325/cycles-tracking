from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Day(models.Model):
    name = models.CharField(max_length=10)  # e.g., 'Monday'
    code = models.CharField(max_length=3)
    order = models.IntegerField(null=True)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class MetaCycle(models.Model):
    # user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    frequency =  models.ManyToManyField(Day)  # Many-to-many 

    class Meta:
        ordering = ['name']
        verbose_name = "Meta Cycle"
        verbose_name_plural = "Meta Cycles"


    def __str__(self):
        return f"{self.name}"


class Activity(models.Model):
    meta_cycle = models.ForeignKey(MetaCycle, related_name='activities', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['start_time']
        verbose_name = "activity"
        verbose_name_plural = "activities"

    def duration(self):
        # Combine the time with a date (using today's date for example)
        today = datetime.now().date()
        start_datetime = datetime.combine(today, self.start_time)
        end_datetime = datetime.combine(today, self.end_time)

        # Calculate the duration in minutes
        duration = (end_datetime - start_datetime).total_seconds() / 60
        
        return duration
    
    def __str__(self):
        return f"{self.name} ({self.meta_cycle}) from {self.start_time} to {self.end_time}"
