from commands.base import *
from Bomber.models import *
from random import randint
from email.mime.text import MIMEText

from Email.manager import *

class QueueTexts(CommandHandlerBase):

	command_name = 'QUEUE_TEXTS'

	params = [
		Param('number', Types.STRING),
		Param('message', Types.STRING),
		Param('provider', Types.INTEGER),
		Param('count', Types.INTEGER)
	]

	manager = Manager()

	def handle(self, request, data):

		address = self.get_email_for_provider(data.number, data.provider)
		message = self.create_message(address, data.message)

		spoofs = Spoof.objects.all()
		batch_pk = self.manager.queue_emails(spoofs, message, data.count)
		self.manager.start_work([spoof.username for spoof in spoofs])

		return self.success({'batchPk': batch_pk})

	def create_message(self, address, contents):
		message = MIMEText(contents)
		message['To'] = address
		message['Subject'] = 'h4x'
		return message

	def get_email_for_provider(self, number, provider):
		provider = Provider.objects.get(pk=provider)
		return provider.get_address_from_number(number)


class GetProgress(CommandHandlerBase):

	command_name = 'GET_PROGRESS'
	params = [Param('batchPk', Types.INTEGER)]

	def handle(self, request, data):
		batch = Batch.objects.get(pk=data.batchPk)
		return self.success({'percent': batch.percent_complete})