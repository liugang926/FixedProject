from django.contrib import admin
from .models import Asset, AssetCategory, AssetTransfer

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at',)

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(AssetTransfer)
class AssetTransferAdmin(admin.ModelAdmin):
    list_display = ('asset', 'from_user', 'to_user', 'transfer_date')
    search_fields = ('asset__name', 'from_user__username', 'to_user__username')
    list_filter = ('transfer_date',)

# 删除这些重复的注册
# admin.site.register(Asset)
# admin.site.register(AssetCategory)
# admin.site.register(AssetTransfer) 