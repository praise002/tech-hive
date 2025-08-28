from django.urls import path

from . import views

urlpatterns = [
    path("me/", views.ProfileViewGeneric.as_view()),
    path("avatar/", views.AvatarUpdateView.as_view()),
    path("<str:username>/", views.PublicProfileView.as_view()),
    path("<str:username>/articles/", views.UserArticleListCreateView.as_view()),
    path("<str:username>/saved/", views.SavedArticlesView.as_view()),
    path("<str:username>/comments/", views.UserCommentsView.as_view()),
]
