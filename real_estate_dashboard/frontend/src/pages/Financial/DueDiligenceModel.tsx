import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Stack,
  Card,
  CardContent,
  Checkbox,
  FormControlLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Chip,
  Button,
  TextField,
  alpha,
  Divider,
} from '@mui/material';
import {
  ExpandMore as ExpandIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Assignment as DDIcon,
  Save as SaveIcon,
  Download as DownloadIcon,
  FileUpload as UploadIcon,
} from '@mui/icons-material';

interface ChecklistItem {
  id: string;
  label: string;
  completed: boolean;
  critical: boolean;
  notes?: string;
}

interface ChecklistCategory {
  id: string;
  title: string;
  items: ChecklistItem[];
  color: string;
}

export const DueDiligenceModel: React.FC = () => {
  const [categories, setCategories] = useState<ChecklistCategory[]>([
    {
      id: 'financial',
      title: 'Financial Due Diligence',
      color: '#3b82f6',
      items: [
        { id: 'f1', label: 'Review 3-5 years of audited financial statements', completed: false, critical: true },
        { id: 'f2', label: 'Analyze revenue recognition policies', completed: false, critical: true },
        { id: 'f3', label: 'Verify working capital trends', completed: false, critical: false },
        { id: 'f4', label: 'Review accounts receivable aging', completed: false, critical: false },
        { id: 'f5', label: 'Analyze inventory turnover and obsolescence', completed: false, critical: false },
        { id: 'f6', label: 'Examine debt covenants and restrictions', completed: false, critical: true },
        { id: 'f7', label: 'Review capital expenditure history', completed: false, critical: false },
        { id: 'f8', label: 'Analyze EBITDA adjustments and quality', completed: false, critical: true },
        { id: 'f9', label: 'Verify customer concentration risk', completed: false, critical: true },
        { id: 'f10', label: 'Review tax returns and deferred tax assets', completed: false, critical: false },
      ],
    },
    {
      id: 'legal',
      title: 'Legal Due Diligence',
      color: '#8b5cf6',
      items: [
        { id: 'l1', label: 'Review all material contracts and agreements', completed: false, critical: true },
        { id: 'l2', label: 'Verify ownership of intellectual property', completed: false, critical: true },
        { id: 'l3', label: 'Check pending or threatened litigation', completed: false, critical: true },
        { id: 'l4', label: 'Review employment agreements and compensation', completed: false, critical: false },
        { id: 'l5', label: 'Examine regulatory compliance history', completed: false, critical: true },
        { id: 'l6', label: 'Verify licenses and permits', completed: false, critical: true },
        { id: 'l7', label: 'Review insurance policies and claims', completed: false, critical: false },
        { id: 'l8', label: 'Check corporate governance documents', completed: false, critical: false },
      ],
    },
    {
      id: 'operational',
      title: 'Operational Due Diligence',
      color: '#10b981',
      items: [
        { id: 'o1', label: 'Assess production capacity and efficiency', completed: false, critical: false },
        { id: 'o2', label: 'Review supply chain and vendor relationships', completed: false, critical: true },
        { id: 'o3', label: 'Analyze key customer relationships', completed: false, critical: true },
        { id: 'o4', label: 'Evaluate IT systems and infrastructure', completed: false, critical: false },
        { id: 'o5', label: 'Review quality control processes', completed: false, critical: false },
        { id: 'o6', label: 'Assess human resources and culture', completed: false, critical: false },
        { id: 'o7', label: 'Examine product development pipeline', completed: false, critical: false },
        { id: 'o8', label: 'Review sales and marketing strategies', completed: false, critical: false },
      ],
    },
    {
      id: 'commercial',
      title: 'Commercial Due Diligence',
      color: '#f59e0b',
      items: [
        { id: 'c1', label: 'Analyze market size and growth trends', completed: false, critical: true },
        { id: 'c2', label: 'Assess competitive positioning', completed: false, critical: true },
        { id: 'c3', label: 'Review customer satisfaction and retention', completed: false, critical: false },
        { id: 'c4', label: 'Evaluate pricing power and strategy', completed: false, critical: false },
        { id: 'c5', label: 'Assess barriers to entry', completed: false, critical: false },
        { id: 'c6', label: 'Review market share trends', completed: false, critical: true },
      ],
    },
    {
      id: 'tax',
      title: 'Tax Due Diligence',
      color: '#ef4444',
      items: [
        { id: 't1', label: 'Review federal and state tax returns (3-5 years)', completed: false, critical: true },
        { id: 't2', label: 'Identify tax audit history and exposure', completed: false, critical: true },
        { id: 't3', label: 'Analyze NOL carryforwards and limitations', completed: false, critical: false },
        { id: 't4', label: 'Review transfer pricing policies', completed: false, critical: false },
        { id: 't5', label: 'Assess sales and use tax compliance', completed: false, critical: false },
        { id: 't6', label: 'Evaluate tax structure optimization opportunities', completed: false, critical: false },
      ],
    },
    {
      id: 'environmental',
      title: 'Environmental Due Diligence',
      color: '#06b6d4',
      items: [
        { id: 'e1', label: 'Conduct Phase I environmental assessment', completed: false, critical: true },
        { id: 'e2', label: 'Review environmental permits and compliance', completed: false, critical: true },
        { id: 'e3', label: 'Assess potential contamination liabilities', completed: false, critical: true },
        { id: 'e4', label: 'Review waste disposal practices', completed: false, critical: false },
        { id: 'e5', label: 'Check asbestos and hazardous materials', completed: false, critical: false },
      ],
    },
  ]);

  const [companyName, setCompanyName] = useState('');
  const [targetValue, setTargetValue] = useState('');

  const handleItemToggle = (categoryId: string, itemId: string) => {
    setCategories(prev =>
      prev.map(cat =>
        cat.id === categoryId
          ? {
              ...cat,
              items: cat.items.map(item =>
                item.id === itemId ? { ...item, completed: !item.completed } : item
              ),
            }
          : cat
      )
    );
  };

  const calculateProgress = () => {
    const totalItems = categories.reduce((sum, cat) => sum + cat.items.length, 0);
    const completedItems = categories.reduce(
      (sum, cat) => sum + cat.items.filter(item => item.completed).length,
      0
    );
    return totalItems > 0 ? (completedItems / totalItems) * 100 : 0;
  };

  const getCriticalItemsRemaining = () => {
    return categories.reduce(
      (sum, cat) => sum + cat.items.filter(item => item.critical && !item.completed).length,
      0
    );
  };

  const getCategoryProgress = (category: ChecklistCategory) => {
    const total = category.items.length;
    const completed = category.items.filter(item => item.completed).length;
    return total > 0 ? (completed / total) * 100 : 0;
  };

  const overallProgress = calculateProgress();
  const criticalRemaining = getCriticalItemsRemaining();

  return (
    <Box>
      {/* Header */}
      <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 3 }}>
        <Box
          sx={{
            width: 56,
            height: 56,
            background: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
            borderRadius: 3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 20px rgba(236, 72, 153, 0.3)',
          }}
        >
          <DDIcon sx={{ fontSize: 32, color: 'white' }} />
        </Box>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Due Diligence Model
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Comprehensive checklist for M&A and investment analysis
          </Typography>
        </Box>
      </Stack>

      <Grid container spacing={3}>
        {/* Left Panel - Info & Progress */}
        <Grid item xs={12} lg={4}>
          <Stack spacing={3}>
            {/* Target Info */}
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                Target Information
              </Typography>
              <Stack spacing={2}>
                <TextField
                  label="Company Name"
                  fullWidth
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                />
                <TextField
                  label="Enterprise Value ($M)"
                  type="number"
                  fullWidth
                  value={targetValue}
                  onChange={(e) => setTargetValue(e.target.value)}
                />
              </Stack>
            </Paper>

            {/* Overall Progress */}
            <Card sx={{ background: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)', color: 'white' }}>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Overall Progress
                </Typography>

                <Box sx={{ mb: 2 }}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Completion
                    </Typography>
                    <Typography variant="h5" sx={{ fontWeight: 700 }}>
                      {overallProgress.toFixed(0)}%
                    </Typography>
                  </Stack>
                  <LinearProgress
                    variant="determinate"
                    value={overallProgress}
                    sx={{
                      height: 10,
                      borderRadius: 5,
                      bgcolor: 'rgba(255,255,255,0.2)',
                      '& .MuiLinearProgress-bar': {
                        bgcolor: 'white',
                      },
                    }}
                  />
                </Box>

                <Divider sx={{ my: 2, bgcolor: 'rgba(255,255,255,0.2)' }} />

                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Box>
                      <Typography variant="caption" sx={{ opacity: 0.9 }}>
                        Total Items
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700 }}>
                        {categories.reduce((sum, cat) => sum + cat.items.length, 0)}
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box>
                      <Typography variant="caption" sx={{ opacity: 0.9 }}>
                        Critical Remaining
                      </Typography>
                      <Typography
                        variant="h4"
                        sx={{
                          fontWeight: 700,
                          color: criticalRemaining > 0 ? '#fbbf24' : 'white',
                        }}
                      >
                        {criticalRemaining}
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>

                {criticalRemaining > 0 && (
                  <Box
                    sx={{
                      mt: 2,
                      p: 2,
                      bgcolor: 'rgba(251, 191, 36, 0.2)',
                      borderRadius: 2,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 1,
                    }}
                  >
                    <WarningIcon sx={{ color: '#fbbf24' }} />
                    <Typography variant="body2">
                      {criticalRemaining} critical item{criticalRemaining > 1 ? 's' : ''} remaining
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>

            {/* Action Buttons */}
            <Stack spacing={2}>
              <Button
                variant="contained"
                startIcon={<SaveIcon />}
                fullWidth
                sx={{
                  py: 1.5,
                  background: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
                  fontWeight: 600,
                }}
              >
                Save Progress
              </Button>
              <Button
                variant="outlined"
                startIcon={<DownloadIcon />}
                fullWidth
              >
                Export Report
              </Button>
              <Button
                variant="outlined"
                startIcon={<UploadIcon />}
                fullWidth
              >
                Attach Documents
              </Button>
            </Stack>
          </Stack>
        </Grid>

        {/* Right Panel - Checklist Categories */}
        <Grid item xs={12} lg={8}>
          <Stack spacing={2}>
            {categories.map((category) => {
              const progress = getCategoryProgress(category);
              const completedCount = category.items.filter(item => item.completed).length;

              return (
                <Accordion key={category.id} defaultExpanded>
                  <AccordionSummary expandIcon={<ExpandIcon />}>
                    <Stack
                      direction="row"
                      alignItems="center"
                      justifyContent="space-between"
                      sx={{ width: '100%', pr: 2 }}
                    >
                      <Stack direction="row" alignItems="center" spacing={2}>
                        <Box
                          sx={{
                            width: 12,
                            height: 12,
                            borderRadius: '50%',
                            bgcolor: category.color,
                          }}
                        />
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          {category.title}
                        </Typography>
                      </Stack>
                      <Stack direction="row" spacing={2} alignItems="center">
                        <Chip
                          label={`${completedCount}/${category.items.length}`}
                          size="small"
                          sx={{
                            bgcolor: alpha(category.color, 0.1),
                            color: category.color,
                            fontWeight: 600,
                          }}
                        />
                        <Box sx={{ width: 100 }}>
                          <LinearProgress
                            variant="determinate"
                            value={progress}
                            sx={{
                              height: 6,
                              borderRadius: 3,
                              bgcolor: alpha(category.color, 0.1),
                              '& .MuiLinearProgress-bar': {
                                bgcolor: category.color,
                              },
                            }}
                          />
                        </Box>
                      </Stack>
                    </Stack>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Stack spacing={1}>
                      {category.items.map((item) => (
                        <Paper
                          key={item.id}
                          sx={{
                            p: 2,
                            bgcolor: item.completed ? alpha(category.color, 0.05) : 'background.paper',
                            border: item.critical ? `1px solid ${alpha('#ef4444', 0.3)}` : '1px solid',
                            borderColor: item.completed ? category.color : 'divider',
                          }}
                        >
                          <Stack direction="row" alignItems="center" spacing={2}>
                            <FormControlLabel
                              control={
                                <Checkbox
                                  checked={item.completed}
                                  onChange={() => handleItemToggle(category.id, item.id)}
                                  sx={{
                                    color: category.color,
                                    '&.Mui-checked': {
                                      color: category.color,
                                    },
                                  }}
                                />
                              }
                              label={
                                <Stack direction="row" spacing={1} alignItems="center">
                                  <Typography
                                    variant="body2"
                                    sx={{
                                      textDecoration: item.completed ? 'line-through' : 'none',
                                      color: item.completed ? 'text.secondary' : 'text.primary',
                                    }}
                                  >
                                    {item.label}
                                  </Typography>
                                  {item.critical && (
                                    <Chip
                                      label="Critical"
                                      size="small"
                                      sx={{
                                        bgcolor: alpha('#ef4444', 0.1),
                                        color: '#ef4444',
                                        fontSize: '0.65rem',
                                        height: 20,
                                      }}
                                    />
                                  )}
                                </Stack>
                              }
                              sx={{ flex: 1, m: 0 }}
                            />
                            {item.completed && (
                              <CheckIcon sx={{ color: category.color, fontSize: 20 }} />
                            )}
                          </Stack>
                        </Paper>
                      ))}
                    </Stack>
                  </AccordionDetails>
                </Accordion>
              );
            })}
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
};
