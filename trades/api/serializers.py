from rest_framework import serializers

from trades.models import TradeOffer
from javagochi.api.serializers import JavagochiSerializer, JavagochiBaseSerializer

class TradeOfferSerializer(serializers.ModelSerializer):
    offering = JavagochiSerializer(read_only=True)
    interested_into = JavagochiBaseSerializer(read_only=True)

    class Meta:
        model = TradeOffer
        fields = ('id', 'offering', 'interested_into')
