from django.urls import path, include
from . import views


urlpatterns = (
    path('wordcloud/', views.wordcloud, name='wordcloud'),
)