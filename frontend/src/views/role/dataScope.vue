<template>
  <div class="app-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>数据权限配置</span>
        </div>
      </template>
      
      <el-form
        ref="form"
        :model="scopeForm"
        label-width="120px"
        v-loading="loading"
      >
        <el-form-item label="角色名称">
          <span>{{ currentRole.name }}</span>
        </el-form-item>
        
        <el-form-item label="数据范围">
          <el-radio-group v-model="scopeForm.scope">
            <el-radio
              v-for="item in scopeOptions"
              :key="item.value"
              :label="item.value"
            >
              {{ item.label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item
          label="自定义部门"
          v-if="scopeForm.scope === 'custom'"
        >
          <el-tree
            ref="deptTree"
            :data="departmentTree"
            show-checkbox
            node-key="id"
            :props="defaultProps"
            @check="handleCheck"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            @click="handleSubmit"
            :loading="submitting"
          >
            保存配置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getDataScope, updateDataScope, getDepartmentTree } from '@/api/dataScope'
import { getRoleDetail } from '@/api/role'

export default defineComponent({
  name: 'DataScope',
  setup() {
    const route = useRoute()
    const loading = ref(false)
    const submitting = ref(false)
    const currentRole = ref({})
    const departmentTree = ref([])
    const deptTree = ref(null)
    
    // 表单数据
    const scopeForm = reactive({
      scope: 'personal',
      departments: []
    })
    
    // 数据范围选项
    const scopeOptions = [
      { label: '全部数据', value: 'all' },
      { label: '本部门及以下数据', value: 'department_and_below' },
      { label: '本部门数据', value: 'department' },
      { label: '仅个人数据', value: 'personal' },
      { label: '自定义数据', value: 'custom' }
    ]
    
    // 部门树配置
    const defaultProps = {
      children: 'children',
      label: 'name'
    }
    
    // 获取角色信息
    const getRoleInfo = async () => {
      try {
        const { data } = await getRoleDetail(route.params.id)
        currentRole.value = data
      } catch (error) {
        console.error('Failed to get role info:', error)
      }
    }
    
    // 获取数据权限配置
    const getScope = async () => {
      loading.value = true
      try {
        const { data } = await getDataScope(route.params.id)
        scopeForm.scope = data.scope
        scopeForm.departments = data.departments || []
        
        // 设置选中的部门
        if (scopeForm.scope === 'custom' && scopeForm.departments.length > 0) {
          await nextTick()
          if (deptTree.value) {
            deptTree.value.setCheckedKeys(scopeForm.departments)
          }
        }
      } catch (error) {
        console.error('Failed to get data scope:', error)
      }
      loading.value = false
    }
    
    // 获取部门树
    const getDeptTree = async () => {
      try {
        const { data } = await getDepartmentTree()
        departmentTree.value = data
      } catch (error) {
        console.error('Failed to get department tree:', error)
      }
    }
    
    // 处理部门选择
    const handleCheck = (data, { checkedKeys }) => {
      scopeForm.departments = checkedKeys
    }
    
    // 提交配置
    const handleSubmit = async () => {
      submitting.value = true
      try {
        await updateDataScope(route.params.id, scopeForm)
        ElMessage.success('配置保存成功')
      } catch (error) {
        console.error('Failed to update data scope:', error)
        ElMessage.error('配置保存失败')
      }
      submitting.value = false
    }
    
    onMounted(() => {
      getRoleInfo()
      getScope()
      getDeptTree()
    })
    
    return {
      loading,
      submitting,
      currentRole,
      scopeForm,
      scopeOptions,
      departmentTree,
      defaultProps,
      deptTree,
      handleCheck,
      handleSubmit
    }
  }
})
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-card {
  width: 100%;
  margin-bottom: 20px;
}
</style> 