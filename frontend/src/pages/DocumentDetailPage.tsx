import { useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { documentsApi } from '../api/documents'
import { validationApi } from '../api/validation'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Textarea } from '../components/ui/textarea'
import { Label } from '../components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Edit2, Save, X, Trash2, PlayCircle } from 'lucide-react'
import { LoadingSpinner } from '../components/common/Loading'
import { toast } from 'sonner'

export function DocumentDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState('')
  const [editContent, setEditContent] = useState('')

  const { data: document, isLoading } = useQuery({
    queryKey: ['document', id],
    queryFn: () => documentsApi.getById(Number(id)),
    enabled: !!id,
  })

  const updateMutation = useMutation({
    mutationFn: (data: { title: string; content: string }) =>
      documentsApi.update(Number(id), data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['document', id] })
      queryClient.invalidateQueries({ queryKey: ['documents'] })
      setIsEditing(false)
      toast.success('Document updated successfully')
    },
    onError: () => {
      toast.error('Failed to update document')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: () => documentsApi.delete(Number(id)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] })
      toast.success('Document deleted successfully')
      navigate('/documents')
    },
    onError: () => {
      toast.error('Failed to delete document')
    },
  })

  const createValidationMutation = useMutation({
    mutationFn: (documentId: number) =>
      validationApi.create({ document_id: documentId }),
    onSuccess: async (data) => {
      // Start the validation immediately
      try {
        await validationApi.start(data.id)
        toast.success('Analysis started successfully')
        navigate(`/analysis/${data.id}`)
      } catch {
        toast.error('Failed to start analysis')
      }
    },
    onError: () => {
      toast.error('Failed to create validation')
    },
  })

  const handleEdit = () => {
    if (document) {
      setEditTitle(document.title)
      setEditContent(document.content)
      setIsEditing(true)
    }
  }

  const handleSave = () => {
    if (!editTitle.trim()) {
      toast.error('Title cannot be empty')
      return
    }
    updateMutation.mutate({ title: editTitle, content: editContent })
  }

  const handleCancel = () => {
    setIsEditing(false)
    setEditTitle('')
    setEditContent('')
  }

  const handleDelete = () => {
    if (
      window.confirm(
        `Are you sure you want to delete "${document?.title}"? This action cannot be undone.`
      )
    ) {
      deleteMutation.mutate()
    }
  }

  const handleStartAnalysis = () => {
    if (id) {
      createValidationMutation.mutate(Number(id))
    }
  }

  if (isLoading) {
    return (
      <div className="container mx-auto p-6">
        <LoadingSpinner />
      </div>
    )
  }

  if (!document) {
    return (
      <div className="container mx-auto p-6">
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-muted-foreground mb-4">Document not found</p>
            <Link to="/documents">
              <Button>Back to Documents</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 max-w-4xl space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Link to="/documents">
            <Button variant="ghost">← Back</Button>
          </Link>
        </div>
        <div className="flex gap-2">
          {!isEditing && (
            <>
              <Button onClick={handleStartAnalysis} variant="default">
                <PlayCircle className="h-4 w-4 mr-2" />
                Start Analysis
              </Button>
              <Button onClick={handleEdit} variant="outline">
                <Edit2 className="h-4 w-4 mr-2" />
                Edit
              </Button>
              <Button
                onClick={handleDelete}
                variant="destructive"
                disabled={deleteMutation.isPending}
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete
              </Button>
            </>
          )}
        </div>
      </div>

      <Card>
        <CardHeader>
          {isEditing ? (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="edit-title">Title</Label>
                <Input
                  id="edit-title"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                />
              </div>
              <div className="flex gap-2">
                <Button onClick={handleSave} disabled={updateMutation.isPending}>
                  <Save className="h-4 w-4 mr-2" />
                  Save
                </Button>
                <Button onClick={handleCancel} variant="outline">
                  <X className="h-4 w-4 mr-2" />
                  Cancel
                </Button>
              </div>
            </div>
          ) : (
            <CardTitle>{document.title}</CardTitle>
          )}
          <p className="text-sm text-muted-foreground">
            Created {new Date(document.was_created).toLocaleString()}
          </p>
        </CardHeader>
        <CardContent>
          {isEditing ? (
            <div className="space-y-2">
              <Label htmlFor="edit-content">Content</Label>
              <Textarea
                id="edit-content"
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                rows={15}
              />
            </div>
          ) : (
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap font-sans text-foreground">
                {document.content}
              </pre>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
