import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Alert,
  Stack,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
  Button,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  TextField,
} from '@mui/material';
import {
  CalendarMonth as CalendarIcon,
  ExpandMore as ExpandMoreIcon,
  Warning as WarningIcon,
  Event as EventIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import { apiClient } from '@/services/apiClient';

interface Deadline {
  date: string;
  task: string;
  form: string;
  who: string;
  penalty_for_missing: string;
  priority: string;
  note?: string;
  days_until?: number;
  status?: string;
}

interface CalendarData {
  [month: string]: Deadline[];
}

export const ComplianceCalendar: React.FC = () => {
  const [year, setYear] = useState(new Date().getFullYear());
  const [calendar, setCalendar] = useState<CalendarData | null>(null);
  const [upcomingDeadlines, setUpcomingDeadlines] = useState<Deadline[]>([]);
  const [daysAhead, setDaysAhead] = useState(90);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [expandedMonth, setExpandedMonth] = useState<string | false>(false);

  useEffect(() => {
    fetchCalendar();
    fetchUpcoming();
  }, [year]);

  const fetchCalendar = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiClient.get(`/tax-calculators/compliance-calendar/${year}`);
      setCalendar(data.calendar);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error fetching compliance calendar');
    } finally {
      setLoading(false);
    }
  };

  const fetchUpcoming = async () => {
    try {
      const data = await apiClient.get(`/tax-calculators/compliance-calendar/upcoming/${daysAhead}`);
      setUpcomingDeadlines(data.deadlines);
    } catch (err: any) {
      console.error('Error fetching upcoming deadlines:', err);
    }
  };

  const getPriorityColor = (priority: string): 'default' | 'error' | 'warning' | 'info' => {
    switch (priority) {
      case 'CRITICAL':
        return 'error';
      case 'HIGH':
        return 'error';
      case 'MEDIUM':
        return 'warning';
      case 'LOW':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status?: string): 'error' | 'warning' | 'info' => {
    if (status === 'URGENT') return 'error';
    return 'warning';
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const monthOrder = [
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'july',
    'august',
    'september',
    'october',
    'november',
    'december',
  ];

  const handleAccordionChange = (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
    setExpandedMonth(isExpanded ? panel : false);
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Tax Compliance Calendar
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Never miss a tax deadline. Track all IRS filing dates and compliance requirements.
        </Typography>
      </Box>

      {/* Year Selector */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Tax Year"
              type="number"
              value={year}
              onChange={(e) => setYear(parseInt(e.target.value))}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button variant="contained" fullWidth size="large" onClick={fetchCalendar} disabled={loading}>
              {loading ? 'Loading...' : 'Load Calendar'}
            </Button>
          </Grid>
          <Grid item xs={12} md={6}>
            <Alert severity="info" icon={<CalendarIcon />}>
              <Typography variant="body2">
                Viewing tax deadlines for calendar year {year}. Deadlines include federal, state, and payroll tax obligations.
              </Typography>
            </Alert>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {/* Upcoming Deadlines */}
      {upcomingDeadlines.length > 0 && (
        <Paper sx={{ p: 3, mb: 4, bgcolor: 'warning.light' }}>
          <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
            <WarningIcon />
            <Typography variant="h6" fontWeight="bold">
              Upcoming Deadlines (Next {daysAhead} Days)
            </Typography>
          </Stack>
          <Grid container spacing={2}>
            {upcomingDeadlines.slice(0, 4).map((deadline, idx) => (
              <Grid item xs={12} md={6} key={idx}>
                <Card sx={{ border: 1, borderColor: `${getStatusColor(deadline.status)}.main` }}>
                  <CardContent>
                    <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                      <Chip
                        label={deadline.status === 'URGENT' ? `${deadline.days_until} days` : `${deadline.days_until} days`}
                        color={getStatusColor(deadline.status)}
                        size="small"
                      />
                      <Chip label={deadline.priority} color={getPriorityColor(deadline.priority)} size="small" />
                    </Stack>
                    <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                      {deadline.task}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      <strong>Date:</strong> {formatDate(deadline.date)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      <strong>Form:</strong> {deadline.form}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      <strong>Who:</strong> {deadline.who}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
          {upcomingDeadlines.length > 4 && (
            <Alert severity="info" sx={{ mt: 2 }}>
              <Typography variant="body2">
                Showing 4 of {upcomingDeadlines.length} upcoming deadlines. View full calendar below for all dates.
              </Typography>
            </Alert>
          )}
        </Paper>
      )}

      {/* Full Calendar by Month */}
      {calendar && (
        <Box>
          <Typography variant="h5" fontWeight="bold" gutterBottom sx={{ mb: 2 }}>
            Full {year} Calendar
          </Typography>

          {monthOrder
            .filter((month) => calendar[month] && calendar[month].length > 0)
            .map((month) => (
              <Accordion
                key={month}
                expanded={expandedMonth === month}
                onChange={handleAccordionChange(month)}
                sx={{ mb: 2 }}
              >
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Stack direction="row" spacing={2} alignItems="center" sx={{ flex: 1 }}>
                    <EventIcon color="primary" />
                    <Typography variant="h6" fontWeight="bold" sx={{ textTransform: 'capitalize' }}>
                      {month}
                    </Typography>
                    <Chip label={`${calendar[month].length} deadlines`} size="small" color="primary" variant="outlined" />
                  </Stack>
                </AccordionSummary>
                <AccordionDetails>
                  <List>
                    {calendar[month].map((deadline, idx) => (
                      <React.Fragment key={idx}>
                        <ListItem
                          sx={{
                            display: 'block',
                            bgcolor: deadline.priority === 'CRITICAL' ? 'error.light' : 'transparent',
                            borderRadius: 1,
                            mb: 1,
                          }}
                        >
                          <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                            <Stack direction="row" spacing={1} alignItems="center">
                              <ScheduleIcon fontSize="small" color="action" />
                              <Typography variant="body2" fontWeight="bold">
                                {formatDate(deadline.date)}
                              </Typography>
                            </Stack>
                            <Chip label={deadline.priority} color={getPriorityColor(deadline.priority)} size="small" />
                          </Stack>

                          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                            {deadline.task}
                          </Typography>

                          <Grid container spacing={1} sx={{ mt: 1 }}>
                            <Grid item xs={12} md={6}>
                              <Typography variant="body2" color="text.secondary">
                                <strong>Form:</strong> {deadline.form}
                              </Typography>
                            </Grid>
                            <Grid item xs={12} md={6}>
                              <Typography variant="body2" color="text.secondary">
                                <strong>Who:</strong> {deadline.who}
                              </Typography>
                            </Grid>
                            <Grid item xs={12}>
                              <Typography variant="body2" color="error.main">
                                <strong>Penalty:</strong> {deadline.penalty_for_missing}
                              </Typography>
                            </Grid>
                            {deadline.note && (
                              <Grid item xs={12}>
                                <Alert severity="info" sx={{ mt: 1 }}>
                                  {deadline.note}
                                </Alert>
                              </Grid>
                            )}
                          </Grid>
                        </ListItem>
                        {idx < calendar[month].length - 1 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                </AccordionDetails>
              </Accordion>
            ))}
        </Box>
      )}

      {/* Tips Section */}
      <Paper sx={{ p: 3, mt: 4, bgcolor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom>
          Compliance Best Practices
        </Typography>
        <List>
          <ListItem>
            <ListItemText
              primary="Set Calendar Reminders"
              secondary="Add all relevant deadlines to your calendar with 2-week advance reminders"
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="File Even if You Can't Pay"
              secondary="Always file on time even if you can't pay. Failure-to-file penalties are much higher than failure-to-pay"
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Request Extensions When Needed"
              secondary="Use Form 4868 (individuals) or Form 7004 (businesses) to get automatic extensions"
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Track Estimated Tax Payments"
              secondary="Make quarterly estimated payments if you expect to owe $1,000+ to avoid underpayment penalties"
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Maintain Documentation"
              secondary="Keep all tax records for at least 7 years in case of audit"
            />
          </ListItem>
        </List>
      </Paper>
    </Container>
  );
};
