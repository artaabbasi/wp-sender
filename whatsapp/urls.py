from django.urls import path
from .import views

urlpatterns = [
    path('messagedetail/<int:id>', views.Retrievemessage.as_view(), name='retrieve-message'),
    path('createmessage/', views.Createmessage.as_view(), name='create-message'),
    path('phones/', views.Createphone.as_view(), name='create-phone'),
    path('sendmessage/', views.sendmessage , name = 'send-message'),
]