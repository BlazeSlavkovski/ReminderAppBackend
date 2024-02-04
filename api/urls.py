from django.contrib import admin
from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, CreateTaskView,CompleteTaskView, EditTaskView, DeleteTaskView,GetTaskView

urlpatterns = [
   #auth urls
   path('register', RegisterView.as_view()),
   path('login', LoginView.as_view()),
   path('user', UserView.as_view()),
   path('logout', LogoutView.as_view()),

    #task urls
    path('createTask', CreateTaskView.as_view()),
    path('editTask', EditTaskView.as_view()),
    path('completeTask', CompleteTaskView.as_view()),
    path('deleteTask', DeleteTaskView.as_view()),
    path('getTasks', GetTaskView.as_view()),
]
