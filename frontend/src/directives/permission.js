import store from '@/store'

function checkPermission(el, binding) {
  const { value } = binding
  const roles = store.state.user.roles
  const permissions = store.state.user.permissions

  if (value && value instanceof Array) {
    if (value.length > 0) {
      const permissionRoles = value
      const hasPermission = roles.some(role => {
        return permissionRoles.includes(role)
      })

      // 检查具体权限
      const hasSpecificPermission = permissions.some(permission => {
        return permissionRoles.includes(permission)
      })

      if (!hasPermission && !hasSpecificPermission) {
        el.parentNode && el.parentNode.removeChild(el)
      }
    }
  } else {
    throw new Error(`需要指定权限，例如 v-permission="['admin','edit_user']"`)
  }
}

export default {
  mounted(el, binding) {
    checkPermission(el, binding)
  },
  updated(el, binding) {
    checkPermission(el, binding)
  }
} 