from django.db import models


class Trend(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()


class Article(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    pub_date = models.DateTimeField()
    sentiment = models.FloatField(null=True)
    trend = models.ManyToManyField(Trend)
