<template>
  <div class="app-container">
    <!-- 搜索栏 -->
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="操作描述/IP/浏览器"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter="handleFilter"
      />
      <el-select
        v-model="listQuery.action"
        placeholder="操作类型"
        clearable
        class="filter-item"
        style="width: 130px"
      >
        <el-option
          v-for="item in actionOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-select
        v-model="listQuery.module"
        placeholder="功能模块"
        clearable
        class="filter-item"
        style="width: 130px"
      >
        <el-option
          v-for="item in moduleOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        class="filter-item"
        value-format="yyyy-MM-dd"
        @change="handleDateRangeChange"
      />
      <el-button
        class="filter-item"
        type="primary"
        icon="Search"
        @click="handleFilter"
      >
        搜索
      </el-button>
      <el-button
        class="filter-item"
        type="success"
        icon="Download"
        @click="handleExport"
      >
        导出
      </el-button>
    </div>

    <!-- 日志列表 -->
    <el-table
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%"
    >
      <el-table-column label="操作人" prop="user.username" align="center" />
      <el-table-column label="操作类型" align="center">
        <template #default="{ row }">
          <el-tag :type="getActionTagType(row.action)">
            {{ getActionLabel(row.action) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="功能模块" prop="module" align="center" />
      <el-table-column label="操作描述" prop="description" align="center" />
      <el-table-column label="IP地址" prop="ip" align="center" width="120" />
      <el-table-column label="浏览器" prop="browser" align="center" />
      <el-table-column label="操作系统" prop="os" align="center" />
      <el-table-column label="状态" align="center" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status ? 'success' : 'danger'">
            {{ row.status ? '成功' : '失败' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作时间" align="center" width="160">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="80">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="handleDetail(row)"
          >
            详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="listQuery.page"
      v-model:limit="listQuery.limit"
      @pagination="getList"
    />

    <!-- 详情对话框 -->
    <el-dialog
      title="操作详情"
      v-model="dialogVisible"
      width="600px"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="请求地址">
          {{ currentLog.url }}
        </el-descriptions-item>
        <el-descriptions-item label="请求方法">
          {{ currentLog.method }}
        </el-descriptions-item>
        <el-descriptions-item label="请求参数">
          <pre>{{ formatJson(currentLog.params) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="错误信息" v-if="!currentLog.status">
          {{ currentLog.error_msg }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getOperationLogs, exportOperationLogs } from '@/api/operationLog'
import Pagination from '@/components/Pagination/index.vue'

export default defineComponent({
  name: 'OperationLog',
  components: { Pagination },
  setup() {
    // 列表数据
    const list = ref([])
    const total = ref(0)
    const listLoading = ref(true)
    const listQuery = reactive({
      page: 1,
      limit: 20,
      search: '',
      action: '',
      module: '',
      start_date: '',
      end_date: ''
    })

    // 选项数据
    const actionOptions = [
      { label: '创建', value: 'create' },
      { label: '更新', value: 'update' },
      { label: '删除', value: 'delete' },
      { label: '导出', value: 'export' },
      { label: '导入', value: 'import' },
      { label: '其他', value: 'other' }
    ]

    const moduleOptions = [
      { label: '用户管理', value: 'user' },
      { label: '角色管理', value: 'role' },
      { label: '权限管理', value: 'permission' }
    ]

    // 日期范围
    const dateRange = ref([])

    // 详情对话框
    const dialogVisible = ref(false)
    const currentLog = ref({})

    // 获取列表数据
    const getList = async () => {
      listLoading.value = true
      try {
        const { data } = await getOperationLogs(listQuery)
        list.value = data.results
        total.value = data.count
      } catch (error) {
        console.error('Failed to get operation logs:', error)
      }
      listLoading.value = false
    }

    // 处理搜索
    const handleFilter = () => {
      listQuery.page = 1
      getList()
    }

    // 处理日期范围变化
    const handleDateRangeChange = (val) => {
      if (val) {
        listQuery.start_date = val[0]
        listQuery.end_date = val[1]
      } else {
        listQuery.start_date = ''
        listQuery.end_date = ''
      }
    }

    // 处理导出
    const handleExport = async () => {
      try {
        const response = await exportOperationLogs(listQuery)
        const blob = new Blob([response.data])
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = '操作日志.xlsx'
        link.click()
      } catch (error) {
        ElMessage.error('导出失败')
      }
    }

    // 处理详情
    const handleDetail = (row) => {
      currentLog.value = row
      dialogVisible.value = true
    }

    // 格式化 JSON
    const formatJson = (json) => {
      try {
        return JSON.stringify(json, null, 2)
      } catch (e) {
        return json
      }
    }

    // 获取操作类型标签样式
    const getActionTagType = (action) => {
      const types = {
        create: 'success',
        update: 'warning',
        delete: 'danger',
        export: 'info',
        import: 'info',
        other: ''
      }
      return types[action] || ''
    }

    // 获取操作类型标签文本
    const getActionLabel = (action) => {
      const labels = {
        create: '创建',
        update: '更新',
        delete: '删除',
        export: '导出',
        import: '导入',
        other: '其他'
      }
      return labels[action] || action
    }

    onMounted(() => {
      getList()
    })

    return {
      list,
      total,
      listLoading,
      listQuery,
      actionOptions,
      moduleOptions,
      dateRange,
      dialogVisible,
      currentLog,
      handleFilter,
      handleDateRangeChange,
      handleExport,
      handleDetail,
      formatJson,
      getActionTagType,
      getActionLabel
    }
  }
})
</script>

<style lang="scss" scoped>
.filter-container {
  padding-bottom: 10px;
  .filter-item {
    margin-right: 10px;
  }
}

pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style> 