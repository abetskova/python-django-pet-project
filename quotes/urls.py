from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_quote, name='random_quote'),
    path('vote/<int:quote_id>/<str:action>/', views.vote_quote, name='vote_quote'),
    path('top/', views.top_quotes, name='top_quotes'),
    path('add/', views.add_quote, name='add_quote'),
    path('add/success/', views.add_quote_success, name='add_quote_success'),
]
