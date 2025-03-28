from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Art, Bid

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Bid
        fields = ['user', 'amount', 'timestamp']
