from django.urls import path

from . import views

# Personal workspace (accessed via /account frontend)
# GET /profiles/me/articles/?status=draft
# GET /profiles/me/articles/?status=submitted_for_review
# GET /profiles/me/articles/?status=published

# # Public profile (accessed via /profile/{username} frontend)  
# GET /profiles/{username}/articles/ (published only, no status filter)
# GET /profiles/{username}/comments/

urlpatterns = [
    path("me/", views.ProfileViewGeneric.as_view()),
    path("avatar/", views.AvatarUpdateView.as_view()),
    path("me/articles/", views.UserArticleListCreateView.as_view()),
    path("me/saved/", views.SavedArticlesView.as_view()),
    path("me/comments/", views.UserCommentsView.as_view()),
    path("<str:username>/", views.PublicProfileView.as_view()),
    path("<str:username>/articles/", views.UserArticleListView.as_view()),
    path("<str:username>/comments/", views.UserCommentsView.as_view()),
]
