import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { documentsApi } from '../api/documents'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Textarea } from '../components/ui/textarea'
import { Label } from '../components/ui/label'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Upload, FileText } from 'lucide-react'
import { toast } from 'sonner'

export function CreateDocumentPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [file, setFile] = useState<File | null>(null)

  const createMutation = useMutation({
    mutationFn: documentsApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['documents'] })
      toast.success('Document created successfully')
      navigate(`/documents/${data.id}`)
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create document')
    },
  })

  const uploadMutation = useMutation({
    mutationFn: documentsApi.createFromFile,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['documents'] })
      toast.success('Document uploaded successfully')
      navigate(`/documents/${data.id}`)
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to upload document')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) {
      toast.error('Please enter a title')
      return
    }
    createMutation.mutate({ title, content })
  }

  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      toast.error('Please select a file')
      return
    }

    const allowedTypes = ['.txt', '.rtf']
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
    
    if (!allowedTypes.includes(fileExtension)) {
      toast.error('Only .txt and .rtf files are allowed')
      return
    }

    uploadMutation.mutate(file)
  }

  return (
    <div className="container mx-auto p-6 max-w-4xl space-y-6">
      <div className="flex items-center gap-2">
        <Button variant="ghost" onClick={() => navigate('/documents')}>
          ← Back
        </Button>
        <h1 className="text-3xl font-bold">Create Document</h1>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Manual Entry */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              <CardTitle>Manual Entry</CardTitle>
            </div>
            <CardDescription>Create a document by typing or pasting text</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="title">Title</Label>
                <Input
                  id="title"
                  placeholder="Document title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="content">Content</Label>
                <Textarea
                  id="content"
                  placeholder="Enter your document content here..."
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  rows={10}
                />
              </div>
              <Button
                type="submit"
                className="w-full"
                disabled={createMutation.isPending}
              >
                {createMutation.isPending ? 'Creating...' : 'Create Document'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* File Upload */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              <CardTitle>Upload File</CardTitle>
            </div>
            <CardDescription>Upload a .txt or .rtf file</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleFileUpload} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="file">Select File</Label>
                <Input
                  id="file"
                  type="file"
                  accept=".txt,.rtf"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  required
                />
                {file && (
                  <p className="text-sm text-muted-foreground">
                    Selected: {file.name}
                  </p>
                )}
              </div>
              <div className="border-2 border-dashed border-muted rounded-lg p-8 text-center">
                <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-sm text-muted-foreground">
                  Supported formats: .txt, .rtf
                </p>
              </div>
              <Button
                type="submit"
                className="w-full"
                disabled={uploadMutation.isPending}
              >
                {uploadMutation.isPending ? 'Uploading...' : 'Upload Document'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
