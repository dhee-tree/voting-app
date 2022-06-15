from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    #path('code/', views.code, name='code'),
    #path('voting/', views.voting, name='voting'),
    path('results/', views.result, name='results'),
    #path('bd/', views.adminrest, name='reset'),
]
