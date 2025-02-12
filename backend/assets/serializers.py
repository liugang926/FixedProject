from rest_framework import serializers
from .models import Asset, AssetCategory, AssetTransfer
from users.models import User

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    responsible_person_name = serializers.CharField(source='responsible_person.username', read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'

class AssetTransferSerializer(serializers.ModelSerializer):
    from_user_name = serializers.CharField(source='from_user.username', read_only=True)
    to_user_name = serializers.CharField(source='to_user.username', read_only=True)
    asset_number = serializers.CharField(source='asset.asset_number', read_only=True)

    class Meta:
        model = AssetTransfer
        fields = '__all__' 