from django.urls import path

from .views import (
    TradeOffersListView,
    ParticularTradeOfferView
)

urlpatterns = [
    path('all/', TradeOffersListView.as_view()),
    path('<id>/', ParticularTradeOfferView.as_view())
]
