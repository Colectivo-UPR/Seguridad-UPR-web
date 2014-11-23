from rest_framework import permissions

class IsOwnerOnly(permissions.BasePermission):
	"""
	Read,Update only allowed to the owner of the Incident.
	"""

	def has_object_permission(self, request, view, obj):

		return obj.owner == request.user