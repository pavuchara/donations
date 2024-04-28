from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from apps.services import constants
from apps.services.utils import get_elided_paginator
from apps.collective_donations.models import Collect, Payment
from apps.services.mixins import OnlyAuthorMixin
from apps.collective_donations.forms import (
    CollectFormCreate,
    PaymentForm,
    CollectFormUpdate,
)


class CollectListView(ListView):
    """Представление: Все опубликованные сборы."""

    model = Collect
    template_name = 'collective_donations/index.html'
    paginate_by = constants.COLLECT_PAGINATE_COUNT
    queryset = Collect.published_related.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context.get('page_obj')
        if page:
            context = get_elided_paginator(page, context)
        context['title'] = 'Главная страница'
        return context


class CollectDetailView(ListView):
    """Представление: Карточка сбора."""

    model = Payment
    template_name = 'collective_donations/collect_detail.html'
    paginate_by = constants.PAIMENT_PAGINATE_COUNT

    def dispatch(self, request, *args, **kwargs):
        """Получение сбора в кач-ве атрибута."""
        self.collect = get_object_or_404(
            Collect.published_related.all(),
            slug=kwargs.get('collect_slug')
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Получение все донатов сбора."""
        queryset = self.model.objects.select_related(
            'user').filter(collect=self.collect)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Передача title в context.
        Пагинатор: реализована пагинация для большого кол-ва старниц.
        """
        context = super().get_context_data(**kwargs)
        page = context.get('page_obj')
        if page:
            context = get_elided_paginator(page, context)
        context['collect'] = self.collect
        context['title'] = self.collect.title
        return context


class CollectCreateView(LoginRequiredMixin, CreateView):
    """Представление: Создание сбора."""

    model = Collect
    form_class = CollectFormCreate
    template_name = 'collective_donations/collect_create.html'

    def get_context_data(self, **kwargs):
        """Передача title в context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создай сбор'
        return context

    def form_valid(self, form):
        """Добавление объекту формы автора."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class CollectUpdateView(OnlyAuthorMixin, UpdateView):
    """Представление: Редактирование сбора."""

    model = Collect
    form_class = CollectFormUpdate
    template_name = 'collective_donations/collect_create.html'
    slug_field = 'slug'
    slug_url_kwarg = 'collect_slug'

    def get_context_data(self, **kwargs):
        """Передача title в context."""
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class CollectDeleteView(OnlyAuthorMixin, DeleteView):
    """Представление: Удаление сбора."""

    model = Collect
    template_name = 'collective_donations/collect_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'collect_slug'
    success_url = reverse_lazy('collective_donations:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PaymentCreateView(LoginRequiredMixin, CreateView):
    """Представление: Создание доната."""

    model = Payment
    form_class = PaymentForm
    template_name = 'collective_donations/payment_create.html'

    def dispatch(self, request, *args, **kwargs):
        """Получение сбора в кач-ве атрибута."""
        self.collect = get_object_or_404(
            Collect.published.all(),
            slug=kwargs.get('collect_slug')
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Передача title в context."""
        context = super().get_context_data(**kwargs)
        context['collect'] = self.collect
        return context

    def get_form_kwargs(self):
        """Передача в форму сбора для валидации."""
        kwargs = super().get_form_kwargs()
        kwargs['collect'] = self.collect
        return kwargs

    def form_valid(self, form):
        """Добавление объекту формы сбора и автора."""
        form.instance.collect = self.collect
        form.instance.user = self.request.user
        return super().form_valid(form)
