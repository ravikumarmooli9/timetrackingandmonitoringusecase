from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    estimated_time = models.DurationField(help_text="Estimated time to complete the task")

    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def duration(self):
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return None

    def __str__(self):
        return f"{self.user} - {self.task} ({self.start_time} to {self.end_time})"

class LeaveRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approved = models.BooleanField(default=False)  # <-- Add this line

    def __str__(self):
        return f"{self.user} Leave: {self.start_date} to {self.end_date}"
