import { Pool } from 'pg';
import Redis from 'ioredis';
import { pipeline } from '@xenova/transformers';

/**
 * Advanced Search Service
 *
 * Implements hybrid search combining:
 * - PostgreSQL full-text search (FTS) for keyword precision
 * - pgvector semantic search for relevance
 * - pg_trgm for fuzzy matching (typos, variations)
 * - Pre-filtering with FTS before semantic ranking
 * - Query optimization for ~200ms response time
 */

export interface SearchQuery {
  query: string;
  filters?: {
    industries?: string[];
    matchTypes?: string[];
    locations?: string[];
    minScore?: number;
  };
  limit?: number;
  offset?: number;
  searchMode?: 'keyword' | 'semantic' | 'hybrid';
  fuzzyMatch?: boolean;
}

export interface SearchResult {
  id: string;
  type: 'user' | 'match' | 'need' | 'offering';
  title: string;
  description: string;
  score: number;
  keywordScore?: number;
  semanticScore?: number;
  metadata: Record<string, any>;
  highlights?: string[];
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  took: number; // milliseconds
  searchMode: string;
  suggestions?: string[];
}

export class AdvancedSearchService {
  private pool: Pool;
  private redis: Redis;
  private embeddingModel: any;
  private modelLoaded = false;

  constructor(pool: Pool, redis: Redis) {
    this.pool = pool;
    this.redis = redis;
    this.loadEmbeddingModel();
  }

  /**
   * Load embedding model for semantic search
   */
  private async loadEmbeddingModel() {
    try {
      this.embeddingModel = await pipeline(
        'feature-extraction',
        'Xenova/all-MiniLM-L6-v2'
      );
      this.modelLoaded = true;
      console.log('Embedding model loaded successfully');
    } catch (error) {
      console.error('Failed to load embedding model:', error);
    }
  }

  /**
   * Main search method - hybrid search by default
   */
  async search(query: SearchQuery): Promise<SearchResponse> {
    const startTime = Date.now();

    const {
      query: searchQuery,
      filters = {},
      limit = 50,
      offset = 0,
      searchMode = 'hybrid',
      fuzzyMatch = true
    } = query;

    let results: SearchResult[] = [];

    switch (searchMode) {
      case 'keyword':
        results = await this.keywordSearch(searchQuery, filters, limit, offset, fuzzyMatch);
        break;

      case 'semantic':
        results = await this.semanticSearch(searchQuery, filters, limit, offset);
        break;

      case 'hybrid':
      default:
        results = await this.hybridSearch(searchQuery, filters, limit, offset, fuzzyMatch);
        break;
    }

    const took = Date.now() - startTime;

    // Get search suggestions for better results
    const suggestions = await this.getSearchSuggestions(searchQuery);

    // Cache results
    await this.cacheSearchResults(searchQuery, results, searchMode);

    return {
      results,
      total: results.length,
      took,
      searchMode,
      suggestions
    };
  }

  /**
   * Hybrid search: FTS pre-filter + semantic ranking
   * Most effective approach based on 2025 research
   */
  private async hybridSearch(
    query: string,
    filters: any,
    limit: number,
    offset: number,
    fuzzyMatch: boolean
  ): Promise<SearchResult[]> {
    // Step 1: Pre-filter with full-text search (fast)
    const ftsResults = await this.keywordSearch(query, filters, limit * 5, 0, fuzzyMatch);

    if (ftsResults.length === 0) {
      return [];
    }

    // Step 2: Apply semantic ranking to pre-filtered results
    if (!this.modelLoaded) {
      // Fall back to keyword-only if model not loaded
      return ftsResults.slice(offset, offset + limit);
    }

    // Generate query embedding
    const queryEmbedding = await this.generateEmbedding(query);

    // Re-rank using semantic similarity
    const reranked = await Promise.all(
      ftsResults.map(async (result) => {
        const semanticScore = await this.calculateSemanticScore(
          result.id,
          result.type,
          queryEmbedding
        );

        // Combine scores: 40% keyword, 60% semantic
        const hybridScore = (result.score * 0.4) + (semanticScore * 0.6);

        return {
          ...result,
          score: hybridScore,
          keywordScore: result.score,
          semanticScore
        };
      })
    );

    // Sort by hybrid score
    reranked.sort((a, b) => b.score - a.score);

    return reranked.slice(offset, offset + limit);
  }

  /**
   * Keyword search using PostgreSQL full-text search
   */
  private async keywordSearch(
    query: string,
    filters: any,
    limit: number,
    offset: number,
    fuzzyMatch: boolean
  ): Promise<SearchResult[]> {
    const client = await this.pool.connect();

    try {
      // Build search query with ts_query
      const tsQuery = query
        .split(/\s+/)
        .map(word => `${word}:*`) // Prefix matching
        .join(' & ');

      // Build filters
      const conditions: string[] = ['search_vector @@ to_tsquery($1)'];
      const params: any[] = [tsQuery];
      let paramIndex = 2;

      if (filters.industries && filters.industries.length > 0) {
        conditions.push(`industry = ANY($${paramIndex})`);
        params.push(filters.industries);
        paramIndex++;
      }

      if (filters.matchTypes && filters.matchTypes.length > 0) {
        conditions.push(`match_type = ANY($${paramIndex})`);
        params.push(filters.matchTypes);
        paramIndex++;
      }

      if (filters.locations && filters.locations.length > 0) {
        conditions.push(`location_text = ANY($${paramIndex})`);
        params.push(filters.locations);
        paramIndex++;
      }

      const whereClause = conditions.join(' AND ');

      // Main search query with ranking
      let searchQuery = `
        SELECT
          id,
          type,
          title,
          description,
          industry,
          location_text,
          metadata,
          ts_rank(search_vector, to_tsquery($1)) as rank,
          ts_headline('english', description, to_tsquery($1),
            'MaxWords=50, MinWords=30, StartSel=<mark>, StopSel=</mark>') as highlight
        FROM search_index
        WHERE ${whereClause}
      `;

      // Add fuzzy matching for better typo tolerance
      if (fuzzyMatch) {
        searchQuery += `
          UNION
          SELECT
            id,
            type,
            title,
            description,
            industry,
            location_text,
            metadata,
            similarity(title, $${paramIndex}) as rank,
            description as highlight
          FROM search_index
          WHERE similarity(title, $${paramIndex}) > 0.3
        `;
        params.push(query);
      }

      searchQuery += `
        ORDER BY rank DESC
        LIMIT $${params.length + 1}
        OFFSET $${params.length + 2}
      `;

      params.push(limit, offset);

      const result = await client.query(searchQuery, params);

      return result.rows.map(row => ({
        id: row.id,
        type: row.type,
        title: row.title,
        description: row.description,
        score: parseFloat(row.rank),
        metadata: row.metadata,
        highlights: [row.highlight]
      }));
    } finally {
      client.release();
    }
  }

  /**
   * Semantic search using pgvector
   */
  private async semanticSearch(
    query: string,
    filters: any,
    limit: number,
    offset: number
  ): Promise<SearchResult[]> {
    if (!this.modelLoaded) {
      throw new Error('Embedding model not loaded');
    }

    const client = await this.pool.connect();

    try {
      // Generate query embedding
      const queryEmbedding = await this.generateEmbedding(query);

      // Build filters
      const conditions: string[] = [];
      const params: any[] = [JSON.stringify(queryEmbedding)];
      let paramIndex = 2;

      if (filters.industries && filters.industries.length > 0) {
        conditions.push(`industry = ANY($${paramIndex})`);
        params.push(filters.industries);
        paramIndex++;
      }

      if (filters.matchTypes && filters.matchTypes.length > 0) {
        conditions.push(`match_type = ANY($${paramIndex})`);
        params.push(filters.matchTypes);
        paramIndex++;
      }

      const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

      // Semantic search using cosine similarity
      const searchQuery = `
        SELECT
          si.id,
          si.type,
          si.title,
          si.description,
          si.metadata,
          1 - (e.embedding <=> $1::vector) as similarity
        FROM search_index si
        JOIN embeddings e ON si.id = e.entity_id AND si.type = e.entity_type
        ${whereClause}
        ORDER BY e.embedding <=> $1::vector
        LIMIT $${params.length + 1}
        OFFSET $${params.length + 2}
      `;

      params.push(limit, offset);

      const result = await client.query(searchQuery, params);

      return result.rows.map(row => ({
        id: row.id,
        type: row.type,
        title: row.title,
        description: row.description,
        score: parseFloat(row.similarity),
        metadata: row.metadata
      }));
    } finally {
      client.release();
    }
  }

  /**
   * Generate embedding for text
   */
  private async generateEmbedding(text: string): Promise<number[]> {
    // Check cache first
    const cacheKey = `embedding:${Buffer.from(text).toString('base64').slice(0, 50)}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Generate embedding
    const output = await this.embeddingModel(text, {
      pooling: 'mean',
      normalize: true
    });

    const embedding = Array.from(output.data);

    // Cache for 24 hours
    await this.redis.setex(cacheKey, 86400, JSON.stringify(embedding));

    return embedding;
  }

  /**
   * Calculate semantic score for an entity
   */
  private async calculateSemanticScore(
    entityId: string,
    entityType: string,
    queryEmbedding: number[]
  ): Promise<number> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(
        `SELECT 1 - (embedding <=> $1::vector) as similarity
         FROM embeddings
         WHERE entity_id = $2 AND entity_type = $3`,
        [JSON.stringify(queryEmbedding), entityId, entityType]
      );

      if (result.rows.length === 0) {
        return 0;
      }

      return parseFloat(result.rows[0].similarity);
    } finally {
      client.release();
    }
  }

  /**
   * Get search suggestions based on query
   */
  private async getSearchSuggestions(query: string): Promise<string[]> {
    const client = await this.pool.connect();

    try {
      // Get common search terms similar to query
      const result = await client.query(
        `SELECT DISTINCT title
         FROM search_index
         WHERE title % $1
         ORDER BY similarity(title, $1) DESC
         LIMIT 5`,
        [query]
      );

      return result.rows.map(row => row.title);
    } catch (error) {
      // pg_trgm might not be enabled
      return [];
    } finally {
      client.release();
    }
  }

  /**
   * Cache search results
   */
  private async cacheSearchResults(
    query: string,
    results: SearchResult[],
    searchMode: string
  ): Promise<void> {
    const cacheKey = `search:${searchMode}:${Buffer.from(query).toString('base64')}`;
    await this.redis.setex(cacheKey, 300, JSON.stringify(results)); // 5 minutes
  }

  /**
   * Index a new entity for search
   */
  async indexEntity(
    id: string,
    type: 'user' | 'match' | 'need' | 'offering',
    data: {
      title: string;
      description: string;
      industry?: string;
      location?: string;
      metadata?: Record<string, any>;
    }
  ): Promise<void> {
    const client = await this.pool.connect();

    try {
      // Insert into search index
      await client.query(
        `INSERT INTO search_index (id, type, title, description, industry, location_text, metadata, search_vector)
         VALUES ($1, $2, $3, $4, $5, $6, $7, to_tsvector('english', $3 || ' ' || $4))
         ON CONFLICT (id, type)
         DO UPDATE SET
           title = $3,
           description = $4,
           industry = $5,
           location_text = $6,
           metadata = $7,
           search_vector = to_tsvector('english', $3 || ' ' || $4),
           updated_at = NOW()`,
        [id, type, data.title, data.description, data.industry, data.location, JSON.stringify(data.metadata || {})]
      );

      // Generate and store embedding
      if (this.modelLoaded) {
        const text = `${data.title} ${data.description}`;
        const embedding = await this.generateEmbedding(text);

        await client.query(
          `INSERT INTO embeddings (entity_id, entity_type, embedding, text)
           VALUES ($1, $2, $3, $4)
           ON CONFLICT (entity_id, entity_type)
           DO UPDATE SET
             embedding = $3,
             text = $4,
             updated_at = NOW()`,
          [id, type, JSON.stringify(embedding), text]
        );
      }
    } finally {
      client.release();
    }
  }

  /**
   * Remove entity from search index
   */
  async removeEntity(id: string, type: string): Promise<void> {
    const client = await this.pool.connect();

    try {
      await client.query(
        `DELETE FROM search_index WHERE id = $1 AND type = $2`,
        [id, type]
      );

      await client.query(
        `DELETE FROM embeddings WHERE entity_id = $1 AND entity_type = $2`,
        [id, type]
      );
    } finally {
      client.release();
    }
  }

  /**
   * Reindex all entities (for bulk updates)
   */
  async reindexAll(): Promise<void> {
    console.log('Starting full reindex...');
    const startTime = Date.now();

    const client = await this.pool.connect();

    try {
      // Reindex users
      const users = await client.query(`
        SELECT id, name, bio, industry, location
        FROM users
        WHERE is_active = true
      `);

      for (const user of users.rows) {
        await this.indexEntity(user.id, 'user', {
          title: user.name,
          description: user.bio || '',
          industry: user.industry,
          location: user.location
        });
      }

      // Reindex needs
      const needs = await client.query(`
        SELECT un.id, un.category, un.description, u.industry, u.location
        FROM user_needs un
        JOIN users u ON un.user_id = u.id
        WHERE un.status = 'active'
      `);

      for (const need of needs.rows) {
        await this.indexEntity(need.id, 'need', {
          title: need.category,
          description: need.description,
          industry: need.industry,
          location: need.location
        });
      }

      // Reindex offerings
      const offerings = await client.query(`
        SELECT uo.id, uo.category, uo.description, u.industry, u.location
        FROM user_offerings uo
        JOIN users u ON uo.user_id = u.id
        WHERE uo.status = 'available'
      `);

      for (const offering of offerings.rows) {
        await this.indexEntity(offering.id, 'offering', {
          title: offering.category,
          description: offering.description,
          industry: offering.industry,
          location: offering.location
        });
      }

      const took = Date.now() - startTime;
      console.log(`Reindex completed in ${took}ms`);
    } finally {
      client.release();
    }
  }
}
