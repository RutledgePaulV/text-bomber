# 3rd party
from rq import Connection, Queue, Worker
from redis import Redis
from email.mime.text import MIMEText

# my project
from Bomber.models import *
from toolkit.singleton import *
from .clients import *


from multiprocessing import Process
class ProcessWorker(object):
	"""
		We're using the standard rq-worker but
		we offload each one into a different process
		so that there's no thread blocking inside the webapp
	"""


	def __init__(self, queue):
		super(ProcessWorker,self).__init__()
		worker = Worker([Queue(queue)], queue)
		self.process = Process(target=worker.work, args=(True,))

	def run(self):
		# TODO: improve error handling and process management
		self.process.start()

@Singleton
class Manager(object):
	"""
		The manager handles distributing the email tasks across queues.
		We always want the same manager regardless of requesting thread
	"""


	@staticmethod
	def queue_emails(spoofs, message, count):
		"""
			This method distributes a set of messages
			across each of the provided spoofs by assigning
			them to a separate queue for each.
		"""
		queues = []
		number_of_spoofs = len(spoofs)
		messages_per_queue = count // number_of_spoofs
		extra_to_distribute = count - (messages_per_queue * number_of_spoofs)

		# going deep into each queue
		for x in range(number_of_spoofs):

			spoof = spoofs[x]
			queue = Queue(spoof.username, connection=Redis())
			queues.append(queue)

			for y in range(messages_per_queue):
				queue.enqueue_call(func=send, args=spoof.task_arguments + (message,))

		# panning across each queue
		for x in range(extra_to_distribute):
			spoof = spoofs[x]
			queue = queues[x]
			queue.enqueue_call(func=send ,args=(spoof.task_arguments + (message,)))


	@staticmethod
	def start_work(queue_names):

		# Provide queue names to listen to as arguments to this script,
		with Connection():
			working_queues = [queue.name for worker in Worker.all() for queue in worker.queues]
			queues_to_start = [queue for queue in queue_names if not queue in working_queues]

			# if there's not already a worker for that queue name, then start one up!
			if len(queues_to_start) > 0:
				[ProcessWorker(queue).run() for queue in queues_to_start]