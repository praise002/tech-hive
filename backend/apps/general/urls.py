from django.urls import path

from . import views

urlpatterns = [
    path("site-detail/", views.SiteDetailView.as_view()),
    path("contact/", views.ContactView.as_view()),
    path("newsletter/", views.NewsletterView.as_view()),
    path(
        "newsletter/unsubscribe/<str:token>/", views.NewsletterUnsubscribeView.as_view()
    ),
]
