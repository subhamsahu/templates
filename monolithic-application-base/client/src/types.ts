/* ---------------------------------------------------
 * Shared TypeScript types mirroring server schemas.
 * ------------------------------------------------- */

// ── Auth ─────────────────────────────────────────────

export interface UserResponse {
  id: number
  username: string
  role: string
  created_at: string
}

export interface Token {
  access_token: string
  token_type: string
  user: UserResponse
}

// ── Permissions ──────────────────────────────────────

export interface RolePermissions {
  id: number
  role: string
  permissions: Record<string, boolean>
  updated_at: string
}

export interface PermissionSet {
  canViewDashboard: boolean
  canViewUserManagement: boolean
  canManageUsers: boolean
  canViewSettings: boolean
  // Add your custom permissions here
}

/** Map of role name → its PermissionSet (only staff + employee are returned) */
export type RolePermissionsMap = Record<string, PermissionSet>

// ─── Add Your Custom Types Below ─────────────────────
// Add your application-specific TypeScript interfaces here
// Example:
// export interface YourModel {
//   id: number
//   name: string
//   created_at: string
// }

