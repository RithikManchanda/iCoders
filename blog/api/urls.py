from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from .views import ( PostListAPIView,PostDetailAPIView,DestroyAPIView,
        PostUpdateAPIView,PostCreateAPIView)

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')



urlpatterns = [
     path('schema/', schema_view),
     path('', PostListAPIView.as_view(), name='Postlist'),
     path('<int:pk>/', PostDetailAPIView.as_view(), name='postDetaillist'),
    # path('BlogPost/<int:id>', views.BlogPost, name='BlogPost'),
     path('create/',  PostCreateAPIView.as_view(), name='BlogPostCreate'),
     path('update/<int:pk>', PostUpdateAPIView.as_view(), name='BlogPostUpdate'),
     path('BlogPostDelete/<int:pk>', DestroyAPIView.as_view(), name='BlogPostDelete'),
    # path('login/', views.login_view,name='login'),
    # path('register/', views.register_view,name='register'),
    # path('logout/', views.logout_view,name='logoutr'),
]
