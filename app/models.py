from django.db import models


class Documents(models.Model):
    document = models.FileField()
