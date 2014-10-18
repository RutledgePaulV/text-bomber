from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
	providers = Provider.objects.all()
	count_options = [5, 20, 100, 250, 500]
	return render(request, 'index.html', {'providers': providers, 'counts': count_options})