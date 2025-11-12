'use client'

import { Dashboard } from '@/components/dashboard'
import { Sidebar } from '@/components/sidebar'
import { Header } from '@/components/header'
import { useState } from 'react'

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [activeTab, setActiveTab] = useState('automation')


  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar 
        isOpen={sidebarOpen} 
        onClose={() => setSidebarOpen(false)}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header 
          onMenuClick={() => setSidebarOpen(true)}
          activeTab={activeTab}
        />
        
        <main className="flex-1 overflow-x-hidden overflow-y-auto">
          <Dashboard activeTab={activeTab} />
        </main>
      </div>
    </div>
  )
}





