from django.shortcuts import render


def custom_403csrf(request, reason=''):
    """Кастомный обработчик ошибки: 403csrf"""
    template = 'pages/403csrf.html'
    return render(request, template, status=403)


def custom_404(request, exception):
    """Кастомный обработчик ошибки: 404"""
    template = 'pages/404.html'
    return render(request, template, status=404)


def custom_500(request):
    """Кастомный обработчик ошибки: 500"""
    template = 'pages/500.html'
    return render(request, template, status=500)
