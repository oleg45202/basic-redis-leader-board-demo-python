from django.urls import path

from . import views

urlpatterns = [
  path('api/list/top10', views.GetTo10.as_view()),
  path('', views.index, name='index'),
]
