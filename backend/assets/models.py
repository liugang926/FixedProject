from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings

def generate_asset_code():
    """生成唯一的资产编号"""
    return f"ASSET-{uuid.uuid4().hex[:8].upper()}"

class AssetCategory(models.Model):
    name = models.CharField(_('类别名称'), max_length=100)
    description = models.TextField(_('描述'), blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('资产类别')
        verbose_name_plural = _('资产类别')
        ordering = ['name']

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(_('资产名称'), max_length=100)
    code = models.CharField(
        _('资产编号'), 
        max_length=50, 
        unique=True,
        blank=True,
        help_text=_('留空将自动生成')
    )
    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.PROTECT,
        verbose_name=_('资产类别'),
        null=True,
        blank=True
    )
    description = models.TextField(_('描述'), blank=True)
    status = models.CharField(
        _('状态'),
        max_length=20,
        choices=[
            ('in_use', '使用中'),
            ('idle', '闲置'),
            ('maintenance', '维修中'),
            ('scrapped', '已报废'),
        ],
        default='idle'
    )
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('资产')
        verbose_name_plural = _('资产')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if not self.code:
            # 生成唯一编号
            while True:
                code = generate_asset_code()
                if not Asset.objects.filter(code=code).exists():
                    self.code = code
                    break
        super().save(*args, **kwargs)

class AssetTransfer(models.Model):
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        verbose_name=_('资产')
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='transfers_from',
        on_delete=models.PROTECT,
        verbose_name=_('转出人')
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='transfers_to',
        on_delete=models.PROTECT,
        verbose_name=_('接收人')
    )
    transfer_date = models.DateTimeField(_('转移日期'))
    reason = models.TextField(_('转移原因'))
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('资产转移')
        verbose_name_plural = _('资产转移')
        ordering = ['-transfer_date']

    def __str__(self):
        return f"{self.asset} - {self.from_user} -> {self.to_user}"