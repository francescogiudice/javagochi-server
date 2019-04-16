from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIViewm, CreateAPIView

from trades.models import TradeOffer
from .serializers import TradeOfferSerializer
from javagochi.models import Javagochi, JavagochiBase

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

class StartTradeView(CreateAPIView):
    queryset = TradeOffer.objects.all()
    serializer_class = TradeOfferSerializer

    def create(self, validated_data):
        print(self.request.data)
        offered_id = self.request.data['offered_id']
        interested_into_race = self.request.data['interested_into']

        offered = Javagochi.objects.filter(id=offered_id)
        interested_into = JavagochiBase.objects.filter(race=interested_into_race)

        trade = Trade(offered=offered, interested_into=interested_into)
        trade.save()
        return Respone("Trade started", status=status.HTTP_201_CREATED)
