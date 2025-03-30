from django.db import models

# Create your models here.


class NewsArticle(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    text = models.TextField()
    summary = models.TextField()
    keywords = models.TextField()
    date_published = models.DateField()
    bias = models.CharField(max_length=10, choices=[
        (1, 'Politically-Biased'),
        (0, 'Politically-Unbiased')
    ], null=True, blank=True)


def __str__(self):
    return self.title
