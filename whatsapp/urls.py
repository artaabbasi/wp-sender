from django.urls import path
from .import views

urlpatterns = [
    path('sendmessage/', views.sendmessage , name = 'send-message'),
    path('image/', views.FileUpload.as_view() , name = 'send-image'),

]