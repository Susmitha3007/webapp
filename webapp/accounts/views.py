from django.shortcuts import render
import re
from django.contrib.auth import authenticate, get_user_model, login, logout
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from accounts import serializer
from accounts.utils import random_hashkey


# Create your views here.


class RegisterNewUser(APIView):
    """
    Class based view to register a new user.

    method: POST
    params: {
        "username": <username>,
        "password": <password>,
        "email": <email>,
    }

    status_code: 200
    response:
        {"sucess": "User created"}

    status_code: 400
    response:
        {"error": "User creation failed or user already exists"}

    Developer: Susmitha N
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        account_name = request.data.get("account_name", "user")
        website = request.data.get("website", "-")

        # Strip out everything after '+' in email if it exists
        email = re.sub(r"\+.*?(?=@)", "", email)

        # Then use a basic email validation regex
        if not bool(
            re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        ):
            return Response(
                {"email": email, "error": "invalid email address", "status_code": 400},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_users = get_user_model().objects.filter(email=email)
        if old_users:
            return Response(
                {"error": "user already exists", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = get_user_model().objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            # logger.debug(f"the user {email} is created")
        except Exception as e:
            print("error", e)
            return Response(
                {
                    "error": "user creation failed",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "status": "sucess",
                "status_code": 200,
                "message": "user created successfully",
                "username": username,
                "email": email,
                "token": token.key,
            }
        )


class LoginView(APIView):
    """
    Login View.

    Get method will only return the username.
    method: GET
    params: None

    status_code: 200
    output: { "user": <username> }


    Post method is for logging in.
    method: POST
    params: { "username": <username>, "password": <password>, "remember_me": true|false }

    status_code: 200
    output: {
        "success": "Successfully logged in",
        "API_TOKEN": <API-key>,
        "token": <user-token>,
        "user": <username>
    }

    status_code: 400
    output: { "error": "invalid credentials" }

    Developer: Susmitha N
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        content = {"user": str(request.user)}
        return Response(data=content)

    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")
        remember_me = request.data.get("remember_me")

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        login(request, user)
        if remember_me:
            request.session.set_expiry(timedelta(hours=12))
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "success": "Successfully logged in",
                "status_code": 200,
                "token": token.key,
                "username": username,
                "email": user.email,
            }
        )


class LogoutView(APIView):
    """
    Class Based view for Logout.

    Get method will logout the user (user needs to be logged in to logout actually!).
    method: GET
    params: None

    status_code: 200
    output: {"status": "success"}

    Developer: Susmitha N
    """

    # authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({"status": "success"})


class PasswordChangeView(generics.GenericAPIView):
    """
    Class Based view for changing the user password in the condition that the user know the current password.

    method: POST
    params: {
        "old_password": <old_password>,
        "new_password": <new_password>,
        "confirm_password": <confirm_password>
    }

    status_code: 200
    output: {"status": "success"}

    status_code: 403
    output:{ "detail": "Authentication credentials were not provided." }

    Developer: Susmitha N
    """

    serializer_class = serializer.PasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success"})


class SendPasswordResetLinkView(generics.GenericAPIView):
    """
    Class Based view for sending verification link when a user click the forgot password link.

    method: POST
    params: {"email": <email-id>}

    Developer: Susmitha N
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = serializer.SendPasswordResetLinkSerializer

    def post(self, request):
        print("request", request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success"})


class ResetPasswordView(generics.GenericAPIView):
    """
    Class Based view for reseting passwork when the user click the verification link in the email.

    method: POST
    params: {
        "uid": <uid>,
        "token": <token>,
        "password": <password>
    }

    status_code: 200
    output: {"status": "success"}

    Developer: Susmitha N
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = serializer.ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success"})


class ViewUser(APIView):

    def get(self, request: Request):
        user_objs = get_user_model().objects.filter(id=request.user.id)
        user_objs = list(user_objs.values())
        return Response(user_objs)


class EditUser(APIView):

    def post(self, request: Request):
        query_params = request.data
        user_name = query_params.get("user_name")
        first_name = query_params.get("first_name")
        last_name = query_params.get("last_name")
        email = query_params.get("email")
        user_objs = get_user_model().objects.filter(id=request.user.id)
        if not user_objs:
            return Response(
                {"Error": "Authentication credentials not provided"}, status=400
            )
        else:
            user_objs = user_objs.first()

        if first_name:
            user_objs.first_name = first_name
        if last_name:
            user_objs.last_name = last_name
        if email:
            user_objs.email = email
        if user_name:
            user_objs.username = user_name

        user_objs.save()

        return Response(
            {
                "message": "User updated successfully",
                "first_name": user_objs.first_name,
                "last_name": user_objs.last_name,
                "email": user_objs.email,
                "username": user_objs.username,
            }
        )


class Deleteuser(APIView):

    def get(self, request: Request):
        username = request.user.username
        user_objs = get_user_model().objects.filter(id=request.user.id)
        if not user_objs:
            return Response(
                {"Error": "Authentication credentials not provided"}, status=400
            )
        else:
            user_objs = user_objs.first()
        user_objs.delete()
        message = f"{username} - User deleted successfully"
        return Response({"message": message})
