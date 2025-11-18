/**
 * Semantic Matching Service
 * Uses sentence transformers for enhanced NLP matching
 * Replaces simple keyword matching with embeddings-based similarity
 */

import { pipeline, Pipeline } from '@xenova/transformers';
import { getDb } from '../database/connection';

export class SemanticMatcher {
  private embedder: Pipeline | null = null;
  private model = 'Xenova/all-MiniLM-L6-v2';
  private initialized = false;
  private embeddingDimension = 384;

  /**
   * Initialize the embedder model
   */
  async initialize(): Promise<void> {
    if (this.initialized) return;

    console.log('Initializing semantic matcher...');
    this.embedder = await pipeline('feature-extraction', this.model);
    this.initialized = true;
    console.log('Semantic matcher initialized');
  }

  /**
   * Ensure model is loaded
   */
  private async ensureInitialized(): Promise<void> {
    if (!this.initialized) {
      await this.initialize();
    }
  }

  /**
   * Generate embedding for text
   */
  async embed(text: string): Promise<number[]> {
    await this.ensureInitialized();

    const output = await this.embedder!(text, {
      pooling: 'mean',
      normalize: true,
    });

    // Extract the embedding array
    const embedding = Array.from(output.data);
    return embedding;
  }

  /**
   * Calculate cosine similarity between two embeddings
   */
  cosineSimilarity(embedding1: number[], embedding2: number[]): number {
    let dotProduct = 0;
    let norm1 = 0;
    let norm2 = 0;

    for (let i = 0; i < embedding1.length; i++) {
      dotProduct += embedding1[i] * embedding2[i];
      norm1 += embedding1[i] * embedding1[i];
      norm2 += embedding2[i] * embedding2[i];
    }

    norm1 = Math.sqrt(norm1);
    norm2 = Math.sqrt(norm2);

    if (norm1 === 0 || norm2 === 0) {
      return 0;
    }

    return dotProduct / (norm1 * norm2);
  }

  /**
   * Calculate semantic similarity between two texts
   */
  async calculateSimilarity(text1: string, text2: string): Promise<number> {
    const [embedding1, embedding2] = await Promise.all([
      this.embed(text1),
      this.embed(text2),
    ]);

    return this.cosineSimilarity(embedding1, embedding2);
  }

  /**
   * Get or create cached embedding
   */
  async getOrCreateEmbedding(
    entityType: string,
    entityId: string,
    text: string
  ): Promise<number[]> {
    const db = getDb();

    // Try to get from cache (Redis)
    const cacheKey = `embedding:${entityType}:${entityId}`;
    const cached = await db.getCacheJSON<number[]>(cacheKey);

    if (cached) {
      return cached;
    }

    // Try to get from database
    const dbResult = await db.queryOne<{ embedding: number[] }>(
      'SELECT embedding FROM embeddings WHERE entity_type = $1 AND entity_id = $2',
      [entityType, entityId]
    );

    if (dbResult) {
      // Cache for future use
      await db.setCacheJSON(cacheKey, dbResult.embedding, 3600); // 1 hour
      return dbResult.embedding;
    }

    // Generate new embedding
    const embedding = await this.embed(text);

    // Store in database
    await db.query(
      `INSERT INTO embeddings (entity_type, entity_id, text, embedding, model)
       VALUES ($1, $2, $3, $4, $5)
       ON CONFLICT (entity_type, entity_id) DO UPDATE
       SET embedding = $4, text = $3, model = $5`,
      [entityType, entityId, text, JSON.stringify(embedding), this.model]
    );

    // Cache for future use
    await db.setCacheJSON(cacheKey, embedding, 3600);

    return embedding;
  }

  /**
   * Match a need with offerings using semantic similarity
   */
  async matchNeedWithOfferings(
    need: { id: string; description: string },
    offerings: Array<{ id: string; description: string }>
  ): Promise<Array<{ offeringId: string; similarity: number }>> {
    const needEmbedding = await this.getOrCreateEmbedding(
      'need',
      need.id,
      need.description
    );

    const matches = await Promise.all(
      offerings.map(async (offering) => {
        const offeringEmbedding = await this.getOrCreateEmbedding(
          'offering',
          offering.id,
          offering.description
        );

        const similarity = this.cosineSimilarity(needEmbedding, offeringEmbedding);

        return {
          offeringId: offering.id,
          similarity,
        };
      })
    );

    // Sort by similarity descending
    return matches.sort((a, b) => b.similarity - a.similarity);
  }

  /**
   * Find similar entities using semantic search
   */
  async findSimilar(
    text: string,
    entityType: string,
    topK: number = 10,
    threshold: number = 0.5
  ): Promise<Array<{ entityId: string; text: string; similarity: number }>> {
    const queryEmbedding = await this.embed(text);

    // Get all embeddings of the entity type
    const db = getDb();
    const results = await db.queryMany<{
      entity_id: string;
      text: string;
      embedding: number[];
    }>(
      'SELECT entity_id, text, embedding FROM embeddings WHERE entity_type = $1',
      [entityType]
    );

    // Calculate similarities
    const similarities = results.map((result) => {
      const embedding =
        typeof result.embedding === 'string'
          ? JSON.parse(result.embedding)
          : result.embedding;

      const similarity = this.cosineSimilarity(queryEmbedding, embedding);

      return {
        entityId: result.entity_id,
        text: result.text,
        similarity,
      };
    });

    // Filter by threshold and sort
    return similarities
      .filter((s) => s.similarity >= threshold)
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, topK);
  }

  /**
   * Batch embed multiple texts
   */
  async batchEmbed(texts: string[]): Promise<number[][]> {
    return await Promise.all(texts.map((text) => this.embed(text)));
  }

  /**
   * Clear embedding cache
   */
  async clearCache(entityType?: string, entityId?: string): Promise<void> {
    const db = getDb();

    if (entityType && entityId) {
      await db.deleteCache(`embedding:${entityType}:${entityId}`);
    } else if (entityType) {
      await db.deleteCachePattern(`embedding:${entityType}:*`);
    } else {
      await db.deleteCachePattern('embedding:*');
    }
  }

  /**
   * Get embedding statistics
   */
  async getStats(): Promise<{
    total: number;
    byType: Record<string, number>;
    cacheSize: number;
  }> {
    const db = getDb();

    const total = await db.queryOne<{ count: number }>(
      'SELECT COUNT(*) as count FROM embeddings'
    );

    const byType = await db.queryMany<{ entity_type: string; count: number }>(
      'SELECT entity_type, COUNT(*) as count FROM embeddings GROUP BY entity_type'
    );

    const byTypeMap = byType.reduce(
      (acc, row) => {
        acc[row.entity_type] = row.count;
        return acc;
      },
      {} as Record<string, number>
    );

    // Redis cache size is harder to get exact number, so we return 0 for now
    const cacheSize = 0;

    return {
      total: total?.count || 0,
      byType: byTypeMap,
      cacheSize,
    };
  }
}

// Singleton instance
let semanticMatcherInstance: SemanticMatcher | null = null;

/**
 * Get semantic matcher instance
 */
export function getSemanticMatcher(): SemanticMatcher {
  if (!semanticMatcherInstance) {
    semanticMatcherInstance = new SemanticMatcher();
  }
  return semanticMatcherInstance;
}

/**
 * Initialize semantic matcher on startup
 */
export async function initSemanticMatcher(): Promise<SemanticMatcher> {
  const matcher = getSemanticMatcher();
  await matcher.initialize();
  return matcher;
}
