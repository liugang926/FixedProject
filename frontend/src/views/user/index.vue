<template>
  <div class="app-container">
    <!-- 搜索栏 -->
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="用户名/邮箱/部门"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter="handleFilter"
      />
      <el-select
        v-model="listQuery.role"
        placeholder="角色"
        clearable
        class="filter-item"
        style="width: 130px"
      >
        <el-option
          v-for="item in roleOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-button
        class="filter-item"
        type="primary"
        icon="Search"
        @click="handleFilter"
      >
        搜索
      </el-button>
      <el-button
        v-permission="['admin', 'create_user']"
        class="filter-item"
        type="primary"
        icon="Plus"
        @click="handleCreate"
      >
        添加用户
      </el-button>
    </div>

    <!-- 用户列表 -->
    <el-table
      :data="list"
      border
      style="width: 100%"
      v-loading="listLoading"
    >
      <el-table-column label="用户名" prop="username" align="center" />
      <el-table-column label="姓名" prop="display_name" align="center" />
      <el-table-column label="部门" prop="department" align="center" />
      <el-table-column label="角色" align="center">
        <template #default="{ row }">
          <el-tag
            v-for="role in row.roles"
            :key="role.id"
            :type="role.code === 'admin' ? 'danger' : ''"
            style="margin-right: 5px"
          >
            {{ role.name }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" align="center">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">
            {{ row.is_active ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="300">
        <template #default="{ row }">
          <el-button
            v-permission="['admin', 'edit_user']"
            type="primary"
            size="small"
            @click="handleUpdate(row)"
          >
            编辑
          </el-button>
          <el-button
            type="warning"
            size="small"
            @click="handleAssignRole(row)"
          >
            分配角色
          </el-button>
          <el-button
            v-if="row.is_active"
            type="danger"
            size="small"
            @click="handleLock(row)"
          >
            锁定
          </el-button>
          <el-button
            v-else
            type="success"
            size="small"
            @click="handleUnlock(row)"
          >
            解锁
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

    <!-- 用户表单对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogFormVisible"
      width="500px"
    >
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="temp.username" />
        </el-form-item>
        <el-form-item label="姓名" prop="display_name">
          <el-input v-model="temp.display_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="temp.email" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="temp.phone" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="temp.department" />
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model="temp.position" />
        </el-form-item>
        <el-form-item v-if="dialogStatus === 'create'" label="密码" prop="password">
          <el-input v-model="temp.password" type="password" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">
            确认
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 角色分配对话框 -->
    <el-dialog
      title="分配角色"
      v-model="dialogRoleVisible"
      width="400px"
    >
      <el-checkbox-group v-model="selectedRoles">
        <el-checkbox
          v-for="role in roleList"
          :key="role.id"
          :label="role.id"
        >
          {{ role.name }}
        </el-checkbox>
      </el-checkbox-group>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogRoleVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmAssignRole">确认</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getUserList,
  createUser,
  updateUser,
  lockUser,
  unlockUser,
  getRoleList,
  assignRole,
  removeRole
} from '@/api/user'
import Pagination from '@/components/Pagination/index.vue'
import { usePermission } from '@/hooks/usePermission'

export default defineComponent({
  name: 'UserManagement',
  components: { Pagination },
  setup() {
    const { hasPermission } = usePermission()

    // 数据列表相关
    const list = ref([])
    const total = ref(0)
    const listLoading = ref(true)
    const listQuery = reactive({
      page: 1,
      limit: 10,
      search: '',
      role: ''
    })

    // 角色选项
    const roleOptions = ref([
      { label: '管理员', value: 'admin' },
      { label: '普通用户', value: 'user' }
    ])

    // 表单相关
    const dialogFormVisible = ref(false)
    const dialogStatus = ref('')
    const dialogTitle = ref('')
    const temp = reactive({
      id: undefined,
      username: '',
      display_name: '',
      email: '',
      phone: '',
      department: '',
      position: '',
      password: ''
    })

    // 表单验证规则
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, message: '长度至少为3个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ]
    }

    // 角色分配相关
    const dialogRoleVisible = ref(false)
    const roleList = ref([])
    const selectedRoles = ref([])
    const currentUser = ref(null)

    // 获取用户列表
    const getList = async () => {
      listLoading.value = true
      try {
        const { data, total: totalCount } = await getUserList(listQuery)
        list.value = data
        total.value = totalCount
      } catch (error) {
        console.error('Failed to get user list:', error)
      }
      listLoading.value = false
    }

    // 搜索
    const handleFilter = () => {
      listQuery.page = 1
      getList()
    }

    // 重置表单
    const resetTemp = () => {
      Object.assign(temp, {
        id: undefined,
        username: '',
        display_name: '',
        email: '',
        phone: '',
        department: '',
        position: '',
        password: ''
      })
    }

    // 创建用户
    const handleCreate = () => {
      if (!hasPermission(['admin', 'create_user'])) {
        ElMessage.error('没有权限执行此操作')
        return
      }
      resetTemp()
      dialogStatus.value = 'create'
      dialogTitle.value = '创建用户'
      dialogFormVisible.value = true
    }

    // 更新用户
    const handleUpdate = (row) => {
      Object.assign(temp, row)
      dialogStatus.value = 'update'
      dialogTitle.value = '编辑用户'
      dialogFormVisible.value = true
    }

    // 提交创建
    const createData = async () => {
      try {
        await createUser(temp)
        dialogFormVisible.value = false
        ElMessage.success('创建成功')
        getList()
      } catch (error) {
        console.error('Failed to create user:', error)
      }
    }

    // 提交更新
    const updateData = async () => {
      try {
        await updateUser(temp.id, temp)
        dialogFormVisible.value = false
        ElMessage.success('更新成功')
        getList()
      } catch (error) {
        console.error('Failed to update user:', error)
      }
    }

    // 锁定用户
    const handleLock = (row) => {
      ElMessageBox.prompt('请输入锁定原因', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /\S+/,
        inputErrorMessage: '锁定原因不能为空'
      }).then(({ value }) => {
        lockUser(row.id, value).then(() => {
          ElMessage.success('用户已锁定')
          getList()
        })
      })
    }

    // 解锁用户
    const handleUnlock = (row) => {
      ElMessageBox.confirm('确定要解锁该用户吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        unlockUser(row.id).then(() => {
          ElMessage.success('用户已解锁')
          getList()
        })
      })
    }

    // 分配角色
    const handleAssignRole = async (row) => {
      currentUser.value = row
      try {
        const { data } = await getRoleList()
        roleList.value = data
        selectedRoles.value = row.roles.map(role => role.id)
        dialogRoleVisible.value = true
      } catch (error) {
        console.error('Failed to get role list:', error)
      }
    }

    // 确认分配角色
    const confirmAssignRole = async () => {
      try {
        // 移除旧角色
        const oldRoles = currentUser.value.roles
        for (const role of oldRoles) {
          if (!selectedRoles.value.includes(role.id)) {
            await removeRole(role.id)
          }
        }

        // 添加新角色
        for (const roleId of selectedRoles.value) {
          if (!oldRoles.find(r => r.id === roleId)) {
            await assignRole({
              user_id: currentUser.value.id,
              role_id: roleId
            })
          }
        }

        dialogRoleVisible.value = false
        ElMessage.success('角色分配成功')
        getList()
      } catch (error) {
        console.error('Failed to assign roles:', error)
      }
    }

    onMounted(() => {
      getList()
    })

    return {
      list,
      total,
      listLoading,
      listQuery,
      roleOptions,
      dialogFormVisible,
      dialogStatus,
      dialogTitle,
      temp,
      rules,
      dialogRoleVisible,
      roleList,
      selectedRoles,
      handleFilter,
      handleCreate,
      handleUpdate,
      createData,
      updateData,
      handleLock,
      handleUnlock,
      handleAssignRole,
      confirmAssignRole,
      hasPermission
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

.dialog-footer {
  text-align: right;
  padding-top: 20px;
}
</style> 