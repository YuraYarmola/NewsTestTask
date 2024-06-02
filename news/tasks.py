from openai import OpenAI
from pytrends.request import TrendReq
from datetime import datetime
from django.utils import timezone

from NewsAggregator.settings import OPENAI_API_KEY
from .models import Article, Trend
from celery import shared_task
import feedparser
import re

@shared_task
def fetch_trends():
    pytrends = TrendReq(hl='uk-UA', tz=360)
    today = timezone.now().date()
    trending_searches_df = pytrends.trending_searches(pn='ukraine')
    trending_searches = trending_searches_df[0].tolist()
    for trend in trending_searches:
        if not Trend.objects.filter(name=trend, date=today).exists():
            trend_instance = Trend(name=trend, date=today)
            trend_instance.save()

    return trending_searches

@shared_task
def fetch_news():
    feed = feedparser.parse("https://tsn.ua/rss/full.rss")
    trends = Trend.objects.filter(date__gte=timezone.now() - timezone.timedelta(days=7))
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        full_text = entry.fulltext
        article_trends = []
        pub_date = datetime(*entry.published_parsed[:6])
        article_title_cleaned = re.sub(r'[^\w\s]', '', title).lower()
        for trend in trends:
            trend_cleaned = re.sub(r'[^\w\s]', '', trend.name).lower()
            if trend_cleaned in article_title_cleaned or trend_cleaned in full_text:
                article_trends.append(trend)
        if not Article.objects.filter(link=link).exists():
            article = Article(title=title, link=link, pub_date=pub_date)
            article.save()
            article.trend.set(article_trends)

@shared_task
def match_and_analyze():
    fetch_news()

    articles = Article.objects.filter(pub_date__gte=timezone.now() - timezone.timedelta(days=7), sentiment__isnull=True)

    for article in articles:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant analyzing the sentiment of news headlines. Return a sentiment score between -1 and 1."},
                {"role": "user",
                 "content": f"You must return sentiment score of news from -1 to 1, where -1 is bad, 1 is good. Return ONLY NUMBER. News: {article.title}"},
            ],
            max_tokens=10,
            n=1,
            stop=None,
            temperature=0
        )
        try:
            sentiment = float(response.choices[0].message.content)
        except ValueError:
            sentiment = 0

        article.sentiment = sentiment
        article.save()
