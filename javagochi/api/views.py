from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework import permissions

from javagochi.models import JavagochiBase, Javagochi, JavagochiExpMap
from .serializers import JavagochiSerializer, JavagochiBaseSerializer, JavagochiExpMapSerializer
from users.models import CustomUser
from users.scripts import *

from javagochi import scripts

class JavagochiBaseListView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = JavagochiBase.objects.all()
    serializer_class = JavagochiBaseSerializer

class JavagochiBaseDetailView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = JavagochiBase.objects.all()
    serializer_class = JavagochiBaseSerializer

class ParticularJavagochiOwnedView(RetrieveAPIView):
    queryset = Javagochi.objects.all()
    serializer_class = JavagochiSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        url_id = self.kwargs['id']
        javagochi = queryset.get(id=url_id)
        return javagochi

class JavagochiExpMapView(ListAPIView):
    queryset = JavagochiExpMap.objects.all()
    serializer_class = JavagochiExpMapSerializer

class JavagochiExpMapDetailView(RetrieveAPIView):
    queryset = JavagochiExpMap.objects.all()
    serializer_class = JavagochiExpMapSerializer

class JavagochiBuyView(CreateAPIView):
    queryset = Javagochi.objects.all()
    serializer_class = JavagochiSerializer

    def create(self, validated_data):
        print(self.request.data)
        usr = self.request.data['user']
        type = self.request.data['race']
        nickname = self.request.data['nickname']

        user = CustomUser.objects.get_by_natural_key(usr)
        race = JavagochiBase.objects.filter(race=type).first()

        jc = Javagochi(owner=user,
                       race=race,
                       nickname=nickname,
                       current_health = race.max_health,
                       current_hunger = 0,
                       current_cold = 0,
                       current_hot = 0,
                       current_age = 0,
                       current_level = 1,
                       current_experience = 0)

        if(user.coins >= race.cost and user.level >= race.min_user_level):
            user.coins -= race.cost
            user.save()
            increase_user_level(user=user, amount_to_increase=race.exp_on_buy)
            jc.save()
            return Response("Correctly added the javagochi to your list", status=status.HTTP_201_CREATED)
        elif(user.level < race.min_user_level):
            return Response("You are not experienced enough to have this Javagochi", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("Not enough money", status=status.HTTP_400_BAD_REQUEST)

class UseItemView(UpdateAPIView):
    queryset = Javagochi.objects.all()
    serializer_class = JavagochiSerializer

    def update(self, request, *args, **kwargs):
        jc_id = kwargs['id']
        item = request.data['item']
        user = request.data['user']
        if(scripts.use_item(jc_id, item, user)):
            return Response("Successfully used the item", status=status.HTTP_200_OK)
        else:
            return Respons("Not enough items", status=status.HTTP_400_BAD_REQUEST)

class JavagochiChallengeView(UpdateAPIView):
    queryset = Javagochi.objects.all()
    serializer_class = JavagochiSerializer

    def update(self, request, *args, **kwargs):
        print(request.data)
        id_challenger = request.data['id_challenger']
        id_challenged = kwargs['id']
        challenger = Javagochi.objects.filter(id=id_challenger).first()
        challenged = Javagochi.objects.filter(id=id_challenged).first()
        message = scripts.challenge_result(challenger, challenged)
        return Response(message, status=status.HTTP_200_OK)
