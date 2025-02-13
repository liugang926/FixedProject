const PERMISSIONS_KEY = 'user_permissions'
const ROLES_KEY = 'user_roles'

export function getPermissions() {
  const permissionsStr = localStorage.getItem(PERMISSIONS_KEY)
  return permissionsStr ? JSON.parse(permissionsStr) : []
}

export function setPermissions(permissions) {
  localStorage.setItem(PERMISSIONS_KEY, JSON.stringify(permissions))
}

export function getRoles() {
  const rolesStr = localStorage.getItem(ROLES_KEY)
  return rolesStr ? JSON.parse(rolesStr) : []
}

export function setRoles(roles) {
  localStorage.setItem(ROLES_KEY, JSON.stringify(roles))
}

export function clearPermissionCache() {
  localStorage.removeItem(PERMISSIONS_KEY)
  localStorage.removeItem(ROLES_KEY)
} 