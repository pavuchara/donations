from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.collective_donations.models import Collect, Payment


# Получение модели пользователя.
DonationUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = DonationUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'paternal_name',
            'email',
            'avatar',
            'bio',
            'password',
        )
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CollectSerializer(serializers.ModelSerializer):
    """Серриализатор: показ определенных полей сбора."""

    class Meta:
        model = Collect
        fields = (
            'id',
            'author',
            'title',
            'slug',
            'occasion',
            'target_amount',
            'contributors_count',
            'collected_amount',
            'contributors_count',
            'cover_image',
            'end_datetime',
            'create',
            'status',
        )
        read_only_fields = [
            'id',
            'author',
            'collected_amount',
            'contributors_count',
            'create',
            'status',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            'id',
            'collect',
            'user',
            'amount',
            'comment',
            'create',
            'payment_method',
            'payment_id',
        ]
        read_only_fields = [
            'id',
            'collect',
            'user',
            'create',
            'payment_id',
        ]


class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'comment',
        ]
