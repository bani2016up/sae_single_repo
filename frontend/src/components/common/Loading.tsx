export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>
  )
}

export function PageLoader() {
  return (
    <div className="flex h-screen items-center justify-center">
      <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary"></div>
    </div>
  )
}

export function CardSkeleton() {
  return (
    <div className="rounded-lg border bg-card p-6 animate-pulse">
      <div className="h-4 bg-muted rounded w-3/4 mb-4"></div>
      <div className="h-4 bg-muted rounded w-1/2"></div>
    </div>
  )
}
