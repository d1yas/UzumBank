from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UpdatePasswordSerializer, UserSerializer, UpdateDataSerializer

class BarchaUser(APIView):
    def get(self, request, id):
        odamlar = User.objects.all().filter(id=id)  # Barcha foydalanuvchilarni olib keladi
        serializer = UserSerializer(odamlar, many=True)  # Seriyalashtiradi
        return Response(serializer.data)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user:
            serializer = UserSerializer(user)
            return Response({"message": "Login successful", "user": serializer.data}, status=200)
        return Response({"detail": "Invalid credentials"}, status=401)


class AllUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self, request, id):
        user = User.objects.all().filter(id=id).first()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdatePasswordUser(APIView):
    serializer_class = UpdatePasswordSerializer

    def put(self, request):
        username = request.data.get('username')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if User.objects.all().filter(username=username, password=old_password).exists():
            User.objects.filter(username=username).update(password=new_password)
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not found or Password Incorrect"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateData(APIView):
    serializer_class = UpdateDataSerializer

    def patch(self, request):
        username = request.data.get('username')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_username = request.data.get('new_username')
        if User.objects.all().filter(username=username, password=old_password).exists():
            User.objects.filter(username=username).update(password=new_password, username=new_username)
            return Response({"message": "User Data updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not found or Password Incorrect"}, status=status.HTTP_400_BAD_REQUEST)


# test