from django.shortcuts import render


def custom_403csrf(request, reason=''):
    """Кастомный обработчик ошибки: 403csrf"""
    template = 'core/403csrf.html'
    return render(request, template, status=403)


def custom_404(request, exception):
    """Кастомный обработчик ошибки: 404"""
    template = 'core/404.html'
    return render(request, template, status=404)


def custom_500(request):
    """Кастомный обработчик ошибки: 500"""
    template = 'core/500.html'
    return render(request, template, status=500)
