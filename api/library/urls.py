from django.urls import path
from .views import LibraryView, BookView

urlpatterns = [
    path('library/', LibraryView.as_view()),
    path('book/', BookView.as_view()),
]
