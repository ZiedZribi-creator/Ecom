from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ReviewSerializer
from .models import Review
# Create your views here.
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ReviewViewset(ModelViewSet):
    serializer_class= ReviewSerializer
    queryset = Review.objects.all()
    pagination_class= StandardResultsSetPagination

    def get_queryset(self):
        qs = Review.objects.all()
        client_name = self.request.GET.get('client_name')
        content = self.request.GET.get('content')
        print(client_name)
        print(content)
        if client_name or content  :
            if client_name :
                qs = qs.filter(client_name__contains=client_name)
            if content :
                qs = qs.filter(content__contains=content)
            return qs
        return qs
