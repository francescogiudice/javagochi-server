from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView

from trades.models import TradeOffer
from .serializers import TradeOfferSerializer
from javagochi.models import Javagochi, JavagochiBase

class SomeTradeOffersListView(ListAPIView):
    queryset = TradeOffer.objects.all()
    serializer_class = TradeOfferSerializer

    def get_queryset(self):
        user = self.kwargs['username']
        return TradeOffer.objects.exclude(offering__owner__username=user)

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

        offered = Javagochi.objects.filter(id=offered_id).first()
        interested_into = JavagochiBase.objects.filter(race=interested_into_race).first()
        started = datetime.now()

        trade = TradeOffer(offering=offered, interested_into=interested_into, started=started)
        trade.save()
        return Response("Your Javagochi is now being traded", status=status.HTTP_201_CREATED)

class DeleteTradeView(DestroyAPIView):
    queryset = TradeOffer.objects.all()
    serializer_class = TradeOfferSerializer

    def get_queryset(self):
        queryset = TradeOffer.objects.filter(id=self.kwargs['id'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        print(self.kwargs)
        trade = TradeOffer.objects.filter(id=self.kwargs['id']).first()
        self.perform_destroy(trade)
        return Response("Eliminated trade", status=status.HTTP_200_OK)

class ConcludeTradeView(UpdateAPIView):
    queryset = TradeOffer.objects.all()
    serializer_class = TradeOffer

    def update(self, request, *args, **kwargs):
        print(request.data)
        trade_id = kwargs['id']
        id_trader = request.data['id_trader']

        trade = TradeOffer.objects.filter(id=trade_id).first()
        jc1 = trade.offering
        jc2 = Javagochi.objects.filter(id=id_trader).first()

        print(jc1.nickname + "->" + jc1.owner.username)
        print(jc2.nickname + "->" + jc2.owner.username)

        usr_tmp = jc2.owner
        jc2.owner = jc1.owner
        jc1.owner = usr_tmp

        print(jc1.nickname + "->" + jc1.owner.username)
        print(jc2.nickname + "->" + jc2.owner.username)

        jc1.save()
        jc2.save()
        trade.delete()

        return Response("Correctly traded the Javagochis", status=status.HTTP_200_OK)
