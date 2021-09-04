"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views



urlpatterns = [
     
  #  path('', views.home,name = "home"),
    path('', views.HomePageView.as_view(),name = "home"),
    path('profile/', views.profile,name = "create"),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('user/<str:username>', views.UserPostListView.as_view(), name='user_posts'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/del/', views.PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/follows', views.FollowsListView.as_view(), name='user-follows'),
    path('user/<str:username>/followers', views.FollowersListView.as_view(), name='user-followers'),
    path('search/', views.searchview, name='search'),
   # path('detail/int:<id>/', views.detail,name = "detail"),
   # path('detail/int:<pk>/', views.Portfdetailview.as_view(),name = "detail"),
    #path('search/',views.search,name="search"),
  
    #path('signup/',views.Signupview.as_view(),name="signup"),

]
