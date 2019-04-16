from django.urls import path

from .views import (
    TradeOffersListView,
    ParticularTradeOfferView,
    StartTradeView
)

urlpatterns = [
    path('all/', TradeOffersListView.as_view()),
    path('add/', StartTradeView.as_view()),
    path('<id>/', ParticularTradeOfferView.as_view())
]
