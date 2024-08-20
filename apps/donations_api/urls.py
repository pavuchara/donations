from django.urls import path

from apps.donations_api import views


urlpatterns = [
     path('users/', views.UserCreateListView.as_view()),
     path('users/<int:user_id>/', views.UserRetriveUpdateView.as_view()),
     path('collects/', views.CollectCreateListView.as_view()),
     path('collects/<int:collect_id>/', views.CollectRetriveUpdateView.as_view()),
     path('collects/<int:collect_id>/payments/', views.CollectPaymentListCreateView.as_view()),
     path('payments/', views.PaymentListView.as_view()),
     path('payments/<int:payment_id>/', views.PaymentUpdateView.as_view()),
]
