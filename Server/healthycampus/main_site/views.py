from django.views import generic
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render
from main_site.models import Page

def IndexView(request):
    return render(request, 'main_site/base.html', {})

