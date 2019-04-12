from rest_framework import serializers

from javagochi.models import Javagochi, JavagochiBase, JavagochiExpMap
from users.api.serializers import CustomUserSerializer

class JavagochiBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = JavagochiBase
        fields = '__all__'

class JavagochiSerializer(serializers.ModelSerializer):
    race = JavagochiBaseSerializer(read_only=True)
    owner = CustomUserSerializer(read_only=True)

    class Meta:
        model = Javagochi
        fields = ('id', 'race', 'owner', 'nickname', 'current_health', 'current_age', 'current_hunger', 'current_hot', 'current_cold', 'current_level', 'current_experience')

class JavagochiExpMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = JavagochiExpMap
        fields = '__all__'
