import { computed } from 'vue'
import { useStore } from 'vuex'

export function usePermission() {
  const store = useStore()
  
  const roles = computed(() => store.state.user.roles)
  const permissions = computed(() => store.state.user.permissions)

  function hasPermission(permissionRoles) {
    if (!permissionRoles || permissionRoles.length === 0) {
      return true
    }

    // 检查角色权限
    const hasRole = roles.value.some(role => permissionRoles.includes(role))
    if (hasRole) return true

    // 检查具体权限
    return permissions.value.some(permission => permissionRoles.includes(permission))
  }

  function hasRole(roleList) {
    if (!roleList || roleList.length === 0) {
      return true
    }
    return roles.value.some(role => roleList.includes(role))
  }

  return {
    hasPermission,
    hasRole,
    roles,
    permissions
  }
} 