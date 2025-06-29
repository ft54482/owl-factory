import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import SuperAdminRoute from './components/SuperAdminRoute'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import Dashboard from './pages/Dashboard'
import AnalysisPage from './pages/AnalysisPage'
import ReportDetail from './pages/ReportDetail'
import PromptManager from './pages/PromptManager'
import ReportManagement from './pages/ReportManagement'
import AdminDashboard from './pages/AdminDashboard'
import UserManagement from './pages/UserManagement'
import SystemConfig from './pages/SystemConfig'
import LogManagement from './pages/LogManagement'
import GpuManagement from './pages/GpuManagement'
import { ToastProvider } from './components/ui/Toast'
import { AuthProvider } from './contexts/AuthContext'

function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <Router>
        <Routes>
          {/* 首页和登录页面不使用Layout */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          
          {/* 其他页面使用Layout和路由保护 */}
          <Route path="/*" element={
            <ProtectedRoute>
              <div className="min-h-screen bg-background">
                <Layout>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Routes>
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/analysis" element={<AnalysisPage />} />
                      <Route path="/report/:id" element={<ReportDetail />} />
                      <Route path="/prompts" element={<PromptManager />} />
                      <Route path="/reports" element={<ReportManagement />} />
                      <Route path="/admin" element={<SuperAdminRoute><AdminDashboard /></SuperAdminRoute>} />
                      <Route path="/admin/users" element={<SuperAdminRoute><UserManagement /></SuperAdminRoute>} />
                      <Route path="/admin/config" element={<SuperAdminRoute><SystemConfig /></SuperAdminRoute>} />
                      <Route path="/admin/logs" element={<SuperAdminRoute><LogManagement /></SuperAdminRoute>} />
                      <Route path="/admin/gpu" element={<SuperAdminRoute><GpuManagement /></SuperAdminRoute>} />
                    </Routes>
                  </motion.div>
                </Layout>
              </div>
            </ProtectedRoute>
          } />
        </Routes>
        </Router>
      </ToastProvider>
    </AuthProvider>
  )
}

export default App