from rest_framework import routers
from django.urls import include, path

from .views import CommentViewSet, AdViewSet


ads_router = routers.SimpleRouter()
ads_router.register("ads", AdViewSet, basename="ads")


comments_router = routers.SimpleRouter()
comments_router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(ads_router.urls)),
    path("", include(comments_router.urls)),
]



