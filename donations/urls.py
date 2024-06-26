from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.edit import CreateView

from apps.user_app.forms import DonationsUserCreateForm

handler404 = 'apps.core.views.custom_404'
handler500 = 'apps.core.views.custom_500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.donations_api.urls')),
    path('', include('apps.collective_donations.urls',
                     namespace='collective_donations')),
    path('', include('apps.user_app.urls', namespace='user_app')),
    path('', include('apps.core.urls', namespace='core')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/',
         CreateView.as_view(
             template_name='registration/registration_form.html',
             form_class=DonationsUserCreateForm,
             success_url=reverse_lazy('login')),
         name='registration'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
