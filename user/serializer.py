from user.models import UserData
from django.db import serializers


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = [
            "userId",
            "id",
            "title",
            "body",
          ]
    def create(self,validated_data):
         return UserData.objects.create(**validated_data)