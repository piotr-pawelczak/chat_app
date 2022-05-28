from django.db import models


# Create your models here.
class ChatMessage(models.Model):
    sender = models.CharField(max_length=100, default=None)
    content = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
