from django.urls import path
from . import views
from . import process_file

urlpatterns = [

    path('', views.upload_files),
    path('process_file/', process_file.process_file),

]
