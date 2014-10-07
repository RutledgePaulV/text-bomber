from Command.base import *
from Command.decorators import *
from random import randint
from Bomber.models import *

def queue_messages(message, provider, count):
	return 100

def get_progress(task_id):
	return randint(0, 100)

class QueueTexts(CommandHandlerBase):

	command_name = 'QUEUE_TEXTS'

	required_params = [
		('number', PARAM_TYPE.STRING, ''),
		('message', PARAM_TYPE.STRING, ''),
		('provider', PARAM_TYPE.NUMBER, 0),
		('count', PARAM_TYPE.NUMBER, 0),
	]

	def handle(self, request, command_data):

		message = command_data['message']
		provider = command_data['provider']#Provider.objects.get(pk=command_data['provider'])
		count = command_data['count']

		task_id = queue_messages(message, provider, count)

		return self.success({'taskId':task_id})


class GetProgress(CommandHandlerBase):

	command_name = 'GET_PROGRESS'

	required_params = [
		('taskId', PARAM_TYPE.NUMBER, 0)
	]

	def handle(self, request, command_data):

		percentage = get_progress(command_data['taskId'])
		return self.success({'percentageComplete':percentage})