from django.db import transaction
from ..models.asset import Asset, AssetTransfer
from django.contrib.auth.models import User

class AssetService:
    @transaction.atomic
    def create_asset(self, data):
        try:
            asset = Asset.objects.create(**data)
            return {
                'id': asset.id,
                'asset_number': asset.asset_number,
                'message': '资产创建成功'
            }
        except Exception as e:
            raise Exception(f'创建资产失败: {str(e)}')

    @transaction.atomic
    def transfer_asset(self, asset_id, data):
        try:
            asset = Asset.objects.get(id=asset_id)
            from_user = asset.responsible_person
            to_user = User.objects.get(id=data['to_user_id'])
            
            transfer = AssetTransfer.objects.create(
                asset=asset,
                from_user=from_user,
                to_user=to_user,
                transfer_date=data['transfer_date'],
                reason=data['reason']
            )
            
            asset.responsible_person = to_user
            asset.save()
            
            return {
                'transfer_id': transfer.id,
                'message': '资产转移成功'
            }
        except Exception as e:
            raise Exception(f'资产转移失败: {str(e)}')

    def get_asset_statistics(self):
        try:
            total_count = Asset.objects.count()
            status_stats = Asset.objects.values('status').annotate(count=Count('id'))
            
            return {
                'total_count': total_count,
                'status_statistics': status_stats
            }
        except Exception as e:
            raise Exception(f'获取统计信息失败: {str(e)}') 