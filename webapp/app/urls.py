from django.urls import path

from . import views

urlpatterns = [
    path("articles/", views.Articles.as_view(), name="articles"),
    path("postman/",views.Postman.as_view(), name="postman"),
    path("create_destination/",views.CreateDestination.as_view(), name="create_destination"),
    path("edit_destination/",views.EditDestination.as_view(), name="edit_destination"),
    path("view_destination/",views.ViewDestination.as_view(), name="view_destination"),
    path("View_detail/",views.ViewDetailDestination.as_view(), name="view_detail"),
    path("delete_destination/",views.DeleteDestination.as_view(), name="delete_destination"),
    path("run_destination/",views.RunDestination.as_view(), name="run_destination"),
]