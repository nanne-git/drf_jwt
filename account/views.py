from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializer import UserRegisterSerializer, LoginSerializer, GetUserDataSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegister(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            user = serializer.save()
            return Response({'msg': "Registration successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'mesg': "Logined"}, status=status.HTTP_200_OK)
            return Response({'error': "Email or password is wrong"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = GetUserDataSerializer(request.user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"user": request.user})
        if(serializer.is_valid(raise_exception=True)):
            return Response({"mesg": "password changed successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "password does not match"}, status=status.HTTP_400_BAD_REQUEST)
