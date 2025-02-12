from django.contrib import admin
from .models import Asset, AssetCategory, AssetTransfer

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_number', 'name', 'category', 'status', 'responsible_person')
    list_filter = ('status', 'category')
    search_fields = ('asset_number', 'name')

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(AssetTransfer)
class AssetTransferAdmin(admin.ModelAdmin):
    list_display = ('asset', 'from_user', 'to_user', 'transfer_date')
    list_filter = ('transfer_date',)

# 删除这些重复的注册
# admin.site.register(Asset)
# admin.site.register(AssetCategory)
# admin.site.register(AssetTransfer) 