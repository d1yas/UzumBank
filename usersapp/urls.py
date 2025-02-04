from django.urls import path
from .views import RegisterView, LoginView, AllUsersView, UserDetailView,UpdatePasswordUser,UpdateData

from django.urls import path
from .views import RegisterView, LoginView, AllUsersView, UserDetailView,UpdatePasswordUser

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('allusers/', AllUsersView.as_view(), name='all_users'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('update_password/', UpdatePasswordUser.as_view(), name='update_password'),
    path('update_data/', UpdateData.as_view(), name='update_data'),

]