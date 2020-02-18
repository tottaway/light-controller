from django.db import models

# Create your models here.
class LightControllerProcess(models.Model):
    pid = models.IntegerField(blank=True, default=None, null=True)
    mode = models.CharField(max_length=50)
