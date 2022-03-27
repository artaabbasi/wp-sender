from rest_framework import permissions
from . import models



class SendMessageAccess(permissions.BasePermission):

    message = ('اجازه دسترسي ندارید')

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        user = request.user
        if user.id == models.SendMessage.user:
            return True
        else:
            return False
