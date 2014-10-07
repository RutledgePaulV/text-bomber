from django.http import JsonResponse


class AjaxResponse(object):

	OKAY = 200
	NOT_ALLOWED = 403
	BAD_REQUEST = 405
	UNAUTHORIZED = 401

	@classmethod
	def success(cls, results, meta=None):
		if isinstance(results, list):
			data = results
		elif isinstance(results, dict):
			data = [results]
		else:
			data = []

		content = {'results': data}
		if meta: content.update(meta)
		return JsonResponse(content, status=cls.OKAY)

	@classmethod
	def error(cls, message, meta=None, status=BAD_REQUEST):
		content = {'error': message}
		if meta: content.update(meta)
		return JsonResponse(content, status=status)
