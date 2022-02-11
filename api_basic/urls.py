from django.db import router
from .views import ArticleDetails, article_list,article_detail, ArticleAPIView,GenericAPIView,ArticleViewSet
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article',ArticleViewSet, basename='article')

urlpatterns = [
    #path('article/', article_list),
    #path('detail/<int:pk>/',article_detail) #for function based views
    #for class based APIView

    path('article/',ArticleAPIView.as_view()),
    path('detail/<int:id>/',ArticleDetails.as_view()),

    #for generic and mixins views
    path('generic/article/<int:id>/',GenericAPIView.as_view()),
    path('viewset/',include(router.urls)), 
    path('viewset/<int:pk>/',include(router.urls)), 
   
   

]
