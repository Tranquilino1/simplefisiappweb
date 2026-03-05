from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_group = models.BooleanField(default=False)
    participants = models.ManyToManyField(User, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('voice', 'Voice'),
        ('file', 'File'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True)
    msg_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'

class Attachment(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='attachment')
    file = models.FileField(upload_to='chat_attachments/')
    file_type = models.CharField(max_length=100) # e.g. "image/png" "audio/mp3"

    def __str__(self):
        return self.file.name
