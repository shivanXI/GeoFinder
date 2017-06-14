from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from .signals import user_logged_in
from .utils import get_client_city_data, get_client_ip
# Create your models here.



class UserSessionManager(models.Manager):
	def create_new(self, user, session_key=None, ip_address=None, city_data=None):
		session_new = self.model()
		session_new.user = user
		session_new.session_key = session_key
		if ip_address is not None:
			session_new.ip_address = ip_address
			if city_data:
				session_new.city_data = city_data
				try:
					city = city_data['city']
				except:
					city = None
				session_new.city = city_data
				try:
					country = city_data['country_name']
				except:
					country = None
			session_new.country = country
			session_new.save()
			return session_new
		return None



class UserSession(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL)
	session_key 	= models.CharField(max_length=60, null=True, blank=True)
	ip_address 		= models.GenericIPAddressField(null=True, blank=True)
	city_data 		= models.TextField(null=True, blank=True)
	city 			= models.CharField(max_length=120, null=True, blank=True)
	country 		= models.CharField(max_length=120, null=True, blank=True)
	active 			= models.BooleanField(default=True)
	timestamp 		= models.DateTimeField(auto_now_add=True)

	objects  = UserSessionManager()

	def __str__(self):
		#if self.city_data:
		#	return str(self.city_data)
		city = self.city
		country = self.country
		if city and country:
			return f"{city}, {country}"
		elif city and not country:
			return f"{city}"
		elif country and not city:
			return f"{country}"
		return self.user.username



def user_logged_in_receiver(sender, request, *args, **kwargs):
	user = sender
	#request = #parse the request to get the ip address	
	#city_data = None
	ip_address = get_client_ip(request)
	#ip_address = '72.14.207.99'
	#if ip_address:
	#	city_data = get_client_city_data(ip_address)
	session_key = request.session.session_key #got ip address
	#UserSession.objects.create(user = user,
	UserSession.objects.create_new(
								user = user, 
								session_key = session_key,
								ip_address = ip_address
								#city_data = city_data
							    #) 
								)



user_logged_in.connect(user_logged_in_receiver)