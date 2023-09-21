from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

User._meta.get_field("email")._unique = True


class Documents(models.Model):
    document = models.FileField(unique=True)
    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class UserKeys(models.Model):
    key = models.CharField(blank=False, null=False, max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    queries_limit = models.IntegerField(default=0)
    documents_limit = models.IntegerField(default=0)
    reset_time = models.DateTimeField()
