from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Asset, AssetCategory, AssetTransfer
from ..serializers import AssetSerializer
from django.db.models import Count

class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.all()

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        try:
            asset = self.get_object()
            # 转移逻辑...
            return Response({'message': '资产转移成功'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        try:
            total_count = Asset.objects.count()
            status_stats = Asset.objects.values('status').annotate(count=Count('id'))
            return Response({
                'total_count': total_count,
                'status_statistics': status_stats
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 