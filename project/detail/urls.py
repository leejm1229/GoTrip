
from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.detail),
    path('list/detail/', views.detail_list),
]