from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

# Create your views here.
def index(request):
    return HttpResponse("You prolly shouldn't be here.")

@csrf_exempt
def page(request, pager_slug):
    pager = Pager.objects.get(slug=pager_slug)
    pager.page(request)
    return HttpResponse("Done!")
