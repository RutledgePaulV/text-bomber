from django.http import JsonResponse


class AjaxMixin(object):

	@classmethod
	def success(cls, results, meta=None, status=200):
		if isinstance(results, list):
			data = results
		elif isinstance(results, dict):
			data = [results]
		else:
			data = []

		content = {'results': data}
		if meta: content.update(meta)
		return JsonResponse(content, status=status)

	@classmethod
	def error(cls, message, meta=None, status=405):
		content = {'error': message, 'results':[]}
		if meta: content.update(meta)
		return JsonResponse(content, status=status)
