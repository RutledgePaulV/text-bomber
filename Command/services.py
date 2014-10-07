from threading import local
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from Command.loader import *
from Command.base import *
import inspect
import json

_local = local()


'''
	Django actually doesn't have a well supported way of describing singleton services.
	So, we spin up a thread specifically for services upon which to instantiate them. And
	provide a single method #get that always returns the same instance per thread for the service.
'''
class Service(object):

	@classmethod
	def get(cls):
		if not hasattr(_local, cls.__name__):
			setattr(_local,cls.__name__, cls())
		return getattr(_local, cls.__name__, None)



'''
	This service exists to index the available commands by scanning the commands package and
	provide a way of routing to the correct command class based on the command name received
	by the front end code.

	This is best expressed as a singleton service because of the meta level inspection that
	needs to be done to read the available handlers. This *could* be an expensive operation
	that kills performance if changed to a prototype scope.
'''
class CommandService(Service):

	# a dictionary that maps command names to the actual command handler class
	dispatch_map = {}

	# the name of the field at which command handlers should specify their callable name.
	command_name_field = 'command_name'

	# when we instantiate the service, we load available commands into the dict.
	def __init__(self):
		for module in load_from_apps():
			for name,obj in inspect.getmembers(module, inspect.isclass):
				if obj is not CommandHandlerBase and issubclass(obj, CommandHandlerBase):
					command_name = getattr(obj, self.command_name_field)
					if not command_name in self.dispatch_map:
						self.dispatch_map[command_name] = obj
					else:
						message = 'Multiple definitions provided for {0} in the commands package.'
						raise Exception(message.format(command_name))

	# used to retrieve a set of all commands and their required parameters
	def get_all_definitions(self):
		return [command.to_definition() for command in self.dispatch_map.values()]

	# used to retrieve a set of commands based on a particular user's permissions
	def get_available_definitions(self, request):
		return [command.to_definition() for command in self.dispatch_map.values()
		        if command.validate_permissions(request) and command.validate_auth(request)]

	# method to check if a handler exists for the command
	def has_handler(self, command_name):
		return command_name in self.dispatch_map

	# handles the dispatching and execution of a command
	def dispatch(self, request, command_data):

		# retrieving the name of the command
		command_name = command_data.pop('command')[0]

		# retrieving the class for the command handler
		handler_class = self.dispatch_map[command_name]

		# First, check if the user needs to be authenticated
		has_necessary_auth = handler_class.validate_auth(request)
		if not has_necessary_auth:
			message = "You must be an authenticated user to perform the requested command."
			return HttpResponse(status=401, content=message)
		# End authentication check.

		# Next, check will be for the necessary permissions
		has_perms = handler_class.validate_permissions(request)
		if not has_perms:
			message = "Your user does not have the correct permissions for the requested command."
			return HttpResponseForbidden(message)
		# End permissions check.

		# Lastly, check if request data is valid for the handler
		valid, message = handler_class.validate_params(command_data)
		if not valid:
			return HttpResponseBadRequest(message)
		# End valid request data check


		'''
			Once we get here, everything that can be known outside of the specific business logic
			for their request has been validated. It is still possible for the command to not
			succeed, but that part must be handled by the command handler itself and cannot be
			reasonably determined via meta-data from the static context.
		'''

		# nothing more can be done off of the static class definition, so go ahead and instantiate
		handler = handler_class()

		# pass responsibility off to the actual handle method
		result = handler.handle(request, command_data)

		# returning the actual HTTP response
		return JsonResponse(result)