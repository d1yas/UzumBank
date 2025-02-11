from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UpdatePasswordSerializer, UserSerializer, UpdateDataSerializer



class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        custom_metadata = {
            'allowed_methods': ['POST', 'OPTIONS'],
            'endpoint_description': 'Register a new user.',
            'available_filters': ['id','username'],
            'pagination': {
                'page_size': 10,
                'max_page_size': 100
            },
            'custom_info': {
                'version': '1.0',
                'developer': 'Diyas',
                'last_updated': '2024-02-11'
            }
        }



class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user:
            serializer = UserSerializer(user)
            return Response({"message": "Login successful", "user": serializer.data}, status=200)
        return Response({"detail": "Invalid credentials"}, status=401)

    def options(self, request, *args, **kwargs):
        custom_metadata = {
            'allowed_methods': ['POST', 'OPTIONS'],
            'endpoint_description': 'Login existing user',
            'required_fields': ['username', 'password'],
            'response_format': {
                'success': {'message': 'string', 'user': 'object'},
                'error': {'detail': 'string'}
            },
            'custom_info': {
                'version': '1.0',
                'developer': 'Diyas',
                'last_updated': '2024-02-11'
            }
        }
        return Response(custom_metadata, status=status.HTTP_200_OK)


class AllUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def options(self, request, *args, **kwargs):
        custom_metadata = {
            'allowed_methods': ['GET', 'OPTIONS'],
            'endpoint_description': 'Show all users in database',
            'available_filters': ['id','username'],
            'pagination': {
                'page_size': 10,
                'max_page_size': 100
            },
            'custom_info': {
                'version': '1.0',
                'developer': 'Diyas',
                'last_updated': '2024-02-11'
            }
        }

        return Response(custom_metadata, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self, request, id):
        user = User.objects.all().filter(id=id).first()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def options(self, request, *args, **kwargs):
        custom_metadata = {
            'allowed_methods': ['GET', 'OPTIONS'],
            'endpoint_description': 'Get user details by ID',
            'parameters': {
                'id': 'integer (required) - User ID'
            },
            'response_format': 'UserSerializer data',
            'custom_info': {
                'version': '1.0',
                'developer': 'Diyas',
                'last_updated': '2024-02-11'
            }
        }
        return Response(custom_metadata, status=status.HTTP_200_OK)

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

    def options(self, request, *args, **kwargs):
        custom_metadata = {
            'allowed_methods': ['PUT', 'OPTIONS'],
            'endpoint_description': 'Update user password',
            'required_fields': ['username', 'old_password', 'new_password'],
            'response_format': {
                'success': {'message': 'string'},
                'error': {'detail': 'string'}
            },
            'custom_info': {
                'version': '1.0',
                'developer': 'Diyas',
                'last_updated': '2024-02-11'
            }
        }
        return Response(custom_metadata, status=status.HTTP_200_OK)

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

    def options(self, request, *args, **kwargs):
        custom_metadata = {
            'allowed_methods': ['PATCH', 'OPTIONS'],
            'endpoint_description': 'Update user data including username and password',
            'required_fields': ['username', 'old_password', 'new_password', 'new_username'],
            'response_format': {
                'success': {'message': 'string'},
                'error': {'detail': 'string'}
            },
            'custom_info': {
                'version': '1.0',
                'developer': 'Diyas',
                'last_updated': '2024-02-11'
            }
        }
        return Response(custom_metadata, status=status.HTTP_200_OK)


class DeleteUserAPI(APIView):
    def delete(self, request, id):
        try:
            user = User.objects.all().filter(id=id).delete()
            return Response({"message": f"User Data deleted successfully User id: {id} "}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found "}, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        custom_metadata = {
                'allowed_methods': ['DELETE', 'OPTIONS'],
                'endpoint_description': 'Delete user by ID',
                'parameters': {
                    'id': 'integer (required) - User ID to delete'
                },
                'response_format': {
                    'success': {'message': 'string'},
                    'error': {'detail': 'string'}
                },
                'custom_info': {
                    'version': '1.0',
                    'developer': 'Diyas',
                    'last_updated': '2024-02-11'
                }
            }
        return Response(custom_metadata, status=status.HTTP_200_OK)


