from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_reset_link/",
        views.SendPasswordResetLinkView.as_view(),
        name="password_reset_link",
    ),
    path(
        "password_reset/",
        views.ResetPasswordView.as_view(),
        name="password_reset",
    ),
    path("register/", views.RegisterNewUser.as_view(), name="register"),
    path("viewuser/", views.ViewUser.as_view(), name="viewuser"),
    path("edituser/",views.EditUser.as_view(), name="edituser"),
    path("deleteuser/",views.Deleteuser.as_view(), name="deleteuser"),
]
