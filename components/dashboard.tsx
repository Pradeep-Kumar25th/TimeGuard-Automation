'use client'

import { motion } from 'framer-motion'
import { EnhancedAutomationDashboard } from '@/components/enhanced-automation-dashboard'

interface DashboardProps {
  activeTab: string
}

export function Dashboard({ activeTab }: DashboardProps) {
  const renderContent = () => {
    if (activeTab === 'automation') {
        return (
          <motion.div 
            className="space-y-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <EnhancedAutomationDashboard />
            </motion.div>
          </motion.div>
        )
    }
    
    return null
  }

  return (
    <div className="p-6">
      {renderContent()}
    </div>
  )
}
