from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from webapp import settings
from accounts.utils import send_html_mail
from rest_framework import serializers



class PasswordChangeSerializer(serializers.Serializer):
    """
    When a user know their current password and choose to change a new password,
    we will check the old password and if it right we will save the new password (as a encrypted hash of course!)

    Developer: Susmitha N
    """

    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        user = self.context["request"].user
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if not user.check_password(old_password):
            raise serializers.ValidationError("Invalid old password.")

        if new_password != confirm_password:
            raise serializers.ValidationError("New passwords don't match.")

        return data

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()


class SendPasswordResetLinkSerializer(serializers.Serializer):
    """
    When a user choose to click Forgot Password, we are checking if the given email have user account associated with it,
    generate a password reset link and send it the verified email id.

    Developer: Susmitha N
    """

    email = serializers.EmailField()

    def validate(self, data):

        try:
            get_user_model().objects.get(email=data["email"])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("User with provided email doesn't exist.")

        return data

    def save(self):
        email = self.validated_data["email"]

        user = get_user_model().objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.BASE_URL}/reset-password/{uid}/{token}"
        print("reset_url",reset_url)

        send_html_mail(
            template_name="accounts/password_reset_mail.html",
            context={
                "username": user.get_username(),
                "reset_url": reset_url,
            },
            subject="WebApp - Password Reset Link",
            to_mail=[email],
        )


class ResetPasswordSerializer(serializers.Serializer):
    """
    When a user clicked the Forgot password link and received a verification mail,
    we are checking the two codes in the link and reset the password for the user.

    Developer: Susmitha N
    """

    password = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(str(data["uid"]))
            print(f"uid: {uid}")
            self.user = get_user_model().objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise serializers.ValidationError("Invalid user id.")

        if not default_token_generator.check_token(self.user, data["token"]):
            raise serializers.ValidationError("Invalid token.")
        return data

    def save(self):
        password = self.validated_data["password"]
        self.user.set_password(password)
        self.user.save()
