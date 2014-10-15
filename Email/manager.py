from Bomber.models import *
from toolkit.singleton import *
from redis import Redis
from rq import Connection, Queue, Worker
import time

class Server():

	def send_message(self, message):
		print(message)
		time.sleep(1)

@Singleton
class Manager(object):
	"""
		The manager handles distributing the email tasks across queues.
	"""
	def queue_emails(self, message, count):

		queues = []
		available_spoofs = ['jerry', 'cambodia']
		number_of_spoofs = len(available_spoofs)
		messages_per_queue = count // number_of_spoofs
		extra = count - (messages_per_queue * number_of_spoofs)
		server = Server()

		# going deep into each queue
		for x in range(number_of_spoofs):

			spoof = available_spoofs[x]
			queue = Queue(spoof, connection=Redis())
			queues.append(queue)

			for y in range(messages_per_queue):
				queue.enqueue(server.send_message, "{0} - {1}".format(x,y))

		# panning across each queue
		for x in range(extra):
			queue = queues[x]
			queue.enqueue(server.send_message, message)


	def start_work(self, queue_names):

		# Provide queue names to listen to as arguments to this script,
		with Connection():

			current_workers = Worker.all()
			working_queues = [queue.name for worker in current_workers for queue in worker.queues]
			queues_to_start = [queue for queue in queue_names if not queue in working_queues]

			if len(queues_to_start) > 0:
				for queue in queues_to_start:

					# starting a separate worker process for each queue
					t = ProcessWorker(Queue[queue], queue)
					t.start()
			else:
				print("Nothing to do here.")


from multiprocessing import Process

class ProcessWorker(Process):

	def __init__(self, queues, name):
		super(ProcessWorker,self).__init__()
		self.worker = Worker(queues, name)

	def run(self):

		# burst mode should force the worker
		# and the process to shutdown once the queue is empty
		self.worker.work(burst=True)