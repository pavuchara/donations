from rest_framework import serializers

from apps.collective_donations.models import Collect, Payment


class CollectSerializer(serializers.ModelSerializer):
    """Серриализатор: показ определенных полей сбора."""

    class Meta:
        model = Collect
        fields = (
            'title',
            'occasion',
            'description',
            'target_amount',
            'cover_image',
            'end_datetime',
        )


class CollectFullSerializer(serializers.ModelSerializer):
    """Серриализатор: показ сбора."""

    class Meta:
        model = Collect
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """Серриализатор: показ доната."""

    class Meta:
        model = Payment
        fields = (
            'user',
            'create',
            'amount',
            'comment',
        )


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Серриализатор: создание доната."""

    class Meta:
        model = Payment
        fields = (
            'amount',
            'comment',
            'payment_method',
        )

    def validate(self, data):
        """
        Проверка валидности платежа.
        Сумма не должна превышать сумму сбора.
        """
        amount = data.get('amount')
        collect = self.context.get('collect')

        if collect and amount is not None:
            current_amount = amount + collect.collected_amount
            if current_amount > collect.target_amount:
                raise serializers.ValidationError(
                    'Сумма платежа не может превышать целевую сумму сбора.'
                )
        return data
