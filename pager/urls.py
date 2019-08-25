from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<pager_slug>', views.page, name='page'),
]