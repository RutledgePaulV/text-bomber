from django.conf.urls import patterns, include, url
from django.contrib import admin
import Command
import Bomber


urlpatterns = patterns('',
    url(r'', include('Bomber.urls', namespace='bomber', app_name='Bomber')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^command/', include('Command.urls', namespace='command', app_name='Command'))
)
