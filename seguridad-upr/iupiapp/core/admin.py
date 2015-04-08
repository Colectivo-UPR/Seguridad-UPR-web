# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Project
from models import AuthUser
from forms import  AuthUserChangeForm, AuthUserCreationForm
# Register your models here.

class AuthUserAdmin(UserAdmin):
	form = AuthUserChangeForm
	add_form = AuthUserCreationForm

	list_display = ('email','username', 'is_staff', 'is_superuser', 'is_director', 'is_shift_manager', 'is_official','is_active')
	list_filter = ('is_superuser', 'is_director', 'is_shift_manager', 'is_official')

	fieldsets = (
		(None, {
			'fields' : ('email','username', 'password', 'first_name', 'last_name')
			}
		),
		('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff', 'is_director', 'is_shift_manager', 'is_official')}),
		)

	add_fieldsets = (
			(None, {
				'classes': ('wide',),
				'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser','is_director', 'is_shift_manager', 'is_official')
				}
			),
		)

	search_fields = ('email', 'username')
	ordering = ('email',)
	filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(AuthUser,AuthUserAdmin)