# 3rd party
from rq import Connection, Queue, Worker
from redis import Redis
from email.mime.text import MIMEText

# my project
from Bomber.models import *
from toolkit.singleton import *
from .clients import *


# defining aa custom rq worker that runs on its own process
from multiprocessing import Process
class ProcessWorker(Process):

	def __init__(self, queues, name):
		super(ProcessWorker,self).__init__()
		self.worker = Worker(queues, name)

	def run(self):
		# burst mode should force the worker
		# and the process to shutdown once the queue is empty
		self.worker.work(burst=True)


@Singleton
class Manager(object):

	@staticmethod
	def get_spoofs(self):
		return Spoof.objects.all()

	"""
		The manager handles distributing the email tasks across queues.
		We always want the same manager regardless of requesting thread
	"""
	@staticmethod
	def queue_emails(message, count):
		queues = []
		available_spoofs = [spoof for spoof in Spoof.objects.all()]
		number_of_spoofs = len(available_spoofs)
		messages_per_queue = count // number_of_spoofs
		extra = count - (messages_per_queue * number_of_spoofs)

		# going deep into each queue
		for x in range(number_of_spoofs):

			spoof = available_spoofs[x]
			queue = Queue(spoof.username, connection=Redis())
			queues.append(queue)

			for y in range(messages_per_queue):
				queue.enqueue_call(func=send,args=(
							  spoof.domain.host,
							  spoof.domain.port,
							  spoof.username,
							  spoof.password,
							  spoof.rate_limit,
							  message))

		# panning across each queue
		for x in range(extra):
			spoof = available_spoofs[x]
			queue = queues[x]
			queue.enqueue_call(func=send,args=(
							  spoof.domain.host,
							  spoof.domain.port,
							  spoof.username,
							  spoof.password,
							  spoof.rate_limit,
							  message))



	@staticmethod
	def start_work(queue_names):

		# Provide queue names to listen to as arguments to this script,
		with Connection():

			current_workers = Worker.all()
			working_queues = [queue.name for worker in current_workers for queue in worker.queues]
			queues_to_start = [queue for queue in queue_names if not queue in working_queues]

			if len(queues_to_start) > 0:
				for queue in queues_to_start:

					# starting a separate worker process for each queue
					t = ProcessWorker([Queue(queue)], queue)
					t.run()
			else:
				print("Nothing to do here.")

def run(queue_names):

	payload = MIMEText('This is a sample message.')
	payload['Subject'] = 'Test'
	payload['From'] = 'paul.v.rutledge@gmail.com'
	payload['To'] = 'paul.v.rutledge@gmail.com'

	m = Manager()
	m.queue_emails(payload, 20)
	m.start_work(queue_names)