from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.donations_api import serializers
from apps.services.mixins import OnlyAuthorMixinApi, GetUserMixin
from apps.collective_donations.models import Collect, Payment


# Получение модели пользователя.
DonationsUser = get_user_model()


class CollectListAPIView(generics.ListAPIView):
    """Получение всех сборов."""

    queryset = Collect.published_related.all()
    serializer_class = serializers.CollectFullSerializer


class CollectCreateAPIView(generics.CreateAPIView):
    """Представление: Создание сбора."""

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CollectSerializer

    def perform_create(self, serializer):
        """
        Передача пользователя в сериалазер.
        Проверка на наличие переданного фото, если не передано,
        устанавливаеся дефолтное.
        """
        user = self.request.user
        cover_image_default = 'images/default_collect.png'
        cover_image = serializer.validated_data.get('cover_image')
        if not cover_image:
            cover_image = cover_image_default
        serializer.save(author=user, cover_image=cover_image)


class CollectRetrieveAPIView(generics.RetrieveAPIView):
    """Представление: Просмотр конкретного сбора."""

    queryset = Collect.published_related.all()
    serializer_class = serializers.CollectFullSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "collect_slug"


class CollectRetrieveUpdateDestroyAPIView(
     generics.RetrieveUpdateDestroyAPIView):
    """Представление: Редактирование конкретного сбора."""

    queryset = Collect.published_related.all()
    lookup_field = 'slug'
    lookup_url_kwarg = "collect_slug"
    serializer_class = serializers.CollectSerializer
    permission_classes = [OnlyAuthorMixinApi]


class PaymentListAPIView(generics.ListAPIView):
    """Представление: Донаты относящиеся к конкретному сбору."""

    serializer_class = serializers.PaymentSerializer

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
    serializer_class = serializers.PaymentCreateSerializer

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


class UserListApiView(generics.ListAPIView):
    """Представление: получение всех пользователей."""

    serializer_class = serializers.UserSerializer
    queryset = DonationsUser.objects.all()


class UserRetrieveApiView(GetUserMixin, generics.RetrieveAPIView):
    """Представление: получение конкретного пользователя."""

    serializer_class = serializers.UserSerializer


class UserCollectListAPIView(GetUserMixin, generics.ListAPIView):
    """Представление: получение всех сборов пользователя."""

    serializer_class = serializers.CollectFullSerializer

    def get_queryset(self):
        queryset = Collect.published_related.filter(author=self.get_object())
        return queryset


class UserPaymentListApiView(GetUserMixin, generics.ListAPIView):
    """Представление: получение всех донатов пользователя."""

    serializer_class = serializers.PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.select_related(
            'user',
        ).filter(user=self.get_object())
        return queryset
