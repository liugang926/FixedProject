<template>
  <div class="asset-list">
    <el-card>
      <template #header>
        <div class="header">
          <span>资产列表</span>
          <el-button type="primary" @click="handleAdd">新增资产</el-button>
        </div>
      </template>
      
      <el-table :data="assetList" border style="width: 100%">
        <el-table-column prop="asset_number" label="资产编号" width="120" />
        <el-table-column prop="name" label="资产名称" />
        <el-table-column prop="category.name" label="类别" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="responsible_person" label="负责人" width="120" />
        <el-table-column prop="location" label="位置" width="150" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { getAssetList } from '@/api/asset'

export default defineComponent({
  name: 'AssetList',
  setup() {
    const assetList = ref([])

    const fetchData = async () => {
      try {
        const { data } = await getAssetList()
        assetList.value = data
      } catch (error) {
        console.error('获取资产列表失败:', error)
      }
    }

    const getStatusType = (status) => {
      const types = {
        in_use: 'success',
        idle: 'info',
        maintenance: 'warning',
        scrapped: 'danger'
      }
      return types[status] || 'info'
    }

    const getStatusLabel = (status) => {
      const labels = {
        in_use: '使用中',
        idle: '闲置',
        maintenance: '维修中',
        scrapped: '已报废'
      }
      return labels[status] || status
    }

    onMounted(fetchData)

    return {
      assetList,
      getStatusType,
      getStatusLabel
    }
  }
})
</script>

<style lang="scss" scoped>
.asset-list {
  min-height: calc(100vh - 120px);
  background-color: transparent;
  
  .el-card {
    box-shadow: 0 1px 4px rgba(0,21,41,.08);
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style> 