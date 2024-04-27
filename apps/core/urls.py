from django.urls import path
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path('about/',
         TemplateView.as_view(template_name='core/about.html'),
         name='about'),
    path('rules/',
         TemplateView.as_view(template_name='core/rules.html'),
         name='rules'),
]
