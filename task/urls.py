from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (RegisterView,LoginView,TaskDetailView,TaskListCreateView,LogoutView)
from django.urls import path



urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('tasks/',TaskListCreateView.as_view(),name='task_list_create'),
    path('tasks/<int:pk>/',TaskDetailView.as_view(),name='task_detail'),  #view,update,delete   for only author and admin
]