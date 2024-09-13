from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.edit import CreateView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from user_app.forms import DonationsUserCreateForm

handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('donations_api.urls')),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('', include('collective_donations.urls',
                     namespace='collective_donations')),
    path('', include('user_app.urls', namespace='user_app')),
    path('', include('core.urls', namespace='core')),
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
