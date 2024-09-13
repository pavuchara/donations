from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from donations_api import serializers
from donations_api.mixins import SimpleListCacheMixin
from donations_api.cache_keys import ALL_COLLECTS, ALL_PAYMENTS
from collective_donations.models import Collect, Payment
from donations_api.permissions import (
    OnlyProfileOwnerPermission,
    OnlyAuthorPermission,
    OnlyOwnerPermission,
)


DonationsUser = get_user_model()


@extend_schema(tags=["Users"])
class UserCreateListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = DonationsUser.objects.all()
    serializer_class = serializers.UserSerializer


@extend_schema(tags=["Users"])
class UserRetriveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [OnlyProfileOwnerPermission]
    queryset = DonationsUser.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_url_kwarg = 'user_id'


@extend_schema(tags=["Users"])
class UserPaymentsListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserPaymentSerializer

    def get_queryset(self):
        user = get_object_or_404(DonationsUser, pk=self.kwargs.get('user_id'))
        return user.payments.all()


@extend_schema(tags=["Users"])
class UserCollectsListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserCollectSerializer

    def get_queryset(self):
        user = get_object_or_404(DonationsUser, pk=self.kwargs.get('user_id'))
        return user.collects.all()


@extend_schema(tags=["Collects"])
class CollectCreateListView(SimpleListCacheMixin, generics.ListCreateAPIView):
    queryset = Collect.published.all()
    serializer_class = serializers.CollectSerializer
    instance_cache_key = ALL_COLLECTS

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=["Collects"])
class CollectRetriveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [OnlyAuthorPermission]
    queryset = Collect.published.all()
    serializer_class = serializers.CollectSerializer
    lookup_url_kwarg = 'collect_id'


@extend_schema(tags=["Collects"])
class CollectPaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    def get_queryset(self):
        return self._get_collect().payments.all()

    def perform_create(self, serializer):
        serializer.save(
            collect=self._get_collect(),
            user=self.request.user,
        )

    def _get_collect(self):
        return get_object_or_404(Collect, pk=self.kwargs.get('collect_id'))


@extend_schema(tags=["Payments"])
class PaymentListView(SimpleListCacheMixin, generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    instance_cache_key = ALL_PAYMENTS


@extend_schema(tags=["Payments"])
class PaymentUpdateView(generics.UpdateAPIView):
    permission_classes = [OnlyOwnerPermission]
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentUpdateSerializer
    lookup_url_kwarg = 'payment_id'
    http_method_names = ['patch']
