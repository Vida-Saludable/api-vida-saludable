from api import serializers
from models.sol_model import Sol


class SolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sol
        fields = '__all__'