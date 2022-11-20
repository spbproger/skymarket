from rest_framework import pagination, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Ad, Comment
from rest_framework.decorators import action
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer
from ads.permissions import IsOwner, IsAdmin
from .filters import AdFilter


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    permission_classes = (AllowAny,)
    serializer_class = AdSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def get_serializer_class(self):
        if self.action in ["retrieve", "create", "update", "partial_update", "destroy"]:
            return AdDetailSerializer
        return AdSerializer

    def get_permissions(self):
        permission_classes = (AllowAny,)
        if self.action in ["list"]:
            permission_classes = (AllowAny,)
        elif self.action in ["retrieve"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["create", "update", "partial_update", "destroy", "me"]:
            permission_classes = (IsOwner | IsAdmin,)
        return tuple(permission() for permission in permission_classes)

    def get_queryset(self):
        if self.action == "me":
            return Ad.objects.filter(author=self.request.user).all()
        return Ad.objects.all()

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(ad_id=self.kwargs['ad_pk'])

    def perform_create(self, serializer):
        ad = Ad.objects.get(pk=self.kwargs['ad_pk'])
        serializer.save(author=self.request.user, ad=ad)

    def get_permissions(self):
        permission_classes = (IsAuthenticated,)
        if self.action in ["list", "retrieve"]:
            permission_classes = (IsAuthenticated,)
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = (IsOwner | IsAdmin,)
        return tuple(permission() for permission in permission_classes)