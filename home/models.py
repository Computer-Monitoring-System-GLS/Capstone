# models.py
from django.db import models

class SSHCredential(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Consider encryption for production use

    def __str__(self):
        return f"{self.username}@{self.ip}"
