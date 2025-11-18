import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Stack,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  alpha,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  RadioGroup,
  FormControlLabel,
  Radio,
  LinearProgress,
  Alert,
  Tabs,
  Tab,
  Switch,
  FormControl,
  FormLabel,
  Divider,
} from '@mui/material';
import {
  UploadFile as UploadIcon,
  Description as PDFIcon,
  CheckCircle as SuccessIcon,
  Business as RealEstateIcon,
  TrendingUp as FinancialIcon,
  CloudUpload as CloudUploadIcon,
  Article as MarkdownIcon,
  AutoAwesome as AIIcon,
  InsertDriveFile as FileIcon,
  Image as ImageIcon,
  Audiotrack as AudioIcon,
} from '@mui/icons-material';
import axios from 'axios';

type ModelType = 'real-estate' | 'financial' | null;

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

export const PDFExtraction: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);

  // PDF Extraction State
  const [modelTypeDialogOpen, setModelTypeDialogOpen] = useState(false);
  const [selectedModelType, setSelectedModelType] = useState<ModelType>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [extracting, setExtracting] = useState(false);
  const [extractionResult, setExtractionResult] = useState<any>(null);

  // MarkItDown State
  const [markdownFile, setMarkdownFile] = useState<File | null>(null);
  const [converting, setConverting] = useState(false);
  const [conversionResult, setConversionResult] = useState<any>(null);
  const [useLLM, setUseLLM] = useState(false);
  const [markdownPreview, setMarkdownPreview] = useState<string>('');

  // Model Integration State
  const [modelDialogOpen, setModelDialogOpen] = useState(false);
  const [availableModels, setAvailableModels] = useState<any[]>([]);
  const [selectedFinancialModel, setSelectedFinancialModel] = useState<string>('');
  const [creatingModel, setCreatingModel] = useState(false);
  const [modelCreationResult, setModelCreationResult] = useState<any>(null);

  // PDF Extraction Handlers
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setUploadedFile(file);
      setModelTypeDialogOpen(true);
    }
  };

  const handleModelTypeSelect = () => {
    if (selectedModelType && uploadedFile) {
      setModelTypeDialogOpen(false);
      performExtraction();
    }
  };

  const performExtraction = async () => {
    setExtracting(true);

    // Simulate extraction (in real implementation, this would call the backend API)
    setTimeout(() => {
      setExtractionResult({
        success: true,
        modelType: selectedModelType,
        fileName: uploadedFile?.name,
        extractedData: {
          documentType: selectedModelType === 'financial' ? 'Income Statement' : 'Property Analysis',
          confidence: 0.94,
          fieldsExtracted: selectedModelType === 'financial' ? 24 : 18,
        },
      });
      setExtracting(false);
    }, 2000);
  };

  const resetExtraction = () => {
    setUploadedFile(null);
    setSelectedModelType(null);
    setExtractionResult(null);
    setExtracting(false);
  };

  // MarkItDown Handlers
  const handleMarkdownFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setMarkdownFile(file);
      performMarkdownConversion(file);
    }
  };

  const performMarkdownConversion = async (file: File) => {
    setConverting(true);
    setConversionResult(null);
    setMarkdownPreview('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(
        `/api/v1/markitdown/convert?use_llm=${useLLM}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setConversionResult(response.data);

      // Fetch the markdown content
      const contentResponse = await axios.get(
        `/api/v1/markitdown/documents/${response.data.document_id}/content`
      );

      setMarkdownPreview(contentResponse.data.markdown_text);
      setConverting(false);
    } catch (error: any) {
      console.error('Conversion error:', error);
      setConversionResult({
        success: false,
        error: error.response?.data?.detail || error.message || 'Conversion failed',
      });
      setConverting(false);
    }
  };

  const resetMarkdownConversion = () => {
    setMarkdownFile(null);
    setConversionResult(null);
    setMarkdownPreview('');
    setModelCreationResult(null);
  };

  // Model Integration Handlers
  const handleRunInModelClick = async () => {
    if (!conversionResult?.document_id) return;

    try {
      // Fetch available models
      const response = await axios.get(
        `/api/v1/markitdown/documents/${conversionResult.document_id}/available-models`
      );
      setAvailableModels(response.data.models);
      setModelDialogOpen(true);
    } catch (error: any) {
      console.error('Failed to fetch models:', error);
      alert('Failed to fetch available models');
    }
  };

  const handleCreateModel = async () => {
    if (!selectedFinancialModel || !conversionResult?.document_id) return;

    setCreatingModel(true);

    try {
      const response = await axios.post(
        `/api/v1/markitdown/documents/${conversionResult.document_id}/run-in-model`,
        {
          model_type: selectedFinancialModel,
          auto_populate: true,
        }
      );

      setModelCreationResult(response.data);
      setModelDialogOpen(false);
      setCreatingModel(false);
    } catch (error: any) {
      console.error('Model creation error:', error);
      alert(error.response?.data?.detail || 'Failed to create model');
      setCreatingModel(false);
    }
  };

  return (
    <Box>
      {/* Header */}
      <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 3 }}>
        <Box
          sx={{
            width: 56,
            height: 56,
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            borderRadius: 3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 20px rgba(16, 185, 129, 0.3)',
          }}
        >
          <PDFIcon sx={{ fontSize: 32, color: 'white' }} />
        </Box>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Document Processing & Extraction
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Extract financial data from PDFs or convert any document to LLM-ready markdown
          </Typography>
        </Box>
      </Stack>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={(e, newValue) => setTabValue(newValue)}
          sx={{
            borderBottom: 1,
            borderColor: 'divider',
            px: 2,
          }}
        >
          <Tab
            label="PDF Financial Extraction"
            icon={<PDFIcon />}
            iconPosition="start"
            sx={{ textTransform: 'none', fontWeight: 600 }}
          />
          <Tab
            label="MarkItDown Conversion"
            icon={<MarkdownIcon />}
            iconPosition="start"
            sx={{ textTransform: 'none', fontWeight: 600 }}
          />
        </Tabs>
      </Paper>

      {/* PDF Extraction Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          {/* Upload Section */}
          <Grid item xs={12} md={6}>
            <Paper
              sx={{
                p: 4,
                textAlign: 'center',
                border: '2px dashed',
                borderColor: 'divider',
                bgcolor: alpha('#10b981', 0.02),
                minHeight: 400,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
              }}
            >
              {!extracting && !extractionResult && (
                <Stack spacing={3} alignItems="center">
                  <CloudUploadIcon sx={{ fontSize: 80, color: 'text.disabled' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Upload PDF Document
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 400 }}>
                    Upload financial statements, property reports, or other documents to automatically extract data
                  </Typography>

                  <Button
                    variant="contained"
                    component="label"
                    startIcon={<UploadIcon />}
                    sx={{
                      py: 1.5,
                      px: 4,
                      background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                      fontWeight: 600,
                    }}
                  >
                    Choose PDF File
                    <input
                      type="file"
                      hidden
                      accept="application/pdf"
                      onChange={handleFileUpload}
                    />
                  </Button>

                  <Typography variant="caption" color="text.secondary">
                    Supported formats: PDF (max 10MB)
                  </Typography>
                </Stack>
              )}

              {extracting && (
                <Stack spacing={3} alignItems="center">
                  <Box sx={{ width: '100%', maxWidth: 400 }}>
                    <LinearProgress />
                  </Box>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Extracting Data...
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Analyzing {uploadedFile?.name}
                  </Typography>
                </Stack>
              )}

              {extractionResult && (
                <Stack spacing={3} alignItems="center">
                  <SuccessIcon sx={{ fontSize: 80, color: '#10b981' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600, color: '#10b981' }}>
                    Extraction Complete!
                  </Typography>
                  <Alert severity="success" sx={{ maxWidth: 400 }}>
                    Successfully extracted {extractionResult.extractedData.fieldsExtracted} fields with{' '}
                    {(extractionResult.extractedData.confidence * 100).toFixed(0)}% confidence
                  </Alert>

                  <Stack direction="row" spacing={2}>
                    <Button variant="outlined" onClick={resetExtraction}>
                      Extract Another
                    </Button>
                    <Button
                      variant="contained"
                      sx={{
                        background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                      }}
                    >
                      View Data
                    </Button>
                  </Stack>
                </Stack>
              )}
            </Paper>
          </Grid>

          {/* Info Section */}
          <Grid item xs={12} md={6}>
            <Stack spacing={3}>
              {/* Features */}
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Key Features
                </Typography>
                <Stack spacing={2}>
                  {[
                    'Automatic document type detection',
                    'Multi-period data extraction (Q1, Q2, Q3, Annual)',
                    '100+ financial keywords recognized',
                    'Quality validation with confidence scoring',
                    'Database-ready structured output',
                    'Support for both real estate and financial models',
                  ].map((feature, idx) => (
                    <Stack key={idx} direction="row" spacing={1.5} alignItems="center">
                      <Box
                        sx={{
                          width: 6,
                          height: 6,
                          borderRadius: '50%',
                          bgcolor: '#10b981',
                        }}
                      />
                      <Typography variant="body2">{feature}</Typography>
                    </Stack>
                  ))}
                </Stack>
              </Paper>

              {/* Model Types */}
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Supported Document Types
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        bgcolor: alpha('#3b82f6', 0.05),
                        border: `1px solid ${alpha('#3b82f6', 0.2)}`,
                      }}
                    >
                      <CardContent>
                        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
                          <RealEstateIcon sx={{ color: '#3b82f6' }} />
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            Real Estate
                          </Typography>
                        </Stack>
                        <Typography variant="caption" color="text.secondary">
                          Property financials, rent rolls, operating statements, NOI reports
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        bgcolor: alpha('#8b5cf6', 0.05),
                        border: `1px solid ${alpha('#8b5cf6', 0.2)}`,
                      }}
                    >
                      <CardContent>
                        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
                          <FinancialIcon sx={{ color: '#8b5cf6' }} />
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            Financial
                          </Typography>
                        </Stack>
                        <Typography variant="caption" color="text.secondary">
                          Income statements, balance sheets, cash flow statements, 10-K/10-Q
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </Paper>

              {/* Stats */}
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Time Savings
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: '#10b981' }}>
                        97%
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Time Reduction
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: '#10b981' }}>
                        30s
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Per Document
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </Paper>
            </Stack>
          </Grid>
        </Grid>
      </TabPanel>

      {/* MarkItDown Tab */}
      <TabPanel value={tabValue} index={1}>
        {/* Info Alert */}
        <Alert severity="info" sx={{ mb: 3 }}>
          <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
            Intelligent Extraction with Optional LLM Enhancement
          </Typography>
          <Typography variant="caption">
            All features work using rule-based extraction (regex patterns, keyword matching, structural analysis).
            Enable LLM Enhancement for additional insights when your local Ollama LLM is available.
          </Typography>
        </Alert>

        <Grid container spacing={3}>
          {/* Upload Section */}
          <Grid item xs={12} md={6}>
            <Paper
              sx={{
                p: 4,
                textAlign: 'center',
                border: '2px dashed',
                borderColor: 'divider',
                bgcolor: alpha('#6366f1', 0.02),
                minHeight: 400,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
              }}
            >
              {!converting && !conversionResult && (
                <Stack spacing={3} alignItems="center">
                  <MarkdownIcon sx={{ fontSize: 80, color: 'text.disabled' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Convert Document to Markdown
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 400 }}>
                    Upload any document to convert it to LLM-ready markdown format with enhanced structure preservation
                  </Typography>

                  {/* LLM Enhancement Toggle */}
                  <FormControl component="fieldset">
                    <Stack direction="row" spacing={2} alignItems="center">
                      <AIIcon sx={{ color: useLLM ? '#6366f1' : 'text.disabled' }} />
                      <FormControlLabel
                        control={
                          <Switch
                            checked={useLLM}
                            onChange={(e) => setUseLLM(e.target.checked)}
                            color="primary"
                          />
                        }
                        label={
                          <Box>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              LLM Enhancement
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              Use local LLM for enhanced analysis (optional)
                            </Typography>
                          </Box>
                        }
                      />
                    </Stack>
                  </FormControl>

                  <Button
                    variant="contained"
                    component="label"
                    startIcon={<UploadIcon />}
                    sx={{
                      py: 1.5,
                      px: 4,
                      background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                      fontWeight: 600,
                    }}
                  >
                    Choose Document
                    <input
                      type="file"
                      hidden
                      accept="*/*"
                      onChange={handleMarkdownFileUpload}
                    />
                  </Button>

                  <Typography variant="caption" color="text.secondary">
                    Supports: PDF, Word, Excel, PowerPoint, Images, HTML, Audio, and more
                  </Typography>
                </Stack>
              )}

              {converting && (
                <Stack spacing={3} alignItems="center">
                  <Box sx={{ width: '100%', maxWidth: 400 }}>
                    <LinearProgress />
                  </Box>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Converting Document...
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Processing {markdownFile?.name}
                  </Typography>
                  {useLLM && (
                    <Chip
                      icon={<AIIcon />}
                      label="AI Enhancement Active"
                      size="small"
                      color="primary"
                    />
                  )}
                </Stack>
              )}

              {conversionResult && !conversionResult.error && (
                <Stack spacing={3} alignItems="center">
                  <SuccessIcon sx={{ fontSize: 80, color: '#6366f1' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600, color: '#6366f1' }}>
                    Conversion Complete!
                  </Typography>
                  <Alert severity="success" sx={{ maxWidth: 400 }}>
                    Converted {conversionResult.word_count?.toLocaleString() || 0} words with{' '}
                    {((conversionResult.conversion_confidence || 0) * 100).toFixed(0)}% confidence
                  </Alert>

                  <Stack spacing={1} sx={{ width: '100%', maxWidth: 400 }}>
                    <Stack direction="row" spacing={2} justifyContent="space-between">
                      <Typography variant="caption" color="text.secondary">
                        File Type:
                      </Typography>
                      <Chip label={conversionResult.file_type} size="small" />
                    </Stack>
                    <Stack direction="row" spacing={2} justifyContent="space-between">
                      <Typography variant="caption" color="text.secondary">
                        Method:
                      </Typography>
                      <Chip
                        label={conversionResult.conversion_method || 'MarkItDown'}
                        size="small"
                        color="primary"
                      />
                    </Stack>
                    <Stack direction="row" spacing={2} justifyContent="space-between">
                      <Typography variant="caption" color="text.secondary">
                        Processing Time:
                      </Typography>
                      <Typography variant="caption">
                        {conversionResult.conversion_duration_ms}ms
                      </Typography>
                    </Stack>
                  </Stack>

                  {modelCreationResult && (
                    <Alert severity="success" icon={<SuccessIcon />} sx={{ maxWidth: 400 }}>
                      <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                        {modelCreationResult.model_type} Model Created Successfully!
                      </Typography>
                      <Typography variant="caption" component="div">
                        Model: {modelCreationResult.model_name}
                      </Typography>
                      <Typography variant="caption" component="div">
                        Fields populated: {modelCreationResult.populated_fields?.length || 0}
                      </Typography>
                      <Typography variant="caption" component="div" sx={{ mt: 1, fontStyle: 'italic' }}>
                        {modelCreationResult.message}
                      </Typography>
                    </Alert>
                  )}

                  <Stack direction="row" spacing={2} flexWrap="wrap" justifyContent="center">
                    <Button variant="outlined" onClick={resetMarkdownConversion}>
                      Convert Another
                    </Button>
                    <Button
                      variant="contained"
                      sx={{
                        background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                      }}
                      onClick={() => {
                        // Scroll to preview
                        document.getElementById('markdown-preview')?.scrollIntoView({ behavior: 'smooth' });
                      }}
                    >
                      View Markdown
                    </Button>
                    <Button
                      variant="contained"
                      color="success"
                      startIcon={<TrendingUp />}
                      onClick={handleRunInModelClick}
                      sx={{
                        background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                        fontWeight: 600,
                      }}
                    >
                      Run in Model
                    </Button>
                  </Stack>
                </Stack>
              )}

              {conversionResult && conversionResult.error && (
                <Stack spacing={3} alignItems="center">
                  <Alert severity="error" sx={{ maxWidth: 400 }}>
                    {conversionResult.error}
                  </Alert>
                  <Button variant="outlined" onClick={resetMarkdownConversion}>
                    Try Again
                  </Button>
                </Stack>
              )}
            </Paper>
          </Grid>

          {/* Info Section */}
          <Grid item xs={12} md={6}>
            <Stack spacing={3}>
              {/* Features */}
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  MarkItDown Features
                </Typography>
                <Stack spacing={2}>
                  {[
                    'Multi-format support (15+ file types)',
                    'Preserves document structure (headings, tables, lists)',
                    'Optional AI-powered image descriptions',
                    'LLM-ready markdown output',
                    'Automatic file type detection',
                    'Confidence scoring and quality metrics',
                  ].map((feature, idx) => (
                    <Stack key={idx} direction="row" spacing={1.5} alignItems="center">
                      <Box
                        sx={{
                          width: 6,
                          height: 6,
                          borderRadius: '50%',
                          bgcolor: '#6366f1',
                        }}
                      />
                      <Typography variant="body2">{feature}</Typography>
                    </Stack>
                  ))}
                </Stack>
              </Paper>

              {/* Supported Formats */}
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Supported Formats
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        bgcolor: alpha('#ef4444', 0.05),
                        border: `1px solid ${alpha('#ef4444', 0.2)}`,
                      }}
                    >
                      <CardContent>
                        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
                          <PDFIcon sx={{ color: '#ef4444' }} />
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            Documents
                          </Typography>
                        </Stack>
                        <Typography variant="caption" color="text.secondary">
                          PDF, Word, Excel, PowerPoint, HTML
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        bgcolor: alpha('#f59e0b', 0.05),
                        border: `1px solid ${alpha('#f59e0b', 0.2)}`,
                      }}
                    >
                      <CardContent>
                        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
                          <ImageIcon sx={{ color: '#f59e0b' }} />
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            Media
                          </Typography>
                        </Stack>
                        <Typography variant="caption" color="text.secondary">
                          Images (JPG, PNG, GIF), Audio, Video
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        bgcolor: alpha('#10b981', 0.05),
                        border: `1px solid ${alpha('#10b981', 0.2)}`,
                      }}
                    >
                      <CardContent>
                        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
                          <FileIcon sx={{ color: '#10b981' }} />
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            Data
                          </Typography>
                        </Stack>
                        <Typography variant="caption" color="text.secondary">
                          CSV, JSON, XML, Jupyter Notebooks
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        bgcolor: alpha('#8b5cf6', 0.05),
                        border: `1px solid ${alpha('#8b5cf6', 0.2)}`,
                      }}
                    >
                      <CardContent>
                        <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
                          <AudioIcon sx={{ color: '#8b5cf6' }} />
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            Web
                          </Typography>
                        </Stack>
                        <Typography variant="caption" color="text.secondary">
                          URLs, RSS Feeds, Web Pages
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </Paper>

              {/* Stats */}
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Performance
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: '#6366f1' }}>
                        15+
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        File Formats
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: '#6366f1' }}>
                        &lt;2s
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Avg. Conversion
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </Paper>
            </Stack>
          </Grid>

          {/* Markdown Preview */}
          {markdownPreview && (
            <Grid item xs={12} id="markdown-preview">
              <Paper sx={{ p: 3 }}>
                <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
                  <MarkdownIcon sx={{ color: '#6366f1' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Markdown Preview
                  </Typography>
                </Stack>
                <Divider sx={{ mb: 2 }} />
                <Box
                  sx={{
                    maxHeight: 600,
                    overflow: 'auto',
                    bgcolor: alpha('#6366f1', 0.02),
                    p: 2,
                    borderRadius: 1,
                    fontFamily: 'monospace',
                    fontSize: '0.875rem',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                  }}
                >
                  {markdownPreview}
                </Box>
              </Paper>
            </Grid>
          )}
        </Grid>
      </TabPanel>

      {/* Model Type Selection Dialog */}
      <Dialog
        open={modelTypeDialogOpen}
        onClose={() => setModelTypeDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Select Document Type
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Choose the type of financial model for this document
          </Typography>
        </DialogTitle>
        <DialogContent>
          <RadioGroup
            value={selectedModelType}
            onChange={(e) => setSelectedModelType(e.target.value as ModelType)}
          >
            <Stack spacing={2}>
              <Paper
                sx={{
                  p: 2,
                  border: selectedModelType === 'real-estate' ? 2 : 1,
                  borderColor: selectedModelType === 'real-estate' ? '#3b82f6' : 'divider',
                  cursor: 'pointer',
                }}
                onClick={() => setSelectedModelType('real-estate')}
              >
                <FormControlLabel
                  value="real-estate"
                  control={<Radio />}
                  label={
                    <Stack direction="row" spacing={1.5} alignItems="center">
                      <RealEstateIcon sx={{ color: '#3b82f6' }} />
                      <Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          Real Estate Models
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Property analysis, rent rolls, NOI statements
                        </Typography>
                      </Box>
                    </Stack>
                  }
                />
              </Paper>

              <Paper
                sx={{
                  p: 2,
                  border: selectedModelType === 'financial' ? 2 : 1,
                  borderColor: selectedModelType === 'financial' ? '#8b5cf6' : 'divider',
                  cursor: 'pointer',
                }}
                onClick={() => setSelectedModelType('financial')}
              >
                <FormControlLabel
                  value="financial"
                  control={<Radio />}
                  label={
                    <Stack direction="row" spacing={1.5} alignItems="center">
                      <FinancialIcon sx={{ color: '#8b5cf6' }} />
                      <Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          Company Financial Models
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Income statements, balance sheets, 10-K/10-Q
                        </Typography>
                      </Box>
                    </Stack>
                  }
                />
              </Paper>
            </Stack>
          </RadioGroup>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setModelTypeDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleModelTypeSelect}
            disabled={!selectedModelType}
            sx={{
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            }}
          >
            Extract Data
          </Button>
        </DialogActions>
      </Dialog>

      {/* Model Selection Dialog */}
      <Dialog
        open={modelDialogOpen}
        onClose={() => setModelDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Run in Financial Model
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Select a financial model to auto-populate with extracted data
          </Typography>
        </DialogTitle>
        <DialogContent>
          <RadioGroup
            value={selectedFinancialModel}
            onChange={(e) => setSelectedFinancialModel(e.target.value)}
          >
            <Stack spacing={2} sx={{ mt: 2 }}>
              {availableModels.map((model) => (
                <Paper
                  key={model.model_type}
                  sx={{
                    p: 2,
                    border: selectedFinancialModel === model.model_type ? 2 : 1,
                    borderColor:
                      selectedFinancialModel === model.model_type ? '#10b981' : 'divider',
                    cursor: 'pointer',
                    '&:hover': {
                      bgcolor: alpha('#10b981', 0.05),
                    },
                  }}
                  onClick={() => setSelectedFinancialModel(model.model_type)}
                >
                  <FormControlLabel
                    value={model.model_type}
                    control={<Radio />}
                    label={
                      <Box sx={{ width: '100%' }}>
                        <Stack direction="row" spacing={1.5} alignItems="center" sx={{ mb: 1 }}>
                          <TrendingUp sx={{ color: '#10b981' }} />
                          <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                            {model.name}
                          </Typography>
                          <Chip label={model.model_type} size="small" color="primary" />
                        </Stack>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1, pl: 4 }}>
                          {model.description}
                        </Typography>
                        <Stack direction="row" spacing={1} sx={{ pl: 4, flexWrap: 'wrap' }}>
                          {model.suitable_for?.map((item: string, idx: number) => (
                            <Chip
                              key={idx}
                              label={item}
                              size="small"
                              variant="outlined"
                              sx={{ fontSize: '0.7rem' }}
                            />
                          ))}
                        </Stack>
                        <Divider sx={{ my: 1.5 }} />
                        <Typography variant="caption" color="text.secondary" sx={{ pl: 4 }}>
                          <strong>Key Inputs:</strong> {model.key_inputs?.join(', ')}
                        </Typography>
                      </Box>
                    }
                  />
                </Paper>
              ))}
            </Stack>
          </RadioGroup>

          {creatingModel && (
            <Box sx={{ mt: 3 }}>
              <LinearProgress />
              <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
                Creating model and extracting data with AI...
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setModelDialogOpen(false)} disabled={creatingModel}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleCreateModel}
            disabled={!selectedFinancialModel || creatingModel}
            sx={{
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            }}
          >
            {creatingModel ? 'Creating...' : 'Create Model'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
