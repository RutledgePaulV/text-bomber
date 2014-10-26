from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
					   url(r'', include('Bomber.urls', namespace='bomber', app_name='Bomber')),
					   url(r'^commands/', include('commands.urls', namespace='commands')),
					   url(r'^admin/', include(admin.site.urls)),
)
