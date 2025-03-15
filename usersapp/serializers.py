from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'birth_year', 'birth_month', 'birth_days','password' ]
        extra_kwargs = {
            'password': {'write_only': True}  # Parolni faqat yozish mumkin
        }


class UpdatePasswordSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()



class UpdateDataSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_first_name = serializers.CharField()




