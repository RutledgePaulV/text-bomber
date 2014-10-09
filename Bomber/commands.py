from Command.base import *
from Command.decorators import *
from Bomber.models import *
from random import randint

def queue_messages(message, provider, count):
	return 100

def get_progress(task_id):
	return randint(0, 100)


class QueueTexts(CommandHandlerBase):

	command_name = 'QUEUE_TEXTS'

	params = [
		Param('number', Param.TYPE.STRING),
		Param('message', Param.TYPE.STRING),
		Param('provider', Param.TYPE.STRING),
		Param('count', Param.TYPE.STRING)
	]

	def handle(self, request, command_data):

		message = command_data['message']
		provider = command_data['provider']
		count = command_data['count']

		task_id = queue_messages(message, provider, count)

		return self.success({'taskId':task_id})


class GetProgress(CommandHandlerBase):

	command_name = 'GET_PROGRESS'
	params = [Param('taskId', Param.TYPE.NUMBER)]

	def handle(self, request, command_data):

		percentage = get_progress(command_data['taskId'])
		return self.success({'percentageComplete':percentage})