from django.urls import path

from apps.user_app.views import UserProfileView, UserProfileUpdateView


app_name = 'user_app'


urlpatterns = [
    path('users/<str:username>/',
         UserProfileView.as_view(),
         name='profile_detail'),
    path('users/<str:username>/update/',
         UserProfileUpdateView.as_view(),
         name='profile_update'),
]
