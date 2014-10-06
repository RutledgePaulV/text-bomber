from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
	providers = Provider.objects.all()
	return render(request, 'index.html', {'providers': providers})