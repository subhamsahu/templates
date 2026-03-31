import { useAppSelector } from '@/store/hooks'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Users, Settings, Shield } from 'lucide-react'

export default function Dashboard() {
  const user = useAppSelector((state) => state.auth.user)

  return (
    <div className="flex flex-1 flex-col gap-6 p-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-sm text-muted-foreground mt-0.5">
          Welcome back, {user?.username}!
        </p>
      </div>

      {/* Welcome Card */}
      <Card>
        <CardHeader>
          <CardTitle>🚀 Welcome to Your Application Base Template</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            This is a clean starting point for building your application. The authentication system,
            user management, and permission framework are ready to use.
          </p>
          
          <div className="grid gap-4 md:grid-cols-3 pt-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-blue-100 dark:bg-blue-900/30">
                    <Users className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">User Management</p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {user?.role === 'admin' ? 'Manage users & roles' : 'View only'}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-purple-100 dark:bg-purple-900/30">
                    <Shield className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Role: {user?.role}</p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      Permission-based access
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-green-100 dark:bg-green-900/30">
                    <Settings className="w-5 h-5 text-green-600 dark:text-green-400" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Settings</p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      Customize your app
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>

      {/* Getting Started */}
      <Card>
        <CardHeader>
          <CardTitle>Getting Started</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="space-y-2">
            <h4 className="font-semibold text-sm">📋 Next Steps:</h4>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-2">
              <li>Add your custom models in <code className="text-xs bg-muted px-1 py-0.5 rounded">server/app/models.py</code></li>
              <li>Create your API endpoints in <code className="text-xs bg-muted px-1 py-0.5 rounded">server/app/routers/</code></li>
              <li>Build your pages in <code className="text-xs bg-muted px-1 py-0.5 rounded">client/src/pages/</code></li>
              <li>Update permissions in <code className="text-xs bg-muted px-1 py-0.5 rounded">DEFAULT_ROLE_PERMISSIONS</code></li>
              <li>Customize the navigation in <code className="text-xs bg-muted px-1 py-0.5 rounded">app-sidebar.tsx</code></li>
            </ul>
          </div>

          <div className="pt-2 border-t">
            <p className="text-xs text-muted-foreground">
              💡 Check the README.md file for detailed customization instructions and examples.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
