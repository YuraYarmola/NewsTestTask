from rest_framework import serializers
from .models import Article, Trend


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ['name', 'date']


class ArticleSerializer(serializers.ModelSerializer):
    trend = TrendSerializer(many=True)

    class Meta:
        model = Article
        fields = ['title', 'link', 'pub_date', 'sentiment', 'trend']
