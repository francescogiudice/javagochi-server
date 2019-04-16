from django.urls import path

from .views import (
    TradeOffersListView,
    ParticularTradeOfferView,
    StartTradeView,
    CloseTradeView
)

urlpatterns = [
    path('all/', TradeOffersListView.as_view()),
    path('add/', StartTradeView.as_view()),
    path('<id>/', ParticularTradeOfferView.as_view()),
    path('<id>/close', CloseTradeView.as_view())
]
