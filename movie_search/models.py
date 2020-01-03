from django.db import models

# Favourite model has only 1 field(title), because it is enough to fetch data from the API.

class Favourite(models.Model):
	title = models.CharField(max_length = 100)

	def __str__(self):
		return self.title