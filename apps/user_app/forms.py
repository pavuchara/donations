from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

DonationsUser = get_user_model()


class DonationsUserCreateForm(UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta(UserCreationForm.Meta):
        model = DonationsUser
        fields = UserCreationForm.Meta.fields + (
            'email',
            'first_name',
            'last_name',
            'paternal_name',
            'avatar',
            'bio',
        )


class DonationUserUpdateForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = DonationsUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'paternal_name',
            'avatar',
            'bio',
        )
