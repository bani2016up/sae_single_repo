import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { validationApi } from '../api/validation'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Badge } from '../components/ui/badge'
import { CheckCircle2, XCircle, Clock, AlertTriangle } from 'lucide-react'
import { LoadingSpinner } from '../components/common/Loading'
import { useState } from 'react'

export function AnalysisDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [selectedError, setSelectedError] = useState<number | null>(null)

  const { data: validation, isLoading: validationLoading } = useQuery({
    queryKey: ['validation', id],
    queryFn: () => validationApi.getById(Number(id)),
    enabled: !!id,
    refetchInterval: (query) => {
      const data = query.state.data
      return data && !data.validated ? 5000 : false
    },
  })

  const { data: errors } = useQuery({
    queryKey: ['validation-errors', id],
    queryFn: () => validationApi.getErrors(Number(id)),
    enabled: !!id && validation?.validated === true,
  })

  if (validationLoading) {
    return (
      <div className="container mx-auto p-6">
        <LoadingSpinner />
      </div>
    )
  }

  if (!validation) {
    return (
      <div className="container mx-auto p-6">
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-muted-foreground mb-4">Validation not found</p>
            <Link to="/analysis">
              <Button>Back to Analysis</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    )
  }

  const getStatusBadge = () => {
    if (!validation.validated) {
      return (
        <Badge variant="secondary">
          <Clock className="h-3 w-3 mr-1" />
          Processing...
        </Badge>
      )
    }
    if (validation.is_valid) {
      return (
        <Badge variant="default" className="bg-green-500">
          <CheckCircle2 className="h-3 w-3 mr-1" />
          Valid
        </Badge>
      )
    }
    return (
      <Badge variant="destructive">
        <XCircle className="h-3 w-3 mr-1" />
        Issues Found
      </Badge>
    )
  }

  return (
    <div className="container mx-auto p-6 max-w-6xl space-y-6">
      <div className="flex items-center gap-2">
        <Link to="/analysis">
          <Button variant="ghost">← Back</Button>
        </Link>
        <h1 className="text-3xl font-bold">Analysis Results</h1>
      </div>

      <div className="flex gap-2">
        {getStatusBadge()}
      </div>

      {!validation.validated && (
        <Card className="border-blue-500 bg-blue-50 dark:bg-blue-950">
          <CardContent className="py-4">
            <div className="flex items-center gap-3">
              <Clock className="h-5 w-5 text-blue-600 dark:text-blue-400 animate-spin" />
              <div>
                <p className="font-medium text-blue-900 dark:text-blue-100">
                  Analysis in Progress
                </p>
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  Your document is being analyzed. This page will update automatically.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {validation.validated && errors && (
        <>
          <Card>
            <CardHeader>
              <CardTitle>Summary</CardTitle>
              <CardDescription>
                {errors.errors.filter((e) => e.error !== null).length} issue(s) found
              </CardDescription>
            </CardHeader>
          </Card>

          {errors.errors.filter((e) => e.error !== null).length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Issues Detected</CardTitle>
                <CardDescription>
                  Click on an issue to view details
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {errors.errors
                  .filter((e) => e.error !== null)
                  .map((errorItem) => (
                    <div
                      key={errorItem.id}
                      className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                        selectedError === errorItem.id
                          ? 'border-red-500 bg-red-50 dark:bg-red-950'
                          : 'hover:bg-accent'
                      }`}
                      onClick={() => setSelectedError(errorItem.id)}
                    >
                      <div className="flex items-start gap-3">
                        <AlertTriangle className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
                        <div className="flex-1 space-y-2">
                          <div className="flex items-center justify-between">
                            <p className="font-medium">
                              "{errorItem.error!.wrong_fragment}"
                            </p>
                            <Badge variant={errorItem.is_resolved ? 'default' : 'secondary'}>
                              {errorItem.is_resolved ? 'Resolved' : 'Unresolved'}
                            </Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">
                            <strong>Suggestion:</strong> {errorItem.error!.suggestion}
                          </p>
                          <p className="text-sm text-muted-foreground">
                            <strong>Explanation:</strong> {errorItem.error!.explanation}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            Position: {errorItem.error!.loc_index_ch_start} - {errorItem.error!.loc_index_ch_end}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
              </CardContent>
            </Card>
          )}

          {errors.errors.filter((e) => e.error !== null).length === 0 && (
            <Card className="border-green-500 bg-green-50 dark:bg-green-950">
              <CardContent className="py-8 text-center">
                <CheckCircle2 className="h-12 w-12 text-green-600 dark:text-green-400 mx-auto mb-4" />
                <p className="font-medium text-green-900 dark:text-green-100 mb-2">
                  No Issues Found
                </p>
                <p className="text-sm text-green-700 dark:text-green-300">
                  Your document passed all validation checks!
                </p>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  )
}
