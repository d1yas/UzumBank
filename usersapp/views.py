from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, User
from .serializers import UpdatePasswordSerializer, UserSerializer, UpdateDataSerializer


def listing(request):
    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 25)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "list.html", {"page_obj": page_obj})


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
        paginator = Paginator(users, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        serializer = UserSerializer(page_obj, many=True)
        return Response({"users": serializer.data, "total_pages": paginator.num_pages}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePasswordUser(APIView):
    serializer_class = UpdatePasswordSerializer

    def put(self, request):
        username = request.data.get('username')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        user = User.objects.filter(username=username, password=old_password).first()
        if user:
            user.password = new_password
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response({"detail": "User not found or Password Incorrect"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateData(APIView):
    serializer_class = UpdateDataSerializer

    def patch(self, request):
        username = request.data.get('username')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_username = request.data.get('new_username')
        user = User.objects.filter(username=username, password=old_password).first()
        if user:
            user.username = new_username
            user.password = new_password
            user.save()
            return Response({"message": "User Data updated successfully"}, status=status.HTTP_200_OK)
        return Response({"detail": "User not found or Password Incorrect"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAPI(APIView):
    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({"message": f"User Data deleted successfully User id: {id}"}, status=status.HTTP_200_OK)
