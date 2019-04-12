from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

urlpatterns = [
    path('expmap/', UserExpMapView.as_view()),
    path('expmap/<pk>/', UserExpMapDetailView.as_view()),
    path('<username>/info/', UserDetailView.as_view()),
    path('<username>/javagochis/', JavagochiOwnedView.as_view()),
    path('<username>/items/', OwnedItemView.as_view()),
    path('<username>/change/', ChangeUserInfoView.as_view()),
]
