from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.CategoryGenericView.as_view()),
    path("tags/", views.TagGenericView.as_view()),
]
