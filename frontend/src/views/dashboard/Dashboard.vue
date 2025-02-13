<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="8" v-for="(item, index) in statistics" :key="index">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>{{ item.title }}</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ item.value }}</h2>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

export default defineComponent({
  name: 'Dashboard',
  setup() {
    const statistics = ref([
      { title: '资产总数', value: 0 },
      { title: '使用中', value: 0 },
      { title: '闲置', value: 0 }
    ])

    const fetchData = async () => {
      try {
        const response = await request({
          url: '/api/assets/statistics/',
          method: 'get'
        })
        
        if (response) {
          statistics.value[0].value = response.total || 0
          statistics.value[1].value = response.inUse || 0
          statistics.value[2].value = response.idle || 0
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
  padding: 20px;
  
  .el-card {
    margin-bottom: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .card-body {
      text-align: center;
      padding: 20px;
      
      h2 {
        margin: 0;
        font-size: 24px;
        color: #409EFF;
      }
    }
  }
}
</style> 