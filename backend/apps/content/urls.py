from django.urls import path

from . import views
from .feeds import LatestArticlesFeed

urlpatterns = [
    path("categories/", views.CategoryGenericView.as_view()),
    path("tags/", views.TagGenericView.as_view()),
    path("contribute/", views.AcceptGuidelinesView.as_view()),
    path("articles/", views.ArticleListView.as_view()),
    path("articles/feed/", LatestArticlesFeed()),
    # path("articles/rss/", views.RSSFeedInfoView.as_view()),
    path(
        "articles/<str:username>/<slug:slug>/",
        views.ArticleRetrieveUpdateView.as_view(),
        name="project_detail",
    ),
]
