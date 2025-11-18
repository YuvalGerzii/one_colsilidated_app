import express from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { authenticate } from '../auth/jwt';
import { AnalyticsDashboardService } from '../services/AnalyticsDashboard';

/**
 * Analytics API Routes
 *
 * Provides endpoints for:
 * - Dashboard metrics
 * - Custom reports
 * - Export data
 * - Comparative analytics
 */

export function createAnalyticsRoutes(pool: Pool, redis: Redis): express.Router {
  const router = express.Router();
  const analyticsService = new AnalyticsDashboardService(pool, redis);

  /**
   * GET /api/analytics/dashboard
   * Get comprehensive dashboard metrics
   */
  router.get('/dashboard', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const timeRange = (req.query.timeRange as any) || '30d';

      const metrics = await analyticsService.getDashboardMetrics(userId, timeRange);

      res.json({
        success: true,
        metrics
      });
    } catch (error) {
      console.error('Error getting dashboard metrics:', error);
      res.status(500).json({ error: 'Failed to get dashboard metrics' });
    }
  });

  /**
   * GET /api/analytics/export
   * Export analytics data as CSV/JSON
   */
  router.get('/export', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const format = (req.query.format as string) || 'json';
      const timeRange = (req.query.timeRange as any) || '30d';

      const metrics = await analyticsService.getDashboardMetrics(userId, timeRange);

      if (format === 'csv') {
        // Convert to CSV
        const csv = this.metricsToCSV(metrics);
        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Content-Disposition', `attachment; filename="bond-ai-analytics-${Date.now()}.csv"`);
        res.send(csv);
      } else {
        res.json(metrics);
      }
    } catch (error) {
      console.error('Error exporting analytics:', error);
      res.status(500).json({ error: 'Failed to export analytics' });
    }
  });

  /**
   * Helper: Convert metrics to CSV
   */
  function metricsToCSV(metrics: any): string {
    const lines: string[] = [];

    // Overview section
    lines.push('OVERVIEW METRICS');
    lines.push('Metric,Value');
    lines.push(`Total Matches,${metrics.overview.totalMatches}`);
    lines.push(`Active Negotiations,${metrics.overview.activeNegotiations}`);
    lines.push(`Successful Agreements,${metrics.overview.successfulAgreements}`);
    lines.push(`Network Size,${metrics.overview.networkSize}`);
    lines.push(`Response Rate,${(metrics.overview.responseRate * 100).toFixed(2)}%`);
    lines.push(`Average Match Score,${(metrics.overview.averageMatchScore * 100).toFixed(2)}%`);
    lines.push('');

    // Trend data
    lines.push('TRENDS');
    lines.push('Date,Matches,Negotiations,Agreements,Network Growth');
    metrics.trends.forEach((trend: any) => {
      lines.push(`${trend.date},${trend.matches},${trend.negotiations},${trend.agreements},${trend.networkGrowth}`);
    });

    return lines.join('\n');
  }

  return router;
}
