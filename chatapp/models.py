from django.db import models

class ChatMessage(models.Model):
    message = models.TextField()
    response = models.TextField()
    topic = models.CharField(max_length=100, default="default_topic")
    system = models.CharField(max_length=100, default="default_system")
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)  # New score field

    def __str__(self):
        return self.message