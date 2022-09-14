from django.urls import path
from .import views

urlpatterns = [
    path('sendmessage/', views.sendmessage , name = 'send-message'),
    path('message/send/', views.accept_message , name = 'accept-message'),
    path('image/', views.FileUpload.as_view() , name = 'send-image'),
    path('message/list/<int:notif_history>/', views.FileUpload.as_view() , name = 'message-list'),

]