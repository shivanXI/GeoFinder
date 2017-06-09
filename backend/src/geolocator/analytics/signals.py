from django.dispatch import signal
	

user_logged_in = Signal(providing_args=['request'])