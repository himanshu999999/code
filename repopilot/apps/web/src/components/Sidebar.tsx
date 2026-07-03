'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { 
  LayoutDashboard, 
  FolderPlus, 
  SearchCode, 
  Bug, 
  History, 
  BarChart3,
  GitBranch
} from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Ingest Repo', href: '/repo-ingestion', icon: FolderPlus },
  { name: 'Code Search', href: '/code-search', icon: SearchCode },
  { name: 'Bug Fix', href: '/issue-repair', icon: Bug },
  { name: 'Run History', href: '/run-history', icon: History },
  { name: 'Evaluations', href: '/evaluations', icon: BarChart3 },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="flex h-full w-64 flex-col bg-card border-r">
      <div className="flex h-16 items-center border-b px-6">
        <GitBranch className="h-6 w-6 text-primary mr-2" />
        <span className="text-lg font-semibold">RepoPilot</span>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                'flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              )}
            >
              <item.icon className="mr-3 h-5 w-5" />
              {item.name}
            </Link>
          )
        })}
      </nav>
      <div className="border-t p-4">
        <div className="text-xs text-muted-foreground">
          <p>v1.0.0</p>
          <p className="mt-1">AI Codebase Intelligence</p>
        </div>
      </div>
    </div>
  )
}
