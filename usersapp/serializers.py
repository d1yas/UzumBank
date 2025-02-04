# from rest_framework import serializers
# from .models import UzumUser
#
#
# class UzumUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UzumUser
#         fields = "__all__"



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



class NewSerializer(serializers.Serializer):
    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_username = serializers.CharField()


class UpdatePasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_last_name = serializers.CharField(required=False)  # last_name ixtiyoriy


