from django.urls import path
from .views import barcha_card, Transacsion, UpdatePasswordCardAPI


urlpatterns = [
    path('all_card/', barcha_card.as_view()),
    path('transacsion/', Transacsion.as_view()),
    path('card_update_password/', UpdatePasswordCardAPI.as_view()),
    # path('card_update_data/', UpdateCardDataAPI.as_view()),
]
# test