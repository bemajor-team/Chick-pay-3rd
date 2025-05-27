# account_app/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Account
from django.shortcuts import get_object_or_404

class BalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_id):
        account = get_object_or_404(Account, id=account_id, user=request.user)
        return Response({
            "account_id": account.id,
            "balance": account.balance,
            "currency": "KRW"
        })
