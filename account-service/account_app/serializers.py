from rest_framework import serializers
from .models import Cash

class CashBalanceSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Cash
        fields = ['email', 'balance']
