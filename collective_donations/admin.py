from django.contrib import admin


from collective_donations.models import Collect, Payment


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    """Редактирование сбора в интерфейсе админки."""

    prepopulated_fields = {'slug': ('title',)}


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Просмотр оплаты, есть возможность только удалить оплату
    и отредактировать комменатрий.
    """

    actions = None
    list_display = ('user', 'collect', 'amount', 'payment_id')
    readonly_fields = (
        'collect',
        'user',
        'amount',
        'create',
        'payment_method',
        'payment_id',
    )
