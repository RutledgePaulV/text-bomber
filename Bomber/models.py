from django.db import models

# represents an account for sending emails from
# having lots of these lets us get around things
# like rate limits.
class Spoof(models.Model):
	username = models.EmailField()
	password = models.CharField(max_length=255)
	domain = models.ForeignKey('SpoofDomain')

	def __str__(self):
		return self.username

# represents a supported email service that can be used to send the emails
class SpoofDomain(models.Model):
	host = models.CharField(max_length=255)
	port = models.PositiveIntegerField()

	def __str__(self):
		return self.host

# a provider represents a cellular provider
class Provider(models.Model):
	name = models.CharField(max_length=255)
	gateway_domain = models.CharField(max_length=255)

	def __str__(self):
		return self.name