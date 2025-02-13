from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Asset
from .serializers import AssetSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取资产统计信息"""
        total = Asset.objects.count()
        status_count = Asset.objects.values('status').annotate(count=Count('id'))
        
        # 初始化状态计数
        stats = {
            'total': total,
            'inUse': 0,
            'idle': 0,
            'maintenance': 0,
            'scrapped': 0
        }
        
        # 更新各状态的数量
        for item in status_count:
            if item['status'] == 'in_use':
                stats['inUse'] = item['count']
            elif item['status'] == 'idle':
                stats['idle'] = item['count']
            elif item['status'] == 'maintenance':
                stats['maintenance'] = item['count']
            elif item['status'] == 'scrapped':
                stats['scrapped'] = item['count']
        
        return Response(stats) 