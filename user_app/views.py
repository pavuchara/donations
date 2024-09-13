from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import ListView, UpdateView
from django.core.exceptions import PermissionDenied

from services.utils import get_elided_paginator
from user_app.forms import DonationUserUpdateForm
from collective_donations.models import Collect
from services import constants


DonationsUser = get_user_model()


class UserProfileView(ListView):
    """Представление: Профиль пользователя с его сборами."""

    model = Collect
    template_name = 'user_app/profile_detail.html'
    paginate_by = constants.COLLECT_PAGINATE_COUNT

    def get_queryset(self):
        queryset = self.model.published_related.filter(
            author__username=self.kwargs.get('username'),
        )
        return queryset

    def get_context_data(self, **kwargs):
        """
        Передача профиля пользователя в шаблон.
        Пагинатор: реализована пагинация для большого кол-ва старниц.
        """
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(
            DonationsUser,
            username=self.kwargs.get('username'),
        )
        page = context.get('page_obj')
        if page:
            context = get_elided_paginator(page, context)
        context['user'] = user
        context['title'] = user.username
        return context


class UserProfileUpdateView(UpdateView):
    model = DonationsUser
    form_class = DonationUserUpdateForm
    template_name = 'user_app/profile_update.html'

    def dispatch(self, request, *args, **kwargs):
        """Проверка, что запрос пришел от владельца профиля."""
        if request.user != self.get_object():
            raise PermissionDenied('Это чужой профиль.')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        object = get_object_or_404(
            self.model,
            username=self.kwargs.get('username'),
        )
        return object

    def form_valid(self, form):
        if 'avatar' in form.changed_data:
            if not form.cleaned_data['avatar']:
                form.instance.avatar = 'images/default_user.jpg'

        return super().form_valid(form)
