from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """ allows users to update own profile """

    def has_object_permission(self, request, view, obj):
        """ check if changing own profile """
        
        if request.method in permissions.SAFE_METHODS:  #view and create new profiles are safe
            return True
        
        return obj.id == request.user.id