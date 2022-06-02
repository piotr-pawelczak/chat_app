from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    @classmethod
    def create(cls, username, content, thread_name):
        sender = User.objects.get(username=username)
        ChatMessage.objects.create(sender=sender, content=content, thread_name=thread_name)


class Notification(models.Model):
    sender = models.ForeignKey(User, related_name='sender_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver_notifications', on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    @classmethod
    def create(cls, sender, receiver):
        Notification.objects.create(sender_id=sender, receiver_id=receiver)

    @classmethod
    def mark_as_not_seen(cls, sender, receiver):
        notification = Notification.objects.get(sender_id=sender, receiver_id=receiver)
        notification.seen = False
        notification.save()

    @classmethod
    def mark_as_seen(cls, sender, receiver):
        if Notification.objects.filter(sender_id=sender, receiver_id=receiver).exists():
            notification = Notification.objects.get(sender_id=sender, receiver_id=receiver)
            notification.seen = True
            notification.save()
