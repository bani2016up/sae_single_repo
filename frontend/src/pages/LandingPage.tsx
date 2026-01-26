import { Link } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card, CardContent } from '../components/ui/card'
import { FileText, BarChart3, Shield, Zap } from 'lucide-react'

export function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold mb-6">
          Document Analysis Made Simple
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Upload, analyze, and validate your documents with AI-powered insights.
          Get instant feedback on your text quality and accuracy.
        </p>
        <div className="flex gap-4 justify-center">
          <Link to="/register">
            <Button size="lg">Get Started</Button>
          </Link>
          <Link to="/login">
            <Button size="lg" variant="outline">
              Sign In
            </Button>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardContent className="pt-6">
              <FileText className="h-12 w-12 mb-4 text-primary" />
              <h3 className="font-semibold mb-2">Document Management</h3>
              <p className="text-sm text-muted-foreground">
                Create, edit, and organize your documents in one place
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <BarChart3 className="h-12 w-12 mb-4 text-primary" />
              <h3 className="font-semibold mb-2">AI Analysis</h3>
              <p className="text-sm text-muted-foreground">
                Get intelligent insights and suggestions for your text
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <Shield className="h-12 w-12 mb-4 text-primary" />
              <h3 className="font-semibold mb-2">Fact Checking</h3>
              <p className="text-sm text-muted-foreground">
                Verify accuracy and identify potential issues
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <Zap className="h-12 w-12 mb-4 text-primary" />
              <h3 className="font-semibold mb-2">Fast & Secure</h3>
              <p className="text-sm text-muted-foreground">
                Quick processing with enterprise-grade security
              </p>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  )
}
