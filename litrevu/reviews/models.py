from django.db import models

# Create your models here.


class Review(models.Model):

    title = models.fields.CharField(max_length=200)
    description = models.fields.CharField(default="Vide", max_length=1600)
    image = models.ImageField(upload_to="")
