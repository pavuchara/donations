from django.urls import path

from collective_donations import views


app_name = 'collective_donations'

urlpatterns = [
    path('', views.CollectListView.as_view(), name='index'),
    path('collects/create/',
         views.CollectCreateView.as_view(),
         name='create'),
    path('collects/<slug:collect_slug>/',
         views.CollectDetailView.as_view(),
         name='collect_detail'),
    path('collects/<slug:collect_slug>/update/',
         views.CollectUpdateView.as_view(),
         name='collect_update'),
    path('collects/<slug:collect_slug>/delete/',
         views.CollectDeleteView.as_view(),
         name='collect_delete'),
    path('collects/<slug:collect_slug>/donate/',
         views.PaymentCreateView.as_view(),
         name='donate'),
]
