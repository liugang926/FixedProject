<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button
        class="filter-item"
        type="primary"
        icon="Plus"
        @click="handleCreate"
      >
        添加权限
      </el-button>
    </div>

    <el-table
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%"
    >
      <el-table-column label="权限名称" prop="name" align="center" />
      <el-table-column label="权限代码" prop="code" align="center" />
      <el-table-column label="描述" prop="description" align="center" />
      <el-table-column label="创建时间" align="center">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="200">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="handleUpdate(row)"
          >
            编辑
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 权限表单对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogFormVisible"
    >
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="right"
        label-width="100px"
      >
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="权限代码" prop="code">
          <el-input v-model="temp.code" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="temp.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button
            type="primary"
            @click="dialogStatus === 'create' ? createData() : updateData()"
          >
            确认
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getPermissionList,
  createPermission,
  updatePermission,
  deletePermission
} from '@/api/permission'

export default defineComponent({
  name: 'PermissionManagement',
  setup() {
    // 数据列表相关
    const list = ref([])
    const listLoading = ref(true)

    // 表单相关
    const dialogFormVisible = ref(false)
    const dialogStatus = ref('')
    const dialogTitle = ref('')
    const temp = reactive({
      id: undefined,
      name: '',
      code: '',
      description: ''
    })

    // 表单验证规则
    const rules = {
      name: [
        { required: true, message: '请输入权限名称', trigger: 'blur' },
        { min: 2, message: '长度至少为2个字符', trigger: 'blur' }
      ],
      code: [
        { required: true, message: '请输入权限代码', trigger: 'blur' },
        { pattern: /^[A-Z_]+$/, message: '只能包含大写字母和下划线', trigger: 'blur' }
      ]
    }

    // 获取权限列表
    const getList = async () => {
      listLoading.value = true
      try {
        const { data } = await getPermissionList()
        list.value = data
      } catch (error) {
        console.error('Failed to get permission list:', error)
      }
      listLoading.value = false
    }

    // 重置表单
    const resetTemp = () => {
      Object.assign(temp, {
        id: undefined,
        name: '',
        code: '',
        description: ''
      })
    }

    // 创建权限
    const handleCreate = () => {
      resetTemp()
      dialogStatus.value = 'create'
      dialogTitle.value = '创建权限'
      dialogFormVisible.value = true
    }

    // 更新权限
    const handleUpdate = (row) => {
      Object.assign(temp, row)
      dialogStatus.value = 'update'
      dialogTitle.value = '编辑权限'
      dialogFormVisible.value = true
    }

    // 提交创建
    const createData = async () => {
      try {
        await createPermission(temp)
        dialogFormVisible.value = false
        ElMessage.success('创建成功')
        getList()
      } catch (error) {
        console.error('Failed to create permission:', error)
      }
    }

    // 提交更新
    const updateData = async () => {
      try {
        await updatePermission(temp.id, temp)
        dialogFormVisible.value = false
        ElMessage.success('更新成功')
        getList()
      } catch (error) {
        console.error('Failed to update permission:', error)
      }
    }

    // 删除权限
    const handleDelete = (row) => {
      ElMessageBox.confirm('确定要删除该权限吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deletePermission(row.id)
          ElMessage.success('删除成功')
          getList()
        } catch (error) {
          console.error('Failed to delete permission:', error)
        }
      })
    }

    onMounted(() => {
      getList()
    })

    return {
      list,
      listLoading,
      dialogFormVisible,
      dialogStatus,
      dialogTitle,
      temp,
      rules,
      handleCreate,
      handleUpdate,
      handleDelete,
      createData,
      updateData
    }
  }
})
</script>

<style lang="scss" scoped>
.filter-container {
  padding-bottom: 10px;
}

.dialog-footer {
  text-align: right;
  padding-top: 20px;
}
</style> 