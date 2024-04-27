from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.donations_api import views


urlpatterns = [
    path('collects/',
         views.CollectListAPIView.as_view(),
         name='collect_list'),
    path('collects/create/',
         views.CollectCreateAPIView.as_view(),
         name='collect_create'),
    path('collects/<slug:collect_slug>/',
         views.CollectRetrieveAPIView.as_view(),
         name='collect_detail'),
    path('collects/<slug:collect_slug>/update/',
         views.CollectRetrieveUpdateDestroyAPIView.as_view(),
         name='collect_update_delete'),
    path('collects/<slug:collect_slug>/donats/',
         views.PaymentListAPIView.as_view(),
         name='donats'),
    path('collects/<slug:collect_slug>/donate/',
         views.PaymentCreateAPIView.as_view(),
         name='donate'),
    path('<str:username>/collects/',
         views.CollectUserListAPIView.as_view(),
         name='collect_list'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui')
]
