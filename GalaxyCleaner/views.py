from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def upload_files(request):
    #return HttpResponse('Hello')
    return render(request, 'index.html')

