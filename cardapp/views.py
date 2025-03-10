from rest_framework import viewsets
from .models import Card
from rest_framework.views import APIView
from .serializers import CardSerializer, TransacsionSerializer, UpdatePasswordCardSerializer, UpdateDataCardSerializer, AddMoneySerializer, AddCardSerializer
from rest_framework.response import Response

from usersapp.models import User


class barcha_card(APIView):
    def get(self, request):
        cardlar = Card.objects.all()
        serializer2 = CardSerializer(cardlar, many=True)
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
        serializer = CardSerializer(card, many=True)
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


class AddMoneyApi(APIView):
    serializer_class = AddMoneySerializer

    def put(self, request):
        money = request.data.get('money')
        card_number = request.data.get('card_number')

        # "money" qiymatini tekshirish
        if not money:
            return Response({"error": "Money field is required"}, status=400)

        try:
            money = float(money)
        except ValueError:
            return Response({"error": "Invalid money value"}, status=400)

        # Karta mavjudligini tekshirish
        old_money = Card.objects.filter(card_number=card_number).first()
        if old_money is None:
            return Response({"error": "Card not found"}, status=404)

        summ = float(old_money.money) + money

        # Pul miqdorini yangilash
        Card.objects.filter(card_number=card_number).update(money=summ)

        return Response({"message": "Money added successfully"}, status=200)



# class  All_Card(APIView):
#     def get(self, request):
#         cards = Card.objects.all()
#         serializers = CardSerializer(cards, many=True)
#         return Response(serializers.data)


class AddCard(APIView):
    def post(self,request):
        serializers = AddCardSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message": "Card added succesfully"},status=200)
        return Response({"message": "Error"},status=404)
    

# class DeleteCard(APIView):
#     def delete(self,request,id):
#         try:
#             card = Card.objects.all().filter(id=id).delete()
#             return Response({"message":"Card delete succesfullly"},status=200)
#         except Card.DoesNotExist:
#             return Response({"message": "Card not found"},status=400)


# class UpdateCardAPI(APIView):
#     serializer_class = UpdateDataCardSerializer

#     def patch(self, request):
#         card_number = request.data.get('card_number')
#         try:
#             card = Card.objects.get(card_number=card_number)
#         except Card.DoesNotExist:
#             return Response({"message": "Card not found"}, status=404)

#         serializer = self.serializer_class(card, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Card updated successfully", "data": serializer.data}, status=200)
#         return Response(serializer.errors, status=400)
