from api import serializers
from users.models.role_model import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'













    

