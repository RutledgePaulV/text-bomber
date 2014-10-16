from django.db import models

class Spoof(models.Model):
	"""
		Represents an account for sending emails
	"""
	username = models.EmailField()
	password = models.CharField(max_length=255)
	rate_limit = models.PositiveIntegerField()
	domain = models.ForeignKey('SpoofDomain')

	@property
	def task_arguments(self):
		return (
			self.domain.host,
			self.domain.port,
			self.username,
			self.password,
			self.rate_limit
		)

	def __str__(self):
		return self.username


class SpoofDomain(models.Model):
	"""
		Represents a supported email service
	"""
	host = models.CharField(max_length=255)
	port = models.PositiveIntegerField()

	def __str__(self):
		return self.host


class Provider(models.Model):
	"""
		Represents a known cell carrier and sms gateway
	"""
	name = models.CharField(max_length=255)
	gateway_domain = models.EmailField()

	def get_address_from_number(self, number):
		result = self.gateway_domain
		for digit in number:
			result = result.replace("#", digit, 1)
		return result

	def __str__(self):
		return self.name

class Batch(models.Model):

	size = models.PositiveIntegerField()
	complete = models.PositiveIntegerField()

	def increment(self):
		if(self.complete < self.size):
			self.complete = self.complete + 1
			self.save()

	@property
	def percent_complete(self):
		return self.complete / self.size