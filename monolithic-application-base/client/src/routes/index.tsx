import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom'
import Layout from '@/layout/layout'
import LoginPage from '@/pages/Login'
import Dashboard from '@/pages/Dashboard'
import Settings from '@/pages/Settings'
import UserManagement from '@/pages/UserManagement'
import Forbidden from '@/pages/Forbidden'
import NotFound from '@/pages/NotFound'
import ProtectedRoute from '@/components/ProtectedRoute'
import Permissions from '@/pages/Permissions'

const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    // Outer shell: must be authenticated
    path: '/',
    element: (
      <ProtectedRoute>
        <Layout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: (
          <ProtectedRoute requirePermission="canViewDashboard">
            <Dashboard />
          </ProtectedRoute>
        ),
      },
      {
        path: 'settings',
        element: (
          <ProtectedRoute requirePermission="canViewSettings">
            <Settings />
          </ProtectedRoute>
        ),
      },
      {
        // Strictly admin-only — not configurable via permissions page
        path: 'user-management',
        element: (
          <ProtectedRoute requireRole="admin">
            <UserManagement />
          </ProtectedRoute>
        ),
      },
      {
        // Strictly admin-only — not configurable via permissions page
        path: 'permissions',
        element: (
          <ProtectedRoute requireRole="admin">
            <Permissions />
          </ProtectedRoute>
        ),
      },
      {
        path: 'forbidden',
        element: <Forbidden />,
      },
      // Add your custom routes here
      // Example:
      // {
      //   path: 'your-feature',
      //   element: (
      //     <ProtectedRoute requirePermission="canViewYourFeature">
      //       <YourFeaturePage />
      //     </ProtectedRoute>
      //   ),
      // },
      {
        path: '*',
        element: <NotFound />,
      },
    ],
  },
  {
    path: '*',
    element: <Navigate to="/" replace />,
  },
])

export default function AppRouter() {
  return <RouterProvider router={router} />
}
