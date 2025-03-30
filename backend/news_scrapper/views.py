from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewsArticle
from .serializers import NewsArticleSerializer
from .utils import scrape_news
from datetime import datetime

# Create your views here.


@api_view(['GET'])
def fetch_news(request):
    # start_date_str = request.GET.get('start_date')
    # end_date_str = request.GET.get('end_date')

    # if not start_date_str or not end_date_str:
    #     return Response({"error": "Please provide start_date and end_date"}, status=400)

    # try:
    #     start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    #     end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    # except ValueError:
    #     return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=400)

    articles = scrape_news()

    for article in articles:
        NewsArticle.objects.create(
            title=article['title'],
            link=article['link'],
            text=article['text'],
            summary=article['summary'],
            keywords=article['keywords'],
            date_published=article['date_published']
        )

    return Response({"message": "News Scraped Successfully!"})


@api_view(['GET'])
def get_news(request):
    news_articles = NewsArticle.objects.all()
    print(f"Total Articles Found: {news_articles.count()}")  # Debugging
    serializer = NewsArticleSerializer(news_articles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def update_news_bias(request, id):
    try:
        news_article = NewsArticle.objects.get(id=id)
    except NewsArticle.DoesNotExist:
        return Response({'error': "Article Not Found"}, status=404)

    bias = request.data.get("bias")
    if bias not in ["Politically-Biased", "Politically-Unbiased"]:
        return Response({'error': "Invalid bias value"}, status=400)

    news_article.bias = bias
    news_article.save()
    return Response({'message': "Bias Updated Successfully"})
