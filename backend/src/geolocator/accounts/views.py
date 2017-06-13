from django.contrib.auth.views import LoginView as DefaultLoginView
from django.shortcuts import render

from .forms import LoginForm
# Create your views here.

class LoginView(DefaultLoginView): #form view
	authentication_form = LoginForm

	def form_validate(self, form):
		done_ = super(LoginView, self).form_valid(form)
		if self.request.user.is_authenticated():
			user.logged_in.send(self.request.user, request=self.request)
		return done_
