from enum import Enum
from .mixins import *
from Meta.plugins import *

def build_param_message(missing_params):
	return "The following parameters were missing: {0}".format(", ".join(missing_params))


class Param(object):

	class TYPE(Enum):
		NUMBER = 'number'
		STRING = 'string'
		OBJECT = 'object'
		NUMBER_ARRAY = 'number[]'
		STRING_ARRAY = 'string[]'
		OBJECT_ARRAY = 'object[]'

	def __init__(self, name, type, required=True, default=None):
		self.name = name
		self.type = type
		self.default = default
		self.required = required

	def dictify(self):
		definition = {'name': self.name, 'type': self.type.value, 'required': self.required}
		if self.default:
			definition['default'] = self.default
		return definition


'''
	This CommandHandlerBase class contains the bulk of dealing with the static data
	associated with a CommandHandler. The static fields allow us to:

	1) dispatch to the appropriate CommandHandler,

	2) perform existence and type validation of the data in the request

	3) check that the user has appropriate permissions to make a request for the
	   execution of a particular command

	4) provide a basic definition of the command to the front end so that
	   it can perform validation upfront and also minimize the number of
	   synchronization points between front end code and backend, since
	   the backend drives the available commands for the front end as well.

	The last thing that this class provides, is simply a #handle method that should
	be overridden in each of the command handlers in order actually process a request.
'''
@Plugin(key='command_name', module='commands')
class CommandHandlerBase(AjaxMixin):

	# the canonical name for the command
	command_name = ''

	# whether or not the command requires a user to be authenticated
	auth_required = False

	# a list of params.
	params = []

	# a list of required user permissions for a command
	required_permissions = []

	# checks that the user on the request is logged in if 'authenticated' is a necessary permission
	@classmethod
	def validate_auth(cls, request):
		return request.user.is_authenticated() if cls.auth_required else True


	# checks that the user on the request has the necessary permissions for the command
	@classmethod
	def validate_permissions(cls, request):
		return request.user.has_perms(cls.required_permissions)


	# checks that the necessary parameters were provided with the command data
	@classmethod
	def validate_params(cls, command_data):
		missing = [param.name for param in cls.params if (param.required) and (param.name not in command_data)]
		if len(missing) > 0: return False, build_param_message(missing)
		return True, ''


	# gets a simple serializable definition of the command
	@classmethod
	def to_definition(cls):
		return {'name': cls.command_name, 'params': [param.dictify() for param in cls.params]}


	# just a placeholder, but implementations should handle the actual incoming command and return a HTTP response
	def handle(self, request, command_data):
		raise NotImplementedError("The default handle method was not overridden by the custom handler.")