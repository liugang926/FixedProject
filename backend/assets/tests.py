from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Asset, AssetCategory, AssetTransfer

User = get_user_model()

class AssetModelTest(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123',
            email='test1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            email='test2@example.com'
        )
        
        # 创建资产类别
        self.category = AssetCategory.objects.create(
            name='测试类别',
            description='测试描述'
        )
        
        # 创建资产
        self.asset = Asset.objects.create(
            name='测试资产',
            asset_number='TEST001',
            status='idle',
            category=self.category,
            responsible_person=self.user1,
            location='测试位置'
        )

    def test_asset_creation(self):
        """测试资产创建"""
        self.assertEqual(self.asset.responsible_person, self.user1)
        self.assertEqual(self.asset.name, '测试资产')

    def test_asset_transfer(self):
        """测试资产转移"""
        transfer = AssetTransfer.objects.create(
            asset=self.asset,
            from_user=self.user1,
            to_user=self.user2,
            transfer_date='2024-02-12 10:00:00',
            reason='测试转移'
        )
        self.assertEqual(transfer.from_user, self.user1)
        self.assertEqual(transfer.to_user, self.user2) 