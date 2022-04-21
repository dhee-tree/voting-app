from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('code/', views.code, name='code'),
    path('voting/', views.voting, name='voting'),
    path('voting/cast/', views.cast_vote, name='cast'),

    # path('home/', views.second_home, name='home'),
    # path('create/', views.create, name='create'),
    # path('vote/<vote_id>/', views.vote, name='vote'),
    # path('results/<vote_id>/', views.results, name='results'),
]
