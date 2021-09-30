from django.db import models


class Emailupdate(models.Model):
	Email = models.EmailField(max_length = 254)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.Email




