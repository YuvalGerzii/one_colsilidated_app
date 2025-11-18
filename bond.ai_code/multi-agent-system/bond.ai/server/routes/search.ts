import express from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { AdvancedSearchService, SearchQuery } from '../services/AdvancedSearchService';
import { authenticate } from '../auth/jwt';

/**
 * Advanced Search API Routes
 *
 * Provides endpoints for:
 * - Hybrid search (keyword + semantic)
 * - Search suggestions and autocomplete
 * - Search analytics
 * - Index management
 */

export function createSearchRoutes(pool: Pool, redis: Redis): express.Router {
  const router = express.Router();
  const searchService = new AdvancedSearchService(pool, redis);

  /**
   * POST /api/search
   * Main search endpoint with hybrid search support
   */
  router.post('/', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const startTime = Date.now();

      const query: SearchQuery = {
        query: req.body.query,
        filters: req.body.filters,
        limit: req.body.limit || 50,
        offset: req.body.offset || 0,
        searchMode: req.body.searchMode || 'hybrid',
        fuzzyMatch: req.body.fuzzyMatch !== false
      };

      if (!query.query || query.query.trim().length === 0) {
        return res.status(400).json({ error: 'Search query required' });
      }

      // Perform search
      const results = await searchService.search(query);

      // Log analytics
      const client = await pool.connect();
      try {
        await client.query(
          `INSERT INTO search_analytics (user_id, query, search_mode, filters, result_count, response_time)
           VALUES ($1, $2, $3, $4, $5, $6)`,
          [userId, query.query, query.searchMode, JSON.stringify(query.filters || {}), results.total, results.took]
        );

        // Add to user search history
        await client.query(
          `INSERT INTO user_search_history (user_id, query, filters)
           VALUES ($1, $2, $3)`,
          [userId, query.query, JSON.stringify(query.filters || {})]
        );
      } finally {
        client.release();
      }

      res.json({
        success: true,
        ...results
      });
    } catch (error) {
      console.error('Search error:', error);
      res.status(500).json({ error: 'Search failed' });
    }
  });

  /**
   * GET /api/search/suggestions
   * Get autocomplete suggestions based on partial query
   */
  router.get('/suggestions', authenticate, async (req, res) => {
    try {
      const { q } = req.query;

      if (!q || typeof q !== 'string' || q.trim().length < 2) {
        return res.json({ success: true, suggestions: [] });
      }

      const client = await pool.connect();

      try {
        const result = await client.query(
          `SELECT suggestion, category, score
           FROM get_search_suggestions($1, 10)`,
          [q]
        );

        res.json({
          success: true,
          suggestions: result.rows
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error getting suggestions:', error);
      res.status(500).json({ error: 'Failed to get suggestions' });
    }
  });

  /**
   * GET /api/search/personalized-suggestions
   * Get personalized suggestions based on user's search history
   */
  router.get('/personalized-suggestions', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;

      const client = await pool.connect();

      try {
        const result = await client.query(
          `SELECT suggestion, frequency
           FROM get_personalized_suggestions($1, 5)`,
          [userId]
        );

        res.json({
          success: true,
          suggestions: result.rows
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error getting personalized suggestions:', error);
      res.status(500).json({ error: 'Failed to get personalized suggestions' });
    }
  });

  /**
   * GET /api/search/popular
   * Get popular search queries
   */
  router.get('/popular', authenticate, async (req, res) => {
    try {
      const client = await pool.connect();

      try {
        const result = await client.query(
          `SELECT query, search_count, avg_results::INTEGER, avg_response_time::INTEGER
           FROM popular_searches
           ORDER BY search_count DESC
           LIMIT 10`
        );

        res.json({
          success: true,
          popular: result.rows
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error getting popular searches:', error);
      res.status(500).json({ error: 'Failed to get popular searches' });
    }
  });

  /**
   * POST /api/search/track-click
   * Track when a user clicks on a search result
   */
  router.post('/track-click', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { query, resultId, resultType } = req.body;

      if (!query || !resultId || !resultType) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      const client = await pool.connect();

      try {
        // Find the most recent search for this query
        await client.query(
          `UPDATE search_analytics
           SET clicked_result_id = $1,
               clicked_result_type = $2
           WHERE user_id = $3
             AND query = $4
             AND clicked_result_id IS NULL
           ORDER BY timestamp DESC
           LIMIT 1`,
          [resultId, resultType, userId, query]
        );

        res.json({ success: true });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error tracking click:', error);
      res.status(500).json({ error: 'Failed to track click' });
    }
  });

  /**
   * POST /api/search/index
   * Index a new entity for search (admin or automated)
   */
  router.post('/index', authenticate, async (req, res) => {
    try {
      const { id, type, title, description, industry, location, metadata } = req.body;

      if (!id || !type || !title || !description) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      await searchService.indexEntity(id, type, {
        title,
        description,
        industry,
        location,
        metadata
      });

      res.json({
        success: true,
        message: 'Entity indexed successfully'
      });
    } catch (error) {
      console.error('Error indexing entity:', error);
      res.status(500).json({ error: 'Failed to index entity' });
    }
  });

  /**
   * DELETE /api/search/index/:type/:id
   * Remove entity from search index
   */
  router.delete('/index/:type/:id', authenticate, async (req, res) => {
    try {
      const { type, id } = req.params;

      await searchService.removeEntity(id, type);

      res.json({
        success: true,
        message: 'Entity removed from index'
      });
    } catch (error) {
      console.error('Error removing entity from index:', error);
      res.status(500).json({ error: 'Failed to remove entity' });
    }
  });

  /**
   * POST /api/search/reindex
   * Reindex all entities (admin only)
   */
  router.post('/reindex', authenticate, async (req, res) => {
    try {
      // TODO: Add admin check
      // if (!req.user!.isAdmin) {
      //   return res.status(403).json({ error: 'Admin access required' });
      // }

      // Run reindex in background
      searchService.reindexAll().catch(error => {
        console.error('Reindex error:', error);
      });

      res.json({
        success: true,
        message: 'Reindexing started in background'
      });
    } catch (error) {
      console.error('Error starting reindex:', error);
      res.status(500).json({ error: 'Failed to start reindex' });
    }
  });

  /**
   * GET /api/search/analytics
   * Get search analytics for the current user
   */
  router.get('/analytics', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;

      const client = await pool.connect();

      try {
        const result = await client.query(
          `SELECT
             COUNT(*) as total_searches,
             COUNT(DISTINCT query) as unique_queries,
             AVG(result_count) as avg_results,
             AVG(response_time) as avg_response_time,
             COUNT(clicked_result_id) as total_clicks,
             (COUNT(clicked_result_id)::FLOAT / COUNT(*)::FLOAT * 100) as click_through_rate
           FROM search_analytics
           WHERE user_id = $1
             AND timestamp > NOW() - INTERVAL '30 days'`,
          [userId]
        );

        const stats = result.rows[0];

        res.json({
          success: true,
          analytics: {
            totalSearches: parseInt(stats.total_searches),
            uniqueQueries: parseInt(stats.unique_queries),
            avgResults: parseFloat(stats.avg_results || 0).toFixed(1),
            avgResponseTime: parseInt(stats.avg_response_time || 0),
            totalClicks: parseInt(stats.total_clicks),
            clickThroughRate: parseFloat(stats.click_through_rate || 0).toFixed(1)
          }
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error getting analytics:', error);
      res.status(500).json({ error: 'Failed to get analytics' });
    }
  });

  return router;
}
