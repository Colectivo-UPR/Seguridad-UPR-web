from rest_framework import permissions

class IsOwnerOnly(permissions.BasePermission):
	"""
	Read,Update only allowed to the owner of the Incident.
	"""

	def has_object_permission(self, request, view, obj):

		return obj.owner == request.user

class IsWebAdmin(permissions.BasePermission):
	"""
	Allow access to only webadminuser
	"""

	def has_permission(self, request,view):
		return request.user and request.user.is_official

class IsDirector(permissions.BasePermission):
	"""
	Allow access to only Director
	"""

	def has_permission(self, request,view):
		return request.user and request.user.is_director