# account_app/urls.py
from django.urls import path
from .api_views import BalanceAPIView

urlpatterns = [
    path('balance/<int:account_id>/', BalanceAPIView.as_view(), name='account-balance'),
]
