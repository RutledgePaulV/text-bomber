
def deep_getattr(obj, key, default):
	chunked = key.split('.')
	for chunk in chunked:
		obj = getattr(obj, chunk, default)
	return obj


class Cereal(object):

	@classmethod
	def dictify(cls, model, fields):
		result = {}
		for field in fields:
			result[field[0]] = deep_getattr(model,field[1], field[2])
		return result
