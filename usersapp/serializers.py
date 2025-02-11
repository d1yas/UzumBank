from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Parolni faqat yozish mumkin
        }


class UpdatePasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()



class UpdateDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_username = serializers.CharField()




