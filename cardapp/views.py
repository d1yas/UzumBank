from rest_framework import viewsets
from .models import Card
from rest_framework.views import APIView
from .serializers import CarsSerializer, TransacsionSerializer, UpdatePasswordCardSerializer, UpdateDataCardSerializer
from rest_framework.response import Response

from usersapp.models import User


class barcha_card(APIView):
    def get(self, request):
        cardlar = Card.objects.all()
        serializer2 = CarsSerializer(cardlar, many=True)
        return Response(serializer2.data)


class Transacsion(APIView):
    serializer_class = TransacsionSerializer

    def post(self, request):
        user_id = request.data.get('user_id')
        sender_card = request.data.get('sender_card')
        reciver_card = request.data.get('sender_card')
        money = float(request.data.get('money'))
        money2 = money - money / 100
        user = Card.objects.all().filter(card_holder=user_id, card_number=sender_card)
        if user:
            for i in user:
                qoldi = i.money - money
                Card.objects.all().filter(card_number=sender_card).update(money=qoldi)
                if i.money >= money:
                    old_money = Card.objects.all().filter(card_number=reciver_card)
                    if old_money:
                        for i in old_money:
                            all_money = Card.objects.all().filter(card_number=reciver_card).update(
                                money=money2 + i.money)

                        return Response({'message': f"Pul jo`natildi {money2}"}, status=201)
                    return Response({'message': f"Bunday karta raqam topilmadi"}, status=404)
                return Response({'message': f"Sizda yetarli Mablag` yoq"}, status=200)
        return Response({"message": 'Bunday foydalanuvchi topilmadi'}, status=404)


class TopMoneyCard(APIView):
    def get(self, request):
        card = Card.objects.all().order_by('?')  # Tasodifiy tartibda olib keladi
        serializer = CarsSerializer(card, many=True)
        return Response(serializer.data)


class UpdatePasswordCardAPI(APIView):
    serializer_class = UpdatePasswordCardSerializer
    def put(self,request):
        card_number = request.data.get('card_number')
        old_card_pin_code = request.data.get('old_card_pin_code')
        new_card_pin_code = request.data.get('new_card_pin_code')
        if Card.objects.all().filter(card_number=card_number, card_pin_code=old_card_pin_code).exists():
            Card.objects.filter(card_number=card_number).update(card_pin_code=new_card_pin_code)
            return Response({"message": "Pincode updated successfully"}, status=200)
        else:
            return Response({"message": "Card not found or pincode does not exist"}, status=404)


# class UpdateCardDataAPI(APIView):
#     serializer_class = UpdateDataCardSerializer
#     def patch(self,request):
#         old_card_number = request.data.get('card_number')
#         new_card_number = request.data.get('new_card_number')
#         old_card_pin_code = request.data.get('old_card_pin_code')
#         new_card_pin_code = request.data.get('new_card_pin_code')
#         if Card.objects.all().filter(card_number=old_card_number, card_pin_code=old_card_pin_code).exists():
#             Card.objects.filter(card_number=old_card_number, card_pin_code=old_card_pin_code).update(card_number=new_card_number, card_pin_code=new_card_pin_code)
#             return Response({"message": "Card Data updated successfully"}, status=200)
#         else:
#             return Response({"message": "Card not found or pincode does not exist"}, status=404)
