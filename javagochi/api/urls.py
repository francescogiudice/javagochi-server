from django.contrib import admin
from django.urls import path, include

from .views import (
    JavagochiBaseListView,
    JavagochiBaseDetailView,
    JavagochiBuyView,
    ParticularJavagochiOwnedView,
    UseItemView,
    JavagochiExpMapView,
    JavagochiExpMapDetailView
)

urlpatterns = [
    path('market/', JavagochiBaseListView.as_view()),
    path('buy/', JavagochiBuyView.as_view()),
    path('expmap/', JavagochiExpMapView.as_view()),
    path('expmap/<pk>/', JavagochiExpMapDetailView.as_view()),
    path('<pk>/', JavagochiBaseDetailView.as_view()),
    path('owned/<id>/', ParticularJavagochiOwnedView.as_view()),
    path('owned/<id>/useitem/', UseItemView.as_view()),
]
