from django.conf import settings
import importlib

def load_from_apps():
	results = []
	for app in settings.CUSTOM_APPS:
		try:
			scanned = importlib.import_module("{0}.{1}".format(app, settings.COMMAND_FILE))
			results.append(scanned)
		except ImportError:
			pass
	return results