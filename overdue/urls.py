from django.urls import path

from overdue import views

urlpatterns = [
  path('sync/', views.sync_overdue, name='overdue-sync'),
  path('validate-status/', views.validate_status, name='overdue-validate-status'),
]
