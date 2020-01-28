from django.db import models
from django.utils import timezone


# Create your models here.

class Membre(models.Model):
    nom=models.CharField(max_length=50)


class discussion(models.Model):
    discussion=models.ForeignKey(Membre, on_delete=models.CASCADE)
    discussion_recv=models.CharField(max_length=50, null=True)
    discussion_send=models.CharField(max_length=50, null=True)
    disc_date=models.DateTimeField(timezone.now)


