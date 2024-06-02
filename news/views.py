from .models import Article
from .serializers import ArticleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class TrendingNewsView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['trend__name', 'pub_date']
    ordering_fields = ['sentiment', 'pub_date']

    def get_queryset(self):
        return Article.objects.filter(trend__isnull=False).order_by('-sentiment')
