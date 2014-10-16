from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Spoof)
admin.site.register(SpoofDomain)
admin.site.register(Provider)