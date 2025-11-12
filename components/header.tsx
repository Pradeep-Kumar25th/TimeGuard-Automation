'use client'

import { Menu } from 'lucide-react'
import { Button } from '@/components/ui/button'
import Image from 'next/image'

interface HeaderProps {
  onMenuClick: () => void
  activeTab: string
}

export function Header({ onMenuClick, activeTab }: HeaderProps) {
  const getPageTitle = (tab: string) => {
    if (tab === 'automation') {
      return 'Automation'
    }
    return 'TimeGuard AI'
  }

  return (
    <header className="bg-white dark:bg-dark-gray border-b border-light-gray dark:border-medium-gray px-4 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={onMenuClick}
            className="lg:hidden"
          >
            <Menu className="h-5 w-5" />
          </Button>
          
          <div className="hidden lg:block">
            <h1 className="text-xl font-bold text-dark-gray dark:text-white">
              {getPageTitle(activeTab)}
            </h1>
          </div>

          {/* Logo - Scaled */}
          <div className="hidden lg:block">
            <Image
              src="/logo.png"
              alt="Logo"
              width={160}
              height={53}
              className="object-contain"
            />
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Header actions can be added here if needed */}
        </div>
      </div>
    </header>
  )
}


