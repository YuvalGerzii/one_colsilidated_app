/**
 * Integration Testing Dashboard Component
 * 
 * Add this component to your app to run and visualize integration tests
 * Route: /testing or /integration-tests
 */

import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  List,
  ListItem,
  ListItemText,
  LinearProgress,
  Grid,
  Paper,
} from '@mui/material';
import {
  ExpandMore,
  PlayArrow,
  CheckCircle,
  Error,
  Warning,
  Info,
} from '@mui/icons-material';

// Import services
import companyService from '../services/companyService';
import financialService from '../services/financialService';
import modelService from '../services/modelService';

interface TestResult {
  name: string;
  status: 'pending' | 'running' | 'passed' | 'failed' | 'warning';
  duration?: number;
  message?: string;
  details?: any;
  error?: any;
}

interface TestSuite {
  name: string;
  description: string;
  tests: TestResult[];
  startTime?: number;
  endTime?: number;
}

export default function IntegrationTestsDashboard() {
  const [running, setRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [suites, setSuites] = useState<TestSuite[]>([]);

  // ==================
  // TEST DEFINITIONS
  // ==================

  const runHealthCheckSuite = async (): Promise<TestSuite> => {
    const suite: TestSuite = {
      name: 'Health Checks',
      description: 'Verify backend and database connectivity',
      tests: [],
      startTime: Date.now(),
    };

    // Test 1: Backend Health
    try {
      const start = Date.now();
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();
      
      suite.tests.push({
        name: 'Backend Health Check',
        status: data.status === 'healthy' ? 'passed' : 'failed',
        duration: Date.now() - start,
        message: `Backend status: ${data.status}`,
        details: data,
      });
    } catch (error: any) {
      suite.tests.push({
        name: 'Backend Health Check',
        status: 'failed',
        message: 'Cannot connect to backend',
        error: error.message,
      });
    }

    // Test 2: API Root
    try {
      const start = Date.now();
      const response = await fetch('http://localhost:8000/');
      const data = await response.json();
      
      suite.tests.push({
        name: 'API Root Endpoint',
        status: response.ok ? 'passed' : 'failed',
        duration: Date.now() - start,
        message: data.message,
        details: data,
      });
    } catch (error: any) {
      suite.tests.push({
        name: 'API Root Endpoint',
        status: 'failed',
        message: 'API root not accessible',
        error: error.message,
      });
    }

    // Test 3: CORS Check
    try {
      const start = Date.now();
      const response = await fetch('http://localhost:8000/api/v1/companies', {
        method: 'OPTIONS',
        headers: {
          'Origin': window.location.origin,
          'Access-Control-Request-Method': 'GET',
        },
      });
      
      const corsHeaders = response.headers.get('access-control-allow-origin');
      
      suite.tests.push({
        name: 'CORS Configuration',
        status: corsHeaders ? 'passed' : 'warning',
        duration: Date.now() - start,
        message: corsHeaders ? 'CORS headers present' : 'CORS headers missing',
        details: { corsHeaders },
      });
    } catch (error: any) {
      suite.tests.push({
        name: 'CORS Configuration',
        status: 'warning',
        message: 'Could not verify CORS',
        error: error.message,
      });
    }

    suite.endTime = Date.now();
    return suite;
  };

  const runCompanyCRUDSuite = async (): Promise<TestSuite> => {
    const suite: TestSuite = {
      name: 'Company CRUD Operations',
      description: 'Test create, read, update, delete operations for companies',
      tests: [],
      startTime: Date.now(),
    };

    let testCompanyId: string | null = null;

    // Test 1: Create Company
    try {
      const start = Date.now();
      const newCompany = await companyService.createCompany({
        fund_id: 'test-fund-id', // You may need to create a test fund first
        company_name: `Test Company ${Date.now()}`,
        industry: 'Technology',
        sector: 'Software',
        investment_date: new Date().toISOString().split('T')[0],
        company_status: 'Active',
      });
      
      testCompanyId = newCompany.company_id;
      
      suite.tests.push({
        name: 'Create Company',
        status: 'passed',
        duration: Date.now() - start,
        message: `Created company: ${newCompany.company_name}`,
        details: newCompany,
      });
    } catch (error: any) {
      suite.tests.push({
        name: 'Create Company',
        status: 'failed',
        message: 'Failed to create company',
        error: error.message,
      });
    }

    // Test 2: Read Company
    if (testCompanyId) {
      try {
        const start = Date.now();
        const company = await companyService.getCompany(testCompanyId);
        
        suite.tests.push({
          name: 'Read Company',
          status: 'passed',
          duration: Date.now() - start,
          message: `Retrieved company: ${company.company_name}`,
          details: company,
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'Read Company',
          status: 'failed',
          message: 'Failed to read company',
          error: error.message,
        });
      }

      // Test 3: Update Company
      try {
        const start = Date.now();
        const updated = await companyService.updateCompany(testCompanyId, {
          company_status: 'Under Review',
          employee_count: 100,
        });
        
        suite.tests.push({
          name: 'Update Company',
          status: 'passed',
          duration: Date.now() - start,
          message: 'Company updated successfully',
          details: updated,
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'Update Company',
          status: 'failed',
          message: 'Failed to update company',
          error: error.message,
        });
      }

      // Test 4: List Companies
      try {
        const start = Date.now();
        const companies = await companyService.getCompanies({ limit: 10 });
        
        suite.tests.push({
          name: 'List Companies',
          status: companies.length > 0 ? 'passed' : 'warning',
          duration: Date.now() - start,
          message: `Found ${companies.length} companies`,
          details: { count: companies.length },
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'List Companies',
          status: 'failed',
          message: 'Failed to list companies',
          error: error.message,
        });
      }

      // Test 5: Delete Company
      try {
        const start = Date.now();
        await companyService.deleteCompany(testCompanyId);
        
        suite.tests.push({
          name: 'Delete Company',
          status: 'passed',
          duration: Date.now() - start,
          message: 'Company deleted successfully',
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'Delete Company',
          status: 'failed',
          message: 'Failed to delete company',
          error: error.message,
        });
      }
    }

    suite.endTime = Date.now();
    return suite;
  };

  const runFinancialDataSuite = async (): Promise<TestSuite> => {
    const suite: TestSuite = {
      name: 'Financial Data Operations',
      description: 'Test financial metrics CRUD operations',
      tests: [],
      startTime: Date.now(),
    };

    let testCompanyId: string | null = null;
    let testMetricId: string | null = null;

    // Create a test company first
    try {
      const company = await companyService.createCompany({
        fund_id: 'test-fund-id',
        company_name: `Financial Test Co ${Date.now()}`,
        industry: 'Technology',
        sector: 'Software',
        investment_date: new Date().toISOString().split('T')[0],
        company_status: 'Active',
      });
      testCompanyId = company.company_id;
    } catch (error) {
      suite.tests.push({
        name: 'Setup Test Company',
        status: 'failed',
        message: 'Could not create test company',
      });
      suite.endTime = Date.now();
      return suite;
    }

    // Test 1: Create Financial Metric
    try {
      const start = Date.now();
      const metric = await financialService.createFinancial({
        company_id: testCompanyId,
        period_date: '2024-03-31',
        period_type: 'Quarterly',
        fiscal_year: 2024,
        fiscal_quarter: 1,
        revenue: 25000000,
        ebitda: 8000000,
        net_income: 5000000,
      });
      
      testMetricId = metric.metric_id;
      
      suite.tests.push({
        name: 'Create Financial Metric',
        status: 'passed',
        duration: Date.now() - start,
        message: 'Financial metric created',
        details: metric,
      });
    } catch (error: any) {
      suite.tests.push({
        name: 'Create Financial Metric',
        status: 'failed',
        message: 'Failed to create financial metric',
        error: error.message,
      });
    }

    // Test 2: Read Financial Metrics
    if (testCompanyId) {
      try {
        const start = Date.now();
        const metrics = await financialService.getFinancials({
          company_id: testCompanyId,
          period_type: 'Quarterly',
        });
        
        suite.tests.push({
          name: 'Read Financial Metrics',
          status: metrics.length > 0 ? 'passed' : 'warning',
          duration: Date.now() - start,
          message: `Found ${metrics.length} metrics`,
          details: { count: metrics.length },
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'Read Financial Metrics',
          status: 'failed',
          message: 'Failed to read financial metrics',
          error: error.message,
        });
      }
    }

    // Test 3: Batch Create
    if (testCompanyId) {
      try {
        const start = Date.now();
        const metrics = await financialService.batchCreateFinancials([
          {
            company_id: testCompanyId,
            period_date: '2024-06-30',
            period_type: 'Quarterly',
            fiscal_year: 2024,
            fiscal_quarter: 2,
            revenue: 27000000,
            ebitda: 9000000,
          },
          {
            company_id: testCompanyId,
            period_date: '2024-09-30',
            period_type: 'Quarterly',
            fiscal_year: 2024,
            fiscal_quarter: 3,
            revenue: 30000000,
            ebitda: 10000000,
          },
        ]);
        
        suite.tests.push({
          name: 'Batch Create Financials',
          status: 'passed',
          duration: Date.now() - start,
          message: `Created ${metrics.length} financial records`,
          details: { count: metrics.length },
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'Batch Create Financials',
          status: 'failed',
          message: 'Failed to batch create financials',
          error: error.message,
        });
      }
    }

    // Cleanup
    if (testCompanyId) {
      try {
        await companyService.deleteCompany(testCompanyId);
        suite.tests.push({
          name: 'Cleanup',
          status: 'passed',
          message: 'Test data cleaned up',
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'Cleanup',
          status: 'warning',
          message: 'Could not cleanup test data',
          error: error.message,
        });
      }
    }

    suite.endTime = Date.now();
    return suite;
  };

  const runModelGenerationSuite = async (): Promise<TestSuite> => {
    const suite: TestSuite = {
      name: 'Model Generation',
      description: 'Test Excel model generation functionality',
      tests: [],
      startTime: Date.now(),
    };

    let testCompanyId: string | null = null;

    // Setup: Create test company with financial data
    try {
      const company = await companyService.createCompany({
        fund_id: 'test-fund-id',
        company_name: `Model Test Co ${Date.now()}`,
        industry: 'Technology',
        sector: 'Software',
        investment_date: new Date().toISOString().split('T')[0],
        company_status: 'Active',
      });
      testCompanyId = company.company_id;

      // Add financial data
      await financialService.createFinancial({
        company_id: testCompanyId,
        period_date: '2024-12-31',
        period_type: 'Annual',
        fiscal_year: 2024,
        revenue: 100000000,
        ebitda: 30000000,
        net_income: 20000000,
      });
    } catch (error) {
      suite.tests.push({
        name: 'Setup Test Data',
        status: 'failed',
        message: 'Could not create test company',
      });
      suite.endTime = Date.now();
      return suite;
    }

    // Test 1: Generate DCF Model
    if (testCompanyId) {
      try {
        const start = Date.now();
        const result = await modelService.generateModel({
          company_id: testCompanyId,
          model_type: 'DCF',
          scenario_name: 'Integration Test',
        });
        
        suite.tests.push({
          name: 'Generate DCF Model',
          status: result.status === 'completed' ? 'passed' : 'failed',
          duration: Date.now() - start,
          message: result.status === 'completed' 
            ? `Model generated in ${result.generation_time}s` 
            : result.error_message || 'Generation failed',
          details: result,
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'Generate DCF Model',
          status: 'failed',
          message: 'Failed to generate DCF model',
          error: error.message,
        });
      }
    }

    // Test 2: Model History
    if (testCompanyId) {
      try {
        const start = Date.now();
        const history = await modelService.getModelHistory(testCompanyId);
        
        suite.tests.push({
          name: 'Get Model History',
          status: 'passed',
          duration: Date.now() - start,
          message: `Found ${history.length} model(s) in history`,
          details: { count: history.length },
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'Get Model History',
          status: 'failed',
          message: 'Failed to get model history',
          error: error.message,
        });
      }
    }

    // Cleanup
    if (testCompanyId) {
      try {
        await companyService.deleteCompany(testCompanyId);
        suite.tests.push({
          name: 'Cleanup',
          status: 'passed',
          message: 'Test data cleaned up',
        });
      } catch (error: any) {
        suite.tests.push({
          name: 'Cleanup',
          status: 'warning',
          message: 'Could not cleanup test data',
        });
      }
    }

    suite.endTime = Date.now();
    return suite;
  };

  // ==================
  // RUN ALL TESTS
  // ==================

  const runAllTests = async () => {
    setRunning(true);
    setProgress(0);
    setSuites([]);

    const totalSuites = 4;
    const results: TestSuite[] = [];

    try {
      // Suite 1: Health Checks
      setProgress(25);
      const healthSuite = await runHealthCheckSuite();
      results.push(healthSuite);
      setSuites([...results]);

      // Suite 2: Company CRUD
      setProgress(50);
      const companySuite = await runCompanyCRUDSuite();
      results.push(companySuite);
      setSuites([...results]);

      // Suite 3: Financial Data
      setProgress(75);
      const financialSuite = await runFinancialDataSuite();
      results.push(financialSuite);
      setSuites([...results]);

      // Suite 4: Model Generation
      setProgress(100);
      const modelSuite = await runModelGenerationSuite();
      results.push(modelSuite);
      setSuites([...results]);

    } catch (error) {
      console.error('Test suite execution error:', error);
    } finally {
      setRunning(false);
    }
  };

  // ==================
  // RENDER HELPERS
  // ==================

  const getStatusIcon = (status: TestResult['status']) => {
    switch (status) {
      case 'passed':
        return <CheckCircle color="success" />;
      case 'failed':
        return <Error color="error" />;
      case 'warning':
        return <Warning color="warning" />;
      case 'running':
        return <CircularProgress size={20} />;
      default:
        return <Info color="info" />;
    }
  };

  const getStatusColor = (status: TestResult['status']) => {
    switch (status) {
      case 'passed':
        return 'success';
      case 'failed':
        return 'error';
      case 'warning':
        return 'warning';
      default:
        return 'default';
    }
  };

  const calculateStats = () => {
    const allTests = suites.flatMap(s => s.tests);
    return {
      total: allTests.length,
      passed: allTests.filter(t => t.status === 'passed').length,
      failed: allTests.filter(t => t.status === 'failed').length,
      warnings: allTests.filter(t => t.status === 'warning').length,
    };
  };

  const stats = calculateStats();

  // ==================
  // RENDER
  // ==================

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Integration Tests
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Run these tests to verify frontend-backend integration and ensure all
        functionality is working correctly.
      </Typography>

      {/* Control Panel */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Button
            variant="contained"
            size="large"
            startIcon={running ? <CircularProgress size={20} /> : <PlayArrow />}
            onClick={runAllTests}
            disabled={running}
          >
            {running ? 'Running Tests...' : 'Run All Tests'}
          </Button>

          {running && (
            <Box sx={{ mt: 2 }}>
              <LinearProgress variant="determinate" value={progress} />
              <Typography variant="caption" sx={{ mt: 1, display: 'block' }}>
                Progress: {progress}%
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Stats */}
      {suites.length > 0 && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h3">{stats.total}</Typography>
              <Typography variant="body2" color="text.secondary">
                Total Tests
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={3}>
            <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'success.light' }}>
              <Typography variant="h3">{stats.passed}</Typography>
              <Typography variant="body2">Passed</Typography>
            </Paper>
          </Grid>
          <Grid item xs={3}>
            <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'error.light' }}>
              <Typography variant="h3">{stats.failed}</Typography>
              <Typography variant="body2">Failed</Typography>
            </Paper>
          </Grid>
          <Grid item xs={3}>
            <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'warning.light' }}>
              <Typography variant="h3">{stats.warnings}</Typography>
              <Typography variant="body2">Warnings</Typography>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* Test Suites */}
      {suites.map((suite, index) => (
        <Accordion key={index} defaultExpanded={true}>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
              <Typography variant="h6">{suite.name}</Typography>
              <Chip
                label={`${suite.tests.filter(t => t.status === 'passed').length}/${suite.tests.length} passed`}
                color={
                  suite.tests.every(t => t.status === 'passed')
                    ? 'success'
                    : suite.tests.some(t => t.status === 'failed')
                    ? 'error'
                    : 'warning'
                }
                size="small"
              />
              {suite.startTime && suite.endTime && (
                <Typography variant="caption" color="text.secondary">
                  {((suite.endTime - suite.startTime) / 1000).toFixed(2)}s
                </Typography>
              )}
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body2" color="text.secondary" paragraph>
              {suite.description}
            </Typography>

            <List>
              {suite.tests.map((test, testIndex) => (
                <ListItem key={testIndex} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, width: '100%' }}>
                    {getStatusIcon(test.status)}
                    <ListItemText
                      primary={test.name}
                      secondary={test.message}
                    />
                    <Chip
                      label={test.status}
                      color={getStatusColor(test.status)}
                      size="small"
                    />
                    {test.duration && (
                      <Typography variant="caption" color="text.secondary">
                        {test.duration}ms
                      </Typography>
                    )}
                  </Box>
                  
                  {test.error && (
                    <Alert severity="error" sx={{ mt: 1, width: '100%' }}>
                      {test.error}
                    </Alert>
                  )}
                  
                  {test.details && (
                    <Box sx={{ mt: 1, p: 1, bgcolor: 'grey.100', borderRadius: 1, width: '100%' }}>
                      <Typography variant="caption" component="pre" sx={{ overflow: 'auto' }}>
                        {JSON.stringify(test.details, null, 2)}
                      </Typography>
                    </Box>
                  )}
                </ListItem>
              ))}
            </List>
          </AccordionDetails>
        </Accordion>
      ))}

      {/* Overall Result */}
      {suites.length > 0 && !running && (
        <Alert
          severity={stats.failed === 0 ? 'success' : 'error'}
          sx={{ mt: 3 }}
        >
          {stats.failed === 0 ? (
            <Typography variant="h6">
              🎉 All tests passed! Your integration is working correctly.
            </Typography>
          ) : (
            <Typography variant="h6">
              ⚠️ {stats.failed} test(s) failed. Please review the errors above.
            </Typography>
          )}
        </Alert>
      )}
    </Box>
  );
}
