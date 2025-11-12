'use client'

import { cn } from '@/lib/utils'
import { 
  X,
  Moon,
  Sun,
  Zap
} from 'lucide-react'
import { useTheme } from 'next-themes'
import { Button } from '@/components/ui/button'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
  activeTab: string
  onTabChange: (tab: string) => void
}

const navigation = [
  { name: 'Automation', href: 'automation', icon: Zap },
]

export function Sidebar({ isOpen, onClose, activeTab, onTabChange }: SidebarProps) {
  const { theme, setTheme } = useTheme()

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-light-gray dark:border-medium-gray">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-teal rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">TG</span>
              </div>
              <div>
                <h1 className="text-lg font-bold text-dark-gray dark:text-white">TimeGuard AI</h1>
                <p className="text-xs text-medium-gray dark:text-light-gray">Enterprise Dashboard</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden"
              onClick={onClose}
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon
              const isActive = activeTab === item.href
              
              return (
                <button
                  key={item.name}
                  onClick={() => {
                    onTabChange(item.href)
                    onClose()
                  }}
                  className={cn(
                    "w-full flex items-center px-3 py-2 text-sm font-bold rounded-lg transition-colors duration-200",
                    isActive
                      ? "navbar-cta-gradient text-white"
                      : "text-dark-gray hover:bg-light-gray dark:text-white dark:hover:bg-medium-gray"
                  )}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.name}
                </button>
              )
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-light-gray dark:border-medium-gray">
            <div className="flex items-center justify-between">
              <div className="text-sm text-medium-gray dark:text-light-gray">
                Version 1.0.0
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                className="p-2"
              >
                {theme === 'dark' ? (
                  <Sun className="h-4 w-4" />
                ) : (
                  <Moon className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}





