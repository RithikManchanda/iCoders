from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
   
    path('', views.BlogHome, name='BlogHome'),
    path('BlogPost/<int:id>', views.BlogPost, name='BlogPost'),
    path('BlogPostCreate/', views.BlogPostCreate, name='BlogPostCreate'),
    path('BlogPostUpdate/<int:id>', views.BlogPostUpdate, name='BlogPostUpdate'),
    path('BlogPostDelete/<int:id>', views.BlogPostDelete, name='BlogPostDelete'),
    path('login/', views.login_view,name='login'),
    path('register/', views.register_view,name='register'),
    path('logout/', views.logout_view,name='logoutr'),
]
