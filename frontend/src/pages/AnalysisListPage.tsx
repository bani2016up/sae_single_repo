import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { AlertTriangle } from 'lucide-react'

export function AnalysisListPage() {
  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold">Analysis Dashboard</h1>

      <Card>
        <CardHeader>
          <CardTitle>Recent Analyses</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12 text-muted-foreground">
            <AlertTriangle className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
            <p className="mb-2">No analyses yet</p>
            <p className="text-sm">
              Start analyzing a document from the Documents page
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
