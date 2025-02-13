<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button
        class="filter-item"
        type="primary"
        icon="Plus"
        @click="handleCreate"
      >
        添加角色
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
      <el-table-column label="角色名称" prop="name" align="center" />
      <el-table-column label="角色代码" prop="code" align="center" />
      <el-table-column label="描述" prop="description" align="center" />
      <el-table-column label="创建时间" align="center">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="300">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="handleUpdate(row)"
          >
            编辑
          </el-button>
          <el-button
            type="success"
            size="small"
            @click="handlePermission(row)"
          >
            权限设置
          </el-button>
          <el-button
            type="warning"
            size="small"
            @click="handleDataScope(row)"
          >
            数据权限
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

    <!-- 角色表单对话框 -->
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
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="角色代码" prop="code">
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

    <!-- 权限设置对话框 -->
    <el-dialog
      title="权限设置"
      v-model="dialogPermissionVisible"
    >
      <el-checkbox-group v-model="selectedPermissions">
        <el-checkbox
          v-for="permission in permissionList"
          :key="permission.id"
          :label="permission.id"
        >
          {{ permission.name }}
        </el-checkbox>
      </el-checkbox-group>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogPermissionVisible = false">取消</el-button>
          <el-button type="primary" @click="updatePermissions">确认</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getRoleList,
  createRole,
  updateRole,
  deleteRole
} from '@/api/role'
import { getPermissionList } from '@/api/user'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'RoleManagement',
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
        { required: true, message: '请输入角色名称', trigger: 'blur' },
        { min: 2, message: '长度至少为2个字符', trigger: 'blur' }
      ],
      code: [
        { required: true, message: '请输入角色代码', trigger: 'blur' },
        { pattern: /^[A-Z_]+$/, message: '只能包含大写字母和下划线', trigger: 'blur' }
      ]
    }

    // 权限相关
    const dialogPermissionVisible = ref(false)
    const permissionList = ref([])
    const selectedPermissions = ref([])
    const currentRole = ref(null)

    // 路由相关
    const router = useRouter()

    // 获取角色列表
    const getList = async () => {
      listLoading.value = true
      try {
        const { data } = await getRoleList()
        list.value = data
      } catch (error) {
        console.error('Failed to get role list:', error)
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

    // 创建角色
    const handleCreate = () => {
      resetTemp()
      dialogStatus.value = 'create'
      dialogTitle.value = '创建角色'
      dialogFormVisible.value = true
    }

    // 更新角色
    const handleUpdate = (row) => {
      Object.assign(temp, row)
      dialogStatus.value = 'update'
      dialogTitle.value = '编辑角色'
      dialogFormVisible.value = true
    }

    // 提交创建
    const createData = async () => {
      try {
        await createRole(temp)
        dialogFormVisible.value = false
        ElMessage.success('创建成功')
        getList()
      } catch (error) {
        console.error('Failed to create role:', error)
      }
    }

    // 提交更新
    const updateData = async () => {
      try {
        await updateRole(temp.id, temp)
        dialogFormVisible.value = false
        ElMessage.success('更新成功')
        getList()
      } catch (error) {
        console.error('Failed to update role:', error)
      }
    }

    // 删除角色
    const handleDelete = (row) => {
      ElMessageBox.confirm('确定要删除该角色吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteRole(row.id)
          ElMessage.success('删除成功')
          getList()
        } catch (error) {
          console.error('Failed to delete role:', error)
        }
      })
    }

    // 权限设置
    const handlePermission = async (row) => {
      currentRole.value = row
      try {
        // 获取所有权限列表
        const { data } = await getPermissionList()
        permissionList.value = data
        // 设置当前角色已有的权限
        selectedPermissions.value = row.permissions.map(p => p.id)
        dialogPermissionVisible.value = true
      } catch (error) {
        console.error('Failed to get permission list:', error)
      }
    }

    // 更新权限
    const updatePermissions = async () => {
      try {
        await updateRole(currentRole.value.id, {
          ...currentRole.value,
          permissions: selectedPermissions.value
        })
        dialogPermissionVisible.value = false
        ElMessage.success('权限设置成功')
        getList()
      } catch (error) {
        console.error('Failed to update permissions:', error)
      }
    }

    // 处理数据权限配置
    const handleDataScope = (row) => {
      router.push(`/role/data-scope/${row.id}`)
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
      dialogPermissionVisible,
      permissionList,
      selectedPermissions,
      handleCreate,
      handleUpdate,
      handleDelete,
      handlePermission,
      createData,
      updateData,
      updatePermissions,
      handleDataScope
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