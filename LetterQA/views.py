from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def upload_letter_file(request):
    return render(request, 'letter_index.html')
