# Django
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, ReadOnlyPasswordHashField
from django import forms
# Project 
from models import AuthUser

class AuthUserCreationForm(UserCreationForm):
	""" A form creating a new users. Includes all requiered field, plus a repeated password. """
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

	class Meta(UserCreationForm.Meta):
		model = AuthUser
		fields = ('username', 'email')
		
	def clean_username(self):
		username = self.cleaned_data['username']
		return username

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class AuthUserChangeForm(UserChangeForm):
	password = ReadOnlyPasswordHashField(label="password",
										 help_text="""Raw pasword are not stored, so there is no way to see this user's passord,
										 but you can change the password using <a href=\"password/\"> this form </a>""")

	class Meta(UserChangeForm.Meta):
		model = AuthUser
		fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'is_director', 'is_shift_manager', 'is_official', 'user_permissions')

		def clean_password(self):
			return self.initial["password"]