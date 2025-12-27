from django.urls import path

from . import views
from .feeds import LatestArticlesFeed

urlpatterns = [
    path("categories/", views.CategoryGenericView.as_view()),
    path("jobs/", views.JobListView.as_view()),
    path("events/", views.EventListView.as_view()),
    path("resources/", views.ResourceListView.as_view()),
    path("tools/", views.ToolListView.as_view()),
    path("tags/", views.TagGenericView.as_view()),
    path("contribute/", views.AcceptGuidelinesView.as_view()),
    path("articles/", views.ArticleListView.as_view()),
    path("comments/", views.CommentCreateView.as_view()),
    path("articles/feed/", LatestArticlesFeed()),
    path("articles/rss/", views.RSSFeedInfoView.as_view()),
    path(
        "articles/<uuid:article_id>/summarize/",
        views.ArticleSummaryView.as_view(),
    ),
    path(
        "articles/<uuid:article_id>/reactions/",
        views.ArticleReactionView.as_view(),
    ),
    path(
        "articles/<str:username>/<slug:slug>/",
        views.ArticleRetrieveView.as_view(),
        name="article_detail",
    ),
    path("comments/<uuid:comment_id>/replies/", views.ThreadRepliesView.as_view()),
    path(
        "comments/<uuid:comment_id>/",
        views.CommentDeleteView.as_view(),
    ),
    path(
        "comments/<uuid:comment_id>/like/",
        views.CommentLikeToggleView.as_view(),
    ),
    path(
        "comments/<uuid:comment_id>/likes/",
        views.CommentLikeStatusView.as_view(),
    ),
    
    # Liveblocks Integration
    path('users/search/', views.UserSearchView.as_view()),
    path('users/batch/', views.UserBatchView.as_view()),
]
