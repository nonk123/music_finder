from django.urls import path

from .views import search

urlpatterns = [
    path('<query>/<int:max_results>/', search)
]
