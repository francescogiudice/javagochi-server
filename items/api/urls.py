from django.contrib import admin
from django.urls import path, include

from .views import BaseItemListView, BaseItemDetailView, ItemBuyView, ParticularOwnedItemView

urlpatterns = [
    path('market/', BaseItemListView.as_view()),
    path('buy/', ItemBuyView.as_view()),
    path('<pk>/', BaseItemDetailView.as_view()),
    path('owned/<id>/', ParticularOwnedItemView.as_view()),
]
