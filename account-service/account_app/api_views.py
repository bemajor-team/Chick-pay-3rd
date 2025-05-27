# account_app/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cash  # ✅ Cash 모델로 수정
from django.shortcuts import get_object_or_404

class BalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_id):
        cash = get_object_or_404(Cash, user__id=account_id)
        return Response({
            "account_id": account_id,
            "balance": cash.balance,
            "currency": "KRW"
        })
