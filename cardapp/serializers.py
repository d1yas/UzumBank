from rest_framework import serializers
from .models import Card
from usersapp.models import User


class CardSerializer(serializers.ModelSerializer):
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


# class UpdateDataCardSerializer(serializers.Serializer):
#     old_card_number = serializers.CharField(max_length=16)
#     new_card_number = serializers.CharField(max_length=16)
#     old_card_pin_code = serializers.CharField()
#     new_card_pin_code = serializers.CharField()


class UpdateDataCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_pin_code', 'money']  # Faqat o‘zgartirilishi mumkin bo‘lgan maydonlar
        extra_kwargs = {
            'card_pin_code': {'required': False},  # Majburiy emas
            'money': {'required': False},  # Majburiy emas
        }

    def validate_money(self, value):
        if value < 0:
            raise serializers.ValidationError("Money amount cannot be negative")
        return value

class AddMoneySerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    money = serializers.FloatField()




class AddCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

