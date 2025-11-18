import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

/**
 * Request Validation Middleware
 *
 * Provides robust validation for all API endpoints using Zod schemas
 */

// Common schemas
export const uuidSchema = z.string().uuid('Invalid UUID format');
export const emailSchema = z.string().email('Invalid email format');
export const paginationSchema = z.object({
  limit: z.number().min(1).max(100).optional().default(50),
  offset: z.number().min(0).optional().default(0)
});

// User schemas
export const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: emailSchema,
  password: z.string().min(8).max(100),
  industry: z.string().optional(),
  bio: z.string().max(1000).optional(),
  location: z.object({
    city: z.string().optional(),
    country: z.string().optional(),
    remote: z.boolean().optional()
  }).optional()
});

export const updateUserSchema = createUserSchema.partial();

// Profile schemas
export const needSchema = z.object({
  category: z.string().min(1).max(100),
  description: z.string().min(1).max(500),
  priority: z.enum(['low', 'medium', 'high', 'critical']),
  urgency: z.enum(['flexible', 'weeks', 'days', 'immediate']),
  flexibility: z.number().min(0).max(1).optional().default(0.5)
});

export const offeringSchema = z.object({
  category: z.string().min(1).max(100),
  description: z.string().min(1).max(500),
  value: z.string().min(1).max(200),
  capacity: z.enum(['limited', 'moderate', 'high', 'unlimited']),
  conditions: z.string().max(500).optional()
});

// Filter schemas
export const filterCriteriaSchema = z.object({
  location: z.object({
    cities: z.array(z.string()).optional(),
    countries: z.array(z.string()).optional(),
    radius: z.number().min(0).max(10000).optional(),
    remote: z.boolean().optional()
  }).optional(),
  industries: z.array(z.string()).optional(),
  expertiseAreas: z.array(z.string()).optional(),
  matchTypes: z.array(z.string()).optional(),
  minCompatibilityScore: z.number().min(0).max(1).optional(),
  needCategories: z.array(z.string()).optional(),
  offeringCategories: z.array(z.string()).optional()
});

// Message schemas
export const sendMessageSchema = z.object({
  conversationId: uuidSchema.optional(),
  recipientId: uuidSchema,
  content: z.string().min(1).max(10000),
  type: z.enum(['text', 'system', 'introduction', 'proposal']).optional()
});

// Validation middleware factory
export function validateBody<T extends z.ZodType>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors.map(err => ({
            path: err.path.join('.'),
            message: err.message
          }))
        });
      }
      next(error);
    }
  };
}

export function validateQuery<T extends z.ZodType>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.query = schema.parse(req.query) as any;
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors.map(err => ({
            path: err.path.join('.'),
            message: err.message
          }))
        });
      }
      next(error);
    }
  };
}

export function validateParams<T extends z.ZodType>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.params = schema.parse(req.params) as any;
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors.map(err => ({
            path: err.path.join('.'),
            message: err.message
          }))
        });
      }
      next(error);
    }
  };
}

// Common param validators
export const uuidParam = z.object({
  id: uuidSchema
});

// Health check schema
export const healthCheckSchema = z.object({
  includeDetails: z.boolean().optional().default(false)
});
