<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>资产总数</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ statistics.total || 0 }}</h2>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>使用中</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ statistics.inUse || 0 }}</h2>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>闲置</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ statistics.idle || 0 }}</h2>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { getAssetStatistics } from '@/api/asset'
import { ElMessage } from 'element-plus'

export default defineComponent({
  name: 'Dashboard',
  setup() {
    const statistics = ref({})

    const fetchData = async () => {
      try {
        const { data } = await getAssetStatistics()
        statistics.value = data || {
          total: 0,
          inUse: 0,
          idle: 0,
          maintenance: 0,
          scrapped: 0
        }
      } catch (error) {
        console.error('获取统计数据失败:', error)
        ElMessage.error('获取统计数据失败')
      }
    }

    onMounted(fetchData)

    return {
      statistics
    }
  }
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  min-height: calc(100vh - 120px);
  background-color: transparent;
  
  .el-card {
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,21,41,.08);
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .card-body {
      text-align: center;
      
      h2 {
        margin: 10px 0;
        font-size: 24px;
        color: #409EFF;
      }
    }
  }
}
</style> 