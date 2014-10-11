from django.views.generic import View
from .services import *

'''
	This controller is responsible for receiving commands to execute
	and appropriately dispatching them to the correct handler strategy.
'''
class CommandHandler(View, AjaxMixin):

	service = CommandService()

	# Right now we're not taking advantage of other HTTP methods.
	def get(self, request, *args, **kwargs):
		return self.error("Get requests are not supported for this endpoint.")

	def post(self, request, *args, **kwargs):
		# dispatch the request to the appropriate handler along with a mutable copy of the POST contents
		return self.service.dispatch(request, request.POST.copy())


'''
	This controller is responsible for describing the various commands to the
	front end so that it can perform validation before a command is actually
	executed, thus preventing server errors due to malformed requests.
'''
class AllCommandDefinitions(View, AjaxMixin):

	service = CommandService()

	def get(self, request, *args, **kwargs):
		all_commands = self.service.get_all_definitions()
		return self.success(all_commands)

	def post(self, request, *args, **kwargs):
		return self.error("Post requests are not supported for this endpoint.")


'''
	This controller is responsible for describing the commands
	that are available to a particular user based on their authentication
	and various permissions.
'''
class AvailableCommandDefinitions(View, AjaxMixin):

	service = CommandService()

	def get(self, request, *args, **kwargs):
		commands = self.service.get_available_definitions(request)
		return self.success(commands)

	def post(self, request, *args, **kwargs):
		return self.error("Post requests are not supported for this endpoint.")