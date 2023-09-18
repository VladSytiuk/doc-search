from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

User._meta.get_field("email")._unique = True


class Documents(models.Model):
    document = models.FileField(unique=True)
    title = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
