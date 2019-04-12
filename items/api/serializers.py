from rest_framework import serializers

from items.models import BaseItem, OwnedItem
from users.api.serializers import CustomUserSerializer

class BaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseItem
        fields = '__all__'

class OwnedItemSerializer(serializers.ModelSerializer):
    item = BaseItemSerializer(read_only=True)
    owner = CustomUserSerializer(read_only=True)

    class Meta:
        model = OwnedItem
        fields = '__all__'
