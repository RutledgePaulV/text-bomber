from commands.base import *
from Bomber.models import *
from random import randint
from email.mime.text import MIMEText

from Email.manager import *

class QueueTexts(CommandHandlerBase):

	command_name = 'QUEUE_TEXTS'

	params = [
		Param('number', Param.TYPE.STRING),
		Param('message', Param.TYPE.STRING),
		Param('provider', Param.TYPE.STRING),
		Param('count', Param.TYPE.STRING)
	]

	manager = Manager()

	def handle(self, request, command_data):

		provider_pk = command_data['provider']
		contents = command_data['message']
		number = command_data['number']
		count = command_data['count']

		address = self.get_email_for_provider(number, provider_pk)
		message = self.create_message(address, contents)

		batch_pk = self.manager.queue_emails(Spoof.objects.all(), message, count)

		return self.success({'batchPk':batch_pk})


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
	params = [Param('batchPk', Param.TYPE.NUMBER)]

	def handle(self, request, command_data):
		batch_pk = command_data['batchPk']
		batch = Batch.objects.get(pk=batch_pk)
		return self.success({'percent': batch.percent_complete})