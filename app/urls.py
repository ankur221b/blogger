from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('new_blog', views.new_blog, name='new_blog'),
    path('blog/<str:title>', views.post_view, name='post_view'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('blog/<str:title>/delete', views.delete, name='delete'),
    path('blog/<str:title>/edit', views.edit, name='edit'),
    path('blog/<str:title>/make_changes', views.make_edit, name='make_edit')

]
