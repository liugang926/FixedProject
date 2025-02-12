from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.asset import Asset, AssetCategory, AssetTransfer
from ..services.asset_service import AssetService
from ..utils.pagination import StandardResultsSetPagination

class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    service = AssetService()

    def get_queryset(self):
        return Asset.objects.all()

    def create(self, request):
        try:
            asset = self.service.create_asset(request.data)
            return Response(asset, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        try:
            transfer = self.service.transfer_asset(pk, request.data)
            return Response(transfer, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        try:
            stats = self.service.get_asset_statistics()
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 