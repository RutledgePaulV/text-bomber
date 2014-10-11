from .base import *
from .mixins import *
from Meta.singleton import *

'''
	This service exists to index the available commands by scanning the commands package and
	provide a way of routing to the correct command class based on the command name received
	by the front end code.
'''

@Singleton
class CommandService(AjaxMixin):

	# the name of the field at which command handlers should specify their callable name.
	command_name_field = 'command_name'

	# handlers
	handlers = CommandHandlerBase.registry

	# used to retrieve a set of all commands and their required parameters
	def get_all_definitions(self):
		return [command.to_definition() for command in self.handlers.values()]

	# used to retrieve a set of commands based on a particular user's permissions
	def get_available_definitions(self, request):
		return [command.to_definition() for command in self.handlers.values()
		        if command.validate_auth(request) and command.validate_permissions(request)]

	# method to check if a handler exists for the command
	def has_handler(self, command_name):
		return command_name in self.handlers

	# returns the appropriate handler
	def get_handler(self, command_name):
		return self.handlers[command_name]

	# handles the dispatching and execution of a command
	def dispatch(self, request, command_data):

		# make sure they actually specified a command in the request
		if not 'command' in request.POST:
			return self.error("No command parameter was received.", 400)

		# retrieving the name of the command
		command_name = command_data.pop('command')[0]

		# make sure a valid handler strategy exists.
		if not self.has_handler(command_name):
			return self.error("No command handler exists for the requested command", 400)

		# retrieving the class for the command handler
		handler_class = self.get_handler(command_name)

		# First, check if the user needs to be authenticated
		if not handler_class.validate_auth(request):
			return self.error("You must be an authenticated user to perform the requested command.", 401)
		# End authentication check.

		# Next, check will be for the necessary permissions
		if not handler_class.validate_permissions(request):
			return self.error("Your user does not have the correct permissions for the requested command.", 403)
		# End permissions check.

		# Lastly, check if request data is valid for the handler
		valid, message = handler_class.validate_params(command_data)
		if not valid: return self.error(message, 400)
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
		return handler.handle(request, command_data)