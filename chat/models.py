from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ChatMessage(models.Model):
    sender = models.CharField(max_length=100, default=None)
    content = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Notification(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    seen = models.BooleanField(default=False)
