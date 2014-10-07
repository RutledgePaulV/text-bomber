from enum import Enum

from .mixins import *


def build_param_message(missing_params):
	return "The following parameters were missing: {0}".format(", ".join(missing_params))


# just a helper method to describe missing permissions.
def build_permissions_message(missing_permissions):
	return "The following permissions were missing: {0}".format(", ".join(missing_permissions))


'''
	Defining a parameter type enumeration to use when
    specifying the type a required parameter
'''


class PARAM_TYPE(Enum):
	NUMBER = 'number'
	STRING = 'string'
	OBJECT = 'object'
	NUMBER_ARRAY = 'number[]'
	STRING_ARRAY = 'string[]'
	OBJECT_ARRAY = 'object[]'


'''
	Defines an enumeration for the status key on a response.
'''


class STATUS(Enum):
	SUCCESS = 'SUCCESS'
	ERROR = 'ERROR'


'''
	This CommandHandlerBase class contains the bulk of dealing with the static data
	associated with a CommandHandler. The static fields allow us to: 1) dispatch
	to the appropriate CommandHandler, 2) perform existence and type validation of
	the data in the request, 3) check that the user has appropriate permissions
	to make a request for the execution of a particular command, and 4) provide
	a basic definition of the command to the front end so that it can perform
	validation upfront and also minimize the number of synchronization points
	between front end code and backend, since the backend drives the available
	commands for the front end as well.

	The last thing that this class provides, is simply a #handle method that should
	be overridden in each of the command handlers in order actually process a request.
'''


class CommandHandlerBase(AjaxResponse):
	# the canonical name for the command
	command_name = ''

	# a list of (name, PARAM_TYPE, default) tuples.
	required_params = []

	# a list of required user permissions for a command
	required_permissions = []

	# checks that the necessary parameters were provided with the command data
	@classmethod
	def validate_params(cls, command_data):
		missing = [param[0] for param in cls.required_params if param[0] not in command_data]
		if len(missing) > 1:
			return False, build_param_message(missing)
		return True, ''


	# checks that the user on the request is logged in if 'authenticated' is a necessary permission
	@classmethod
	def validate_auth(cls, request):
		return request.user.is_authenticated() if 'authenticated' in cls.required_permissions else True


	# checks that the user on the request has the necessary permissions for the command
	@classmethod
	def validate_permissions(cls, request):
		if not 'authenticated' in cls.required_permissions:
			to_check = cls.required_permissions
		else:
			to_check = cls.required_permissions.copy()
			to_check.remove('authenticated')
		if len(to_check) > 0:
			return request.user.has_perms(to_check)
		return True


	# gets a simple serializable definition of the command
	@classmethod
	def to_definition(cls):
		params = [{'name': name, 'type': kind.value, 'default': default} for name, kind, default in cls.required_params]
		return {'name': cls.command_name, 'params': params}


	# just a placeholder, but implementations should handle the actual incoming command and return a HTTP response
	def handle(self, request, command_data):
		raise NotImplementedError("The default handle method was not overridden by the custom handler.")