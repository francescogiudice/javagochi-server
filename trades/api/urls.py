from django.urls import path

from .views import (
    SomeTradeOffersListView,
    TradeOffersListView,
    ParticularTradeOfferView,
    StartTradeView,
    DeleteTradeView,
    ConcludeTradeView
)

urlpatterns = [
    path('all/', TradeOffersListView.as_view()),
    path('<username>/all/', SomeTradeOffersListView.as_view()),
    path('add/', StartTradeView.as_view()),
    path('<id>/', ParticularTradeOfferView.as_view()),
    path('<id>/close', DeleteTradeView.as_view()),
    path('<id>/conclude/', ConcludeTradeView.as_view())
]
