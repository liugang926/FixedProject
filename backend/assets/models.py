from django.db import models

class AssetCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asset_categories'

class Asset(models.Model):
    STATUS_CHOICES = [
        ('in_use', '使用中'),
        ('idle', '闲置'),
        ('maintenance', '维修中'),
        ('scrapped', '已报废'),
    ]

    asset_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        'assets.AssetCategory',
        on_delete=models.PROTECT,
        verbose_name='资产类别'
    )
    specification = models.TextField(blank=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    location = models.CharField(max_length=200)
    responsible_person = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='responsible_assets',
        verbose_name='负责人'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assets'

class AssetTransfer(models.Model):
    asset = models.ForeignKey(
        'assets.Asset',
        on_delete=models.CASCADE,
        verbose_name='资产'
    )
    from_user = models.ForeignKey(
        'users.User',
        related_name='transfers_from',
        on_delete=models.PROTECT,
        verbose_name='转出人'
    )
    to_user = models.ForeignKey(
        'users.User',
        related_name='transfers_to',
        on_delete=models.PROTECT,
        verbose_name='接收人'
    )
    transfer_date = models.DateTimeField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asset_transfers'