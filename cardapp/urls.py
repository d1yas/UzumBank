from django.urls import path
from .views import barcha_card, Transacsion, UpdatePasswordCardAPI, AddMoneyApi, AddCard

urlpatterns = [
    path('all_card/', barcha_card.as_view()),
    path('transacsion/', Transacsion.as_view()),
    path('card_update_password/', UpdatePasswordCardAPI.as_view()),
    path('add_money_api/', AddMoneyApi.as_view()),
    # path('all_card', All_Card.as_view()),
    path('add_card', AddCard.as_view())
#   path('delete_card/<int:id>', DeleteCard.as_view()),
#   path('update_card',UpdateCardAPI.as_view())

]
#
