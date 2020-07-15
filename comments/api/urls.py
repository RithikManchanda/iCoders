from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from .views import (CommentListAPIView, CommentDetailAPIView)

urlpatterns = [
   
     path('', CommentListAPIView.as_view(), name='comments list'),
     path('<int:pk>/', CommentDetailAPIView.as_view(), name='thread'),
    # # path('BlogPost/<int:id>', views.BlogPost, name='BlogPost'),
    #  path('create/',  PostCreateAPIView.as_view(), name='BlogPostCreate'),
    #  path('update/<int:pk>', PostUpdateAPIView.as_view(), name='BlogPostUpdate'),
    #  path('BlogPostDelete/<int:pk>', DestroyAPIView.as_view(), name='BlogPostDelete'),
    # # path('login/', views.login_view,name='login'),
    # # path('register/', views.register_view,name='register'),
    # # path('logout/', views.logout_view,name='logoutr'),
]
