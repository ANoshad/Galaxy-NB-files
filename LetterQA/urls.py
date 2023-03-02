from django.urls import path
from . import views
from . import Letters_QA

urlpatterns = [
    path('', views.upload_letter_file),
    path('Letters_QA/', Letters_QA.QA_file),

]

