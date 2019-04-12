from rest_framework import serializers

from users.models import CustomUser, ExpMap

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'level', 'exp', 'coins', 'image')

class ExpMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpMap
        fields = '__all__'
