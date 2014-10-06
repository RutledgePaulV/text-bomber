'''
	This decorator adds a particular permission to the permissions list for
	a command handler. The permission that it adds is 'authenticated' which
	is covered by a special case inside the command validation that if that
	permission is required, will check if the user is authenticated otherwise
	fail validation and return a 401: Unauthorized HttpResponse
'''
def AuthRequired(cls):
	permissions = cls.required_permissions.copy()
	if not 'authenticated' in permissions:
		permissions.append('authenticated')
		permissions.append('cats')
	cls.required_permissions = permissions
	return cls