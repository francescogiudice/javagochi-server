from rest_framework.generics import ListAPIView, RetrieveAPIView

from trades.models import TradeOffer
from .serializers import TradeOfferSerializer

class TradeOffersListView(ListAPIView):
    queryset = TradeOffer.objects.all()
    serializer_class = TradeOfferSerializer

class ParticularTradeOfferView(RetrieveAPIView):
    queryset = TradeOffer.objects.all()
    serializer_class = TradeOfferSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        url_id = self.kwargs['id']
        trade = queryset.get(id=url_id)
        return trade
