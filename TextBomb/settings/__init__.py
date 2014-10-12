import os
from .base import *

if os.environ['ENVIRONMENT'] == 'LOCAL':
	from .local import *
else:
	from .prod import *
