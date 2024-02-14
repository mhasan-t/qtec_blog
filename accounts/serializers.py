from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', "user_type"]

        extra_kwargs = {
            'password': {'write_only': True}
        }
