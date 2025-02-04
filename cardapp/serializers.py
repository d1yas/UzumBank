from rest_framework import serializers
from .models import Card


class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"



class TransacsionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    sender_card = serializers.CharField(max_length=16)
    reciver_card= serializers.CharField(max_length=16)
    money = serializers.FloatField()



class UpdatePasswordCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    old_card_pin_code = serializers.CharField()
    new_card_pin_code = serializers.CharField()


class UpdateDataCardSerializer(serializers.Serializer):
    old_card_number = serializers.CharField(max_length=16)
    new_card_number = serializers.CharField(max_length=16)
    old_card_pin_code = serializers.CharField()
    new_card_pin_code = serializers.CharField()


