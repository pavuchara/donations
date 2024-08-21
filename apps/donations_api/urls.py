from django.urls import path

from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
)

from apps.donations_api import views


urlpatterns = [
     # API token:
     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

     # Users:
     path('users/', views.UserCreateListView.as_view()),
     path('users/<int:user_id>/', views.UserRetriveUpdateView.as_view()),
     path('users/<int:user_id>/payments/', views.UserPaymentsListView.as_view()),
     path('users/<int:user_id>/collects/', views.UserCollectsListView.as_view()),

     # Collects:
     path('collects/', views.CollectCreateListView.as_view()),
     path('collects/<int:collect_id>/', views.CollectRetriveUpdateView.as_view()),
     path('collects/<int:collect_id>/payments/', views.CollectPaymentListCreateView.as_view()),

     # Payments:
     path('payments/', views.PaymentListView.as_view()),
     path('payments/<int:payment_id>/', views.PaymentUpdateView.as_view()),
]
