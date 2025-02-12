from django.db import models
from django.conf import settings

class AssetCategory(models.Model):
    name = models.CharField('类别名称', max_length=50)
    description = models.TextField('描述', blank=True)

    class Meta:
        verbose_name = '资产类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Asset(models.Model):
    STATUS_CHOICES = [
        ('in_use', '使用中'),
        ('idle', '闲置'),
        ('maintenance', '维修中'),
        ('scrapped', '已报废'),
    ]

    name = models.CharField('资产名称', max_length=100)
    asset_number = models.CharField('资产编号', max_length=50, unique=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='idle')
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, verbose_name='资产类别')
    responsible_person = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        verbose_name='负责人',
        related_name='responsible_assets'
    )
    location = models.CharField('位置', max_length=100)
    purchase_date = models.DateField('购买日期', null=True, blank=True)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '资产'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.asset_number})'

class AssetTransfer(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name='资产')
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
    transfer_date = models.DateTimeField('转移时间')
    reason = models.TextField('转移原因')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '资产转移'
        verbose_name_plural = verbose_name
        db_table = 'asset_transfers'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.asset} - {self.from_user} -> {self.to_user}'