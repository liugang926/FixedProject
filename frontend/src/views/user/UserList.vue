<template>
  <div class="user-list">
    <el-card>
      <template #header>
        <div class="header">
          <span>用户管理</span>
          <div class="right">
            <el-button type="primary" @click="handleAdd">新增用户</el-button>
            <el-button @click="handleImport">批量导入</el-button>
            <el-button @click="handleExport">导出</el-button>
          </div>
        </div>
      </template>

      <el-table :data="userList" border style="width: 100%">
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="is_active" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_locked" label="锁定状态">
          <template #default="{ row }">
            <el-tag :type="row.is_locked ? 'danger' : 'success'">
              {{ row.is_locked ? '已锁定' : '正常' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button 
                size="small" 
                :type="row.is_locked ? 'success' : 'warning'"
                @click="handleLockToggle(row)"
              >
                {{ row.is_locked ? '解锁' : '锁定' }}
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="handleDelete(row)"
              >
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 用户表单对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="userForm.phone" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogType === 'add'">
          <el-input
            v-model="userForm.password"
            type="password"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserList, createUser, updateUser, deleteUser, lockUser, unlockUser } from '@/api/user'

export default defineComponent({
  name: 'UserList',
  setup() {
    const userList = ref([])
    const dialogVisible = ref(false)
    const dialogType = ref('add')
    const userFormRef = ref(null)

    const userForm = reactive({
      id: '',
      username: '',
      email: '',
      phone: '',
      password: ''
    })

    const userRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { pattern: /^[a-zA-Z][a-zA-Z0-9_]{3,19}$/, message: '用户名格式不正确', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 8, max: 16, message: '密码长度在8-16位之间', trigger: 'blur' }
      ]
    }

    const dialogTitle = computed(() => dialogType.value === 'add' ? '新增用户' : '编辑用户')

    // 获取用户列表
    const fetchData = async () => {
      try {
        const { data } = await getUserList()
        userList.value = data
      } catch (error) {
        console.error('获取用户列表失败:', error)
        ElMessage.error('获取用户列表失败')
      }
    }

    // 处理用户表单提交
    const handleSubmit = async () => {
      await userFormRef.value?.validate()
      try {
        if (dialogType.value === 'add') {
          await createUser(userForm)
          ElMessage.success('创建成功')
        } else {
          await updateUser(userForm.id, userForm)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchData()
      } catch (error) {
        ElMessage.error(error.response?.data?.message || '操作失败')
      }
    }

    // 处理添加用户
    const handleAdd = () => {
      dialogType.value = 'add'
      userForm.id = ''
      userForm.username = ''
      userForm.email = ''
      userForm.phone = ''
      userForm.password = ''
      dialogVisible.value = true
    }

    // 处理编辑用户
    const handleEdit = (row) => {
      dialogType.value = 'edit'
      userForm.id = row.id
      userForm.username = row.username
      userForm.email = row.email
      userForm.phone = row.phone
      dialogVisible.value = true
    }

    // 处理删除用户
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `确定要删除用户 ${row.username} 吗？`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          await deleteUser(row.id)
          ElMessage.success('删除成功')
          fetchData()
        } catch (error) {
          ElMessage.error(error.response?.data?.message || '删除失败')
        }
      })
    }

    // 处理锁定/解锁用户
    const handleLockToggle = (row) => {
      const action = row.is_locked ? '解锁' : '锁定'
      ElMessageBox.prompt(
        `请输入${action}原因`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /.+/,
          inputErrorMessage: '请输入原因'
        }
      ).then(async ({ value: reason }) => {
        try {
          if (row.is_locked) {
            await unlockUser(row.id, reason)
          } else {
            await lockUser(row.id, reason)
          }
          ElMessage.success(`${action}成功`)
          fetchData()
        } catch (error) {
          ElMessage.error(error.response?.data?.message || `${action}失败`)
        }
      })
    }

    // 处理批量导入
    const handleImport = () => {
      ElMessage.info('批量导入功能开发中')
    }

    // 处理导出
    const handleExport = () => {
      ElMessage.info('导出功能开发中')
    }

    // 初始化数据
    onMounted(() => {
      fetchData()
    })

    return {
      userList,
      dialogVisible,
      dialogType,
      userForm,
      userRules,
      userFormRef,
      dialogTitle,
      handleSubmit,
      handleAdd,
      handleEdit,
      handleDelete,
      handleLockToggle,
      handleImport,
      handleExport
    }
  }
})
</script>

<style lang="scss" scoped>
.user-list {
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .right {
      display: flex;
      gap: 10px;
    }
  }
}
</style> 