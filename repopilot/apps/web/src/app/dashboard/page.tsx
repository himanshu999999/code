'use client'

import { useEffect, useState } from 'react'
import { repositories, tasks, type Repository, type Task } from '@/lib/api'
import { FolderOpen, FileCode, CheckCircle, Clock, AlertCircle, GitBranch } from 'lucide-react'

export default function DashboardPage() {
  const [repos, setRepos] = useState<Repository[]>([])
  const [recentTasks, setRecentTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      repositories.list().then(r => setRepos(r.data)),
      tasks.list().then(r => setRecentTasks(r.data.slice(0, 5).reverse())),
    ]).finally(() => setLoading(false))
  }, [])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ready':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'pending':
      case 'cloning':
      case 'parsing':
      case 'indexing':
        return <Clock className="h-5 w-5 text-yellow-500" />
      case 'failed':
        return <AlertCircle className="h-5 w-5 text-red-500" />
      default:
        return <FolderOpen className="h-5 w-5 text-gray-500" />
    }
  }

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-muted-foreground">
          Monitor your codebase intelligence and bug-fix operations
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-6 md:grid-cols-4 mb-8">
        <div className="rounded-lg border bg-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Indexed Repos</p>
              <p className="text-3xl font-bold">{repos.length}</p>
            </div>
            <GitBranch className="h-8 w-8 text-primary" />
          </div>
        </div>
        <div className="rounded-lg border bg-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total Files</p>
              <p className="text-3xl font-bold">
                {repos.reduce((sum, r) => sum + r.total_files, 0)}
              </p>
            </div>
            <FolderOpen className="h-8 w-8 text-primary" />
          </div>
        </div>
        <div className="rounded-lg border bg-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Code Chunks</p>
              <p className="text-3xl font-bold">
                {repos.reduce((sum, r) => sum + r.total_chunks, 0)}
              </p>
            </div>
            <FileCode className="h-8 w-8 text-primary" />
          </div>
        </div>
        <div className="rounded-lg border bg-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Tasks Run</p>
              <p className="text-3xl font-bold">{recentTasks.length}</p>
            </div>
            <Clock className="h-8 w-8 text-primary" />
          </div>
        </div>
      </div>

      {/* Repositories Table */}
      <div className="rounded-lg border bg-card mb-8">
        <div className="border-b p-6">
          <h2 className="text-xl font-semibold">Repositories</h2>
        </div>
        <div className="p-6">
          {repos.length === 0 ? (
            <p className="text-muted-foreground text-center py-8">
              No repositories indexed yet. Go to &quot;Ingest Repo&quot; to add one.
            </p>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="border-b text-left text-sm text-muted-foreground">
                  <th className="pb-3">Name</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Language</th>
                  <th className="pb-3">Files</th>
                  <th className="pb-3">Chunks</th>
                </tr>
              </thead>
              <tbody>
                {repos.map((repo) => (
                  <tr key={repo.id} className="border-b last:border-0">
                    <td className="py-3">
                      <div className="font-medium">{repo.name}</div>
                      <div className="text-xs text-muted-foreground truncate max-w-xs">
                        {repo.url}
                      </div>
                    </td>
                    <td className="py-3">
                      <div className="flex items-center gap-2">
                        {getStatusIcon(repo.status)}
                        <span className="capitalize">{repo.status}</span>
                      </div>
                    </td>
                    <td className="py-3 capitalize">{repo.language || 'Unknown'}</td>
                    <td className="py-3">{repo.total_files}</td>
                    <td className="py-3">{repo.total_chunks}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Recent Tasks */}
      <div className="rounded-lg border bg-card">
        <div className="border-b p-6">
          <h2 className="text-xl font-semibold">Recent Tasks</h2>
        </div>
        <div className="p-6">
          {recentTasks.length === 0 ? (
            <p className="text-muted-foreground text-center py-8">
              No tasks have been run yet.
            </p>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="border-b text-left text-sm text-muted-foreground">
                  <th className="pb-3">Type</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Query</th>
                  <th className="pb-3">Confidence</th>
                  <th className="pb-3">Latency</th>
                </tr>
              </thead>
              <tbody>
                {recentTasks.map((task) => (
                  <tr key={task.id} className="border-b last:border-0">
                    <td className="py-3">
                      <span className="capitalize px-2 py-1 rounded bg-accent text-xs">
                        {task.type.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="py-3">
                      <span className={`capitalize ${
                        task.status === 'completed' ? 'text-green-600' :
                        task.status === 'failed' ? 'text-red-600' :
                        'text-yellow-600'
                      }`}>
                        {task.status}
                      </span>
                    </td>
                    <td className="py-3 max-w-md truncate">
                      {task.query || 'Bug fix task'}
                    </td>
                    <td className="py-3">
                      {task.confidence_score 
                        ? `${Math.round(task.confidence_score * 100)}%`
                        : '-'
                      }
                    </td>
                    <td className="py-3">
                      {task.latency_ms 
                        ? `${Math.round(task.latency_ms / 1000)}s`
                        : '-'
                      }
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
