from rest_framework import serializers

from health.models.test_ruffier_models import TestRuffier

class TestRuffierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRuffier
        fields = '__all__'
