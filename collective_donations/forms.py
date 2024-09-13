from django import forms

from collective_donations.models import Collect, Payment


class CollectFormCreate(forms.ModelForm):
    """Форма: Добавление нового сбора."""

    class Meta:
        model = Collect
        fields = '__all__'
        exclude = (
            'author',
            'slug',
            'collected_amount',
            'contributors_count',
            'create',
            'status',
        )
        widgets = {
            'end_datetime': forms.DateInput(attrs={'type': 'date'})
        }


class CollectFormUpdate(CollectFormCreate):
    """Форма: Редактирование сбора."""

    def clean_target_amount(self):
        """
        Проверка при редактировани, новая сумма
        не может быть меньше текущей задоначенной.
        """
        collected_amount = self.instance.collected_amount
        target_amount = self.cleaned_data.get('target_amount')
        if collected_amount > target_amount or collected_amount < 0:
            raise forms.ValidationError(
                f'Сумма не может быть меньше собранной({collected_amount} р.). или == 0'
            )
        return target_amount


class PaymentForm(forms.ModelForm):
    """Форма: добавление новой оплаты."""

    def __init__(self, *args, **kwargs):
        """Для валидации передается объект collect."""
        self.collect = kwargs.pop('collect', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Payment
        fields = '__all__'
        exclude = (
            'collect',
            'user',
            'create',
        )

    def clean_amount(self):
        """Проверка на то, что сумма не превышает сумму сбора."""
        amount = self.cleaned_data.get('amount')
        if self.collect and amount is not None:
            current_amount = amount + self.collect.collected_amount
            if current_amount > self.collect.target_amount or amount < 0:
                raise forms.ValidationError(
                    'Сумма платежа не может превышать целевую сумму сбора.'
                )
        return amount

    def clean(self):
        if self.user == self.collect.author:
            raise forms.ValidationError(
                'Самому себе нельзя донатить.'
            )
        return super().clean()
