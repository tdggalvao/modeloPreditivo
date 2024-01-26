from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
  path(''       , views.index,                 name='index'),
  path('tables/', views.processar_arquivo_csv, name='tables'),
  path('<str:product>/<int:months>', views.result),
  
]
