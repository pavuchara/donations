from apps.user_app.models import DonationsUser
from django.contrib import admin
from django.contrib.auth import get_user_model


# DonationsUser = get_user_model()
# from django.contrib.auth.admin import UserAdmin
# admin.site.register(DonationsUser, UserAdmin)

@admin.register(DonationsUser)
class UserAdmin(admin.ModelAdmin):
    pass
