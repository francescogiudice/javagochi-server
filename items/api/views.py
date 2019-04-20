from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import permissions

from items.models import BaseItem, OwnedItem
from .serializers import BaseItemSerializer, OwnedItemSerializer
from users.models import CustomUser
from users.scripts import increase_user_level

class BaseItemListView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = BaseItem.objects.all()
    serializer_class = BaseItemSerializer

class BaseItemDetailView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = BaseItem.objects.all()
    serializer_class = BaseItemSerializer

class ParticularOwnedItemView(RetrieveAPIView):
    queryset = OwnedItem.objects.all()
    serializer_class = OwnedItemSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        url_id = self.kwargs['id']
        item = queryset.get(id=url_id)
        return item

class ItemBuyView(CreateAPIView):
    queryset = OwnedItem.objects.all()
    serializer_class = OwnedItemSerializer

    def create(self, validated_data):
        usr = self.request.data['user']
        itm = self.request.data['item']
        amount = int(self.request.data['amount'])

        user = CustomUser.objects.get_by_natural_key(usr)
        item = BaseItem.objects.filter(name=itm).first()

        if(user.coins >= item.cost * amount):
            if OwnedItem.objects.filter(owner=user, item=item).count() >= 1:
                itemObj = OwnedItem.objects.filter(owner=user, item=item).first()
                itemObj.amount_owned += amount
            else:
                itemObj = OwnedItem(owner=user,
                                    item=item,
                                    amount_owned=amount)
            user.coins -= item.cost * amount
            user.save()
            increase_user_level(user, item.exp_on_buy * amount)
            itemObj.save()
            return Response("Correctly added the item to your inventory", status=status.HTTP_201_CREATED)
        else:
            return Response("Not enough money", status=status.HTTP_400_BAD_REQUEST)
