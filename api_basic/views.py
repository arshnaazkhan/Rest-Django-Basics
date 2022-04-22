from cgitb import lookup
from multiprocessing import AuthenticationError
from django.shortcuts import render
from html5lib import serialize
from .models import Article
from .serializers import ArticleSerializer 
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication,TokenAuthentication , BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

# Create your views here.

# @csrf_exempt
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return JsonResponse(serializer.data,safe = False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(data=data)
#         if serializer.IS_VALID():
#             serializer.save()
#             return JsonResponse(serializer.data,status=201)
#         return JsonResponse(serializer.errors,status=400)


# @csrf_exempt
# def article_detail(request,pk):
#     #pk is primary key
#     try:
#         article = Article.object.get(pk=pk)

#     except Article.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return JsonResponse(serializer.data)
    
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(article, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
    
#     elif request.method == 'DELETE':
#         article.delete()
#         return HttpResponse(status=204)

#Api_view Decorator of article_list
@api_view(['Get', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



#Api_view Decorator of article_detail

@api_view(['GET','PUT','DELETE'])

def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method =='DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Class Based api_view for article_list
class ArticleAPIView(APIView):
    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






#Class based api_view for article_detail

class ArticleDetails(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)

        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Generic view for article_list

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    
    lookup_field = 'id'

    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request, id = None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)

    
    def put(self,request,id=None):
        return self.update(request, id)

    def delete(self,request,id):
        return self.destroy(request, id)

#ViewSets view

# class ArticleViewSet(viewsets.ViewSet):
#     def list(self, request):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     def create(self,request):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         queryset = Article.objects.all()
#         article = get_object_or_404(queryset, pk = pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         article = Article.objects.get(pk=pk)
#         serializer = ArticleSerializer(article,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Genreric ViewSet

# class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
#     serializer_class = ArticleSerializer
#     queryset = Article.objects.all()    


#Model ViewSets

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

