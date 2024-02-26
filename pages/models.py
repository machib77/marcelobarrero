from django.db import models
from django.urls import reverse

# Create your models here.


class ContactMessage(models.Model):
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
