from django.shortcuts import get_object_or_404
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
    author = UserSerializer(read_only=True)

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
        )
        read_only_fields = [
            'id',
            'author',
            'collected_amount',
            'contributors_count',
            'create',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_target_amount(self, value):
        if value < 0 or (self.instance and value < self.instance.target_amount):
            raise serializers.ValidationError('Сумма должна быть больше нуля и текущей суммы сбора')
        return value


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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

    def validate_amount(self, value):
        """Сумма платежа не дожна превышать целевую сумму сбора."""
        collect = self._get_collect()
        new_amount = collect.collected_amount + value
        if new_amount > collect.target_amount or value < 0:
            raise serializers.ValidationError(
                f'Сумма платежа не может превышать целевую сумму сбора или == 0'
                f'Укажите сумму до {collect.target_amount - collect.collected_amount} р.'
            )
        return value

    def validate(self, attrs):
        """Пользователь не может донатить сам себе."""
        if self.context['request'].user == self._get_collect().author:
            raise serializers.ValidationError('Самому себе нельзя донатить')
        return super().validate(attrs)

    def _get_collect(self):
        return get_object_or_404(Collect, pk=self.context['view'].kwargs.get('collect_id'))


class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'comment',
        ]


class UserPaymentSerializer(serializers.ModelSerializer):

    class Meta(PaymentSerializer.Meta):
        pass


class UserCollectSerializer(serializers.ModelSerializer):

    class Meta(CollectSerializer.Meta):
        pass
