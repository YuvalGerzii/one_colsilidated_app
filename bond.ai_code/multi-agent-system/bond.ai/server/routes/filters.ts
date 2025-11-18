import express from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { SmartFilterService, FilterCriteria, FilterPreferences } from '../services/SmartFilterService';
import { authenticateToken as authenticate } from '../auth/jwt';

/**
 * Smart Match Filters API Routes
 *
 * Provides endpoints for:
 * - Applying filters to matches
 * - Saving and retrieving filter preferences
 * - Getting ML-based filter suggestions
 * - Managing saved filter sets
 */

export function createFilterRoutes(pool: Pool, redis: Redis): express.Router {
  const router = express.Router();
  const filterService = new SmartFilterService(pool, redis);

  /**
   * POST /api/filters/apply
   * Apply filters to match candidates with auto-apply support
   */
  router.post('/apply', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { criteria, limit = 50 } = req.body;

      if (!criteria) {
        return res.status(400).json({ error: 'Filter criteria required' });
      }

      const matches = await filterService.applyFilters(userId, criteria as FilterCriteria, limit);

      res.json({
        success: true,
        matches,
        count: matches.length,
        appliedCriteria: criteria
      });
    } catch (error) {
      console.error('Error applying filters:', error);
      res.status(500).json({ error: 'Failed to apply filters' });
    }
  });

  /**
   * POST /api/filters/preferences
   * Save filter preferences for a user
   */
  router.post('/preferences', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const {
        criteria,
        autoApply = true,
        saveAsDefault = false,
        name = 'default'
      } = req.body;

      if (!criteria) {
        return res.status(400).json({ error: 'Filter criteria required' });
      }

      const preferences: FilterPreferences = {
        userId,
        criteria,
        autoApply,
        saveAsDefault,
        name,
        isActive: true,
        createdAt: new Date(),
        updatedAt: new Date()
      };

      await filterService.saveFilterPreferences(preferences);

      res.json({
        success: true,
        message: 'Filter preferences saved',
        preferences
      });
    } catch (error) {
      console.error('Error saving filter preferences:', error);
      res.status(500).json({ error: 'Failed to save filter preferences' });
    }
  });

  /**
   * GET /api/filters/preferences
   * Get active filter preferences for the current user
   */
  router.get('/preferences', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const preferences = await filterService.getFilterPreferences(userId);

      if (!preferences) {
        return res.json({
          success: true,
          preferences: null,
          message: 'No filter preferences found'
        });
      }

      res.json({
        success: true,
        preferences
      });
    } catch (error) {
      console.error('Error getting filter preferences:', error);
      res.status(500).json({ error: 'Failed to get filter preferences' });
    }
  });

  /**
   * GET /api/filters/suggestions
   * Get ML-based filter suggestions for the current user
   * Based on behavior patterns and similar users
   */
  router.get('/suggestions', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const suggestions = await filterService.getFilterSuggestions(userId);

      res.json({
        success: true,
        suggestions,
        count: suggestions.length
      });
    } catch (error) {
      console.error('Error getting filter suggestions:', error);
      res.status(500).json({ error: 'Failed to get filter suggestions' });
    }
  });

  /**
   * GET /api/filters/popular
   * Get popular filter combinations used by other users
   */
  router.get('/popular', authenticate, async (req, res) => {
    try {
      const limit = parseInt(req.query.limit as string) || 5;
      const popularFilters = await filterService.getPopularFilters(limit);

      res.json({
        success: true,
        filters: popularFilters,
        count: popularFilters.length
      });
    } catch (error) {
      console.error('Error getting popular filters:', error);
      res.status(500).json({ error: 'Failed to get popular filters' });
    }
  });

  /**
   * DELETE /api/filters/preferences/:name
   * Delete a saved filter preference
   */
  router.delete('/preferences/:name', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { name } = req.params;

      const client = await pool.connect();
      try {
        await client.query(
          `UPDATE filter_preferences
           SET is_active = false, updated_at = NOW()
           WHERE user_id = $1 AND name = $2`,
          [userId, name]
        );

        // Clear cache
        await redis.del(`filter:${userId}`);

        res.json({
          success: true,
          message: 'Filter preference deleted'
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error deleting filter preference:', error);
      res.status(500).json({ error: 'Failed to delete filter preference' });
    }
  });

  /**
   * POST /api/filters/saved
   * Create a named saved filter set for quick access
   */
  router.post('/saved', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { name, description, criteria } = req.body;

      if (!name || !criteria) {
        return res.status(400).json({ error: 'Name and criteria required' });
      }

      const client = await pool.connect();
      try {
        const result = await client.query(
          `INSERT INTO saved_filters (user_id, name, description, criteria)
           VALUES ($1, $2, $3, $4)
           ON CONFLICT (user_id, name)
           DO UPDATE SET
             description = $3,
             criteria = $4
           RETURNING *`,
          [userId, name, description, JSON.stringify(criteria)]
        );

        res.json({
          success: true,
          message: 'Filter saved',
          filter: result.rows[0]
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error saving filter:', error);
      res.status(500).json({ error: 'Failed to save filter' });
    }
  });

  /**
   * GET /api/filters/saved
   * Get all saved filters for the current user
   */
  router.get('/saved', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;

      const client = await pool.connect();
      try {
        const result = await client.query(
          `SELECT * FROM saved_filters
           WHERE user_id = $1
           ORDER BY last_used_at DESC NULLS LAST, created_at DESC`,
          [userId]
        );

        res.json({
          success: true,
          filters: result.rows,
          count: result.rows.length
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error getting saved filters:', error);
      res.status(500).json({ error: 'Failed to get saved filters' });
    }
  });

  /**
   * PUT /api/filters/saved/:id/use
   * Mark a saved filter as used (updates usage stats)
   */
  router.put('/saved/:id/use', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { id } = req.params;

      const client = await pool.connect();
      try {
        await client.query(
          `UPDATE saved_filters
           SET usage_count = usage_count + 1,
               last_used_at = NOW()
           WHERE id = $1 AND user_id = $2`,
          [id, userId]
        );

        res.json({
          success: true,
          message: 'Filter usage tracked'
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error tracking filter usage:', error);
      res.status(500).json({ error: 'Failed to track filter usage' });
    }
  });

  return router;
}
