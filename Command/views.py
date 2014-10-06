from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View
from .services import *
import json

'''
	This controller is responsible for receiving commands to execute
	and appropriately dispatching them to the correct handler strategy.
'''
class CommandHandler(View):

	service = CommandService.get()

	# Right now we're not taking advantage of other HTTP methods.
	def get(self, request, *args, **kwargs):
		return HttpResponseBadRequest("Get requests are not supported for this endpoint.")

	def post(self, request, *args, **kwargs):

		# make sure they actually specified a command in the request
		if not 'command' in request.POST:
			return HttpResponseBadRequest("No command parameter was received.")

		# make sure a valid handler strategy exists.
		if not self.service.has_handler(request.POST['command']):
			return HttpResponseBadRequest("No command handler exists for the requested command")

		# dispatch the request to the appropriate handler along with a mutable copy of the POST contents
		return self.service.dispatch(request, request.POST.copy())


'''
	This controller is responsible for describing the various commands to the
	front end so that it can perform validation before a command is actually
	executed, thus preventing server errors due to malformed requests.
'''
class AllCommandDefinitions(View):

	service = CommandService.get()

	def get(self, request, *args, **kwargs):
		all_commands = self.service.get_all_definitions()
		return HttpResponse(json.dumps(all_commands), content_type='application/json')

	def post(self, request, *args, **kwargs):
		return HttpResponseBadRequest("Post requests are not supported for this endpoint.")

'''
	This controller is responsible for describing the commands
	that are available to a particular user based on their authentication
	and various permissions.
'''
class AvailableCommandDefinitions(View):

	service = CommandService.get()

	def get(self, request, *args, **kwargs):
		commands = self.service.get_available_definitions(request)
		return HttpResponse(json.dumps(commands), content_type='application/json')

	def post(self, request, *args, **kwargs):
		return HttpResponseBadRequest("Post requests are not supported for this endpoint.")