from django.db import models
from django.contrib.auth.models import User

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
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    specification = models.TextField(blank=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    location = models.CharField(max_length=200)
    responsible_person = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assets'

class AssetTransfer(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='transfers_from', on_delete=models.PROTECT)
    to_user = models.ForeignKey(User, related_name='transfers_to', on_delete=models.PROTECT)
    transfer_date = models.DateTimeField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asset_transfers' 