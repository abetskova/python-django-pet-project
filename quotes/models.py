
from django.db import models

class Source(models.Model):
	name = models.CharField(max_length=255, unique=True)
	type = models.CharField(max_length=100, blank=True)  # фильм, книга и т.д.

	def __str__(self):
		return self.name

class Quote(models.Model):
	text = models.TextField(unique=True)
	source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes')
	weight = models.PositiveIntegerField(default=1)
	views = models.PositiveIntegerField(default=0)
	likes = models.PositiveIntegerField(default=0)
	dislikes = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('text', 'source')

	def __str__(self):
		return f'"{self.text[:50]}..." ({self.source})'

class Vote(models.Model):
	quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='votes')
	is_like = models.BooleanField()
	voted_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{"Like" if self.is_like else "Dislike"} for {self.quote.id}'
