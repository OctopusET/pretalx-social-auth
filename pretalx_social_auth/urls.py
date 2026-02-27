from django.urls import path

from . import views

urlpatterns = [
    # authentication / association
    path("p/social_auth/login/<str:backend>/", views.auth, name="begin"),
    path("p/social_auth/complete/<str:backend>/", views.complete, name="complete"),
    # disconnection
    path(
        "p/social_auth/disconnect/<str:backend>/",
        views.disconnect,
        name="disconnect",
    ),
    path(
        "p/social_auth/disconnect/<str:backend>/<int:association_id>/",
        views.disconnect,
        name="disconnect_individual",
    ),
]
