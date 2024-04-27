from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from apps.services.mixins import OnlyAuthorMixinApi
from apps.collective_donations.models import Collect, Payment
from apps.donations_api.serializers import (
    CollectSerializer,
    CollectFullSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
)

# Получение модели пользователя.
DonationsUser = get_user_model()


class CollectListAPIView(generics.ListAPIView):
    """Получение всех сборов."""

    queryset = Collect.published_related.all()
    serializer_class = CollectFullSerializer


class CollectUserListAPIView(generics.ListAPIView):
    """Получение всех сборов пользователя."""

    serializer_class = CollectFullSerializer

    def get_queryset(self):
        user = get_object_or_404(
            DonationsUser,
            username=self.kwargs.get('username'),
        )
        queryset = Collect.published_related.filter(author=user)
        return queryset


class CollectCreateAPIView(generics.CreateAPIView):
    """Представление: Создание сбора."""

    permission_classes = [IsAuthenticated]
    serializer_class = CollectSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cover_image_default = 'images/default_collect.png'
        cover_image = serializer.validated_data.get('cover_image')
        if not cover_image:
            cover_image = cover_image_default
        serializer.save(author=user, cover_image=cover_image)


class CollectRetrieveAPIView(generics.RetrieveAPIView):
    """Представление: Просмотр конкретного сбора."""

    queryset = Collect.published_related.all()
    lookup_field = 'slug'
    lookup_url_kwarg = "collect_slug"
    serializer_class = CollectFullSerializer


class CollectRetrieveUpdateDestroyAPIView(
     generics.RetrieveUpdateDestroyAPIView):
    """Представление: Редактирование конкретного сбора."""

    queryset = Collect.published_related.all()
    lookup_field = 'slug'
    lookup_url_kwarg = "collect_slug"
    serializer_class = CollectSerializer
    permission_classes = [OnlyAuthorMixinApi]


class PaymentListAPIView(generics.ListAPIView):
    """Представление: Донаты относящиеся к конкретному сбору."""

    serializer_class = PaymentSerializer

    def get_queryset(self):
        object = get_object_or_404(
            Collect.published.all(),
            slug=self.kwargs.get('collect_slug')
        )
        queryset = Payment.objects.select_related(
            'user').filter(collect=object)
        return queryset


class PaymentCreateAPIView(generics.CreateAPIView):
    """Представление: Создание доната."""

    permission_classes = [IsAuthenticated]
    serializer_class = PaymentCreateSerializer

    def get_collect_object(self):
        """Получение объекта сбора."""
        return get_object_or_404(
            Collect.published.all(),
            slug=self.kwargs.get('collect_slug'),
        )

    def perform_create(self, serializer):
        """Передача пользователя и сбора."""
        collect_instance = self.get_collect_object()
        user = self.request.user
        serializer.save(collect=collect_instance, user=user)

    def get_serializer_context(self):
        """Перадача сбора в контекст для валидации."""
        context = super().get_serializer_context()
        context['collect'] = self.get_collect_object()
        return context
