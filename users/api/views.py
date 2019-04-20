from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework import permissions

from users.models import CustomUser, ExpMap
from javagochi.models import Javagochi
from items.models import OwnedItem
from trades.models import TradeOffer
from .serializers import CustomUserSerializer, ExpMapSerializer
from javagochi.api.serializers import JavagochiSerializer
from items.api.serializers import OwnedItemSerializer
from trades.api.serializers import TradeOfferSerializer

class UserListView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserDetailView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        url_username = self.kwargs['username']
        user = queryset.get(username=url_username)
        return user

class ChangeUserInfoView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        new_username = request.data['username']
        new_email = request.data['email']
        new_password = request.data['password']
        print(new_username)
        print(new_email)
        print(new_password)
        print(kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        user = queryset.get(username=kwargs['username'])
        user.username = new_username
        user.email = new_email
        if(new_password):
            user.set_password(new_password)
        user.save()
        return Response("Successfully updated the info", status=status.HTTP_200_OK)


class UserExpMapView(ListAPIView):
    queryset = ExpMap.objects.all()
    serializer_class = ExpMapSerializer

class UserExpMapDetailView(RetrieveAPIView):
    queryset = ExpMap.objects.all()
    serializer_class = ExpMapSerializer

class JavagochiOwnedView(ListAPIView):
    queryset = Javagochi.objects.all()
    serializer_class = JavagochiSerializer

    def get_queryset(self):
        print(self.request)
        owner = self.kwargs['username']
        return Javagochi.objects.filter(owner__username=owner)

class OwnedItemView(ListAPIView):
    queryset = OwnedItem.objects.all()
    serializer_class = OwnedItemSerializer

    def get_queryset(self):
        owner = self.kwargs['username']
        return OwnedItem.objects.filter(owner__username=owner)

class UserTradesView(ListAPIView):
    queryset = TradeOffer.objects.all()
    serializer_class = TradeOfferSerializer

    def get_queryset(self):
        user = self.kwargs['username']
        return TradeOffer.objects.filter(offering__owner__username=user)
