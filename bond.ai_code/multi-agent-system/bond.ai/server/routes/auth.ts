/**
 * Authentication Routes
 */

import express, { Request, Response } from 'express';
import { generateToken, generateRefreshToken, hashPassword, comparePassword, AuthRequest, authenticateToken } from '../auth/jwt';
import { getDb } from '../database/connection';

const router = express.Router();

/**
 * Register new user
 * POST /api/auth/register
 */
router.post('/register', async (req: Request, res: Response) => {
  try {
    const { email, password, name } = req.body;

    if (!email || !password || !name) {
      return res.status(400).json({ error: 'Email, password, and name are required' });
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ error: 'Invalid email format' });
    }

    // Validate password strength
    if (password.length < 8) {
      return res.status(400).json({ error: 'Password must be at least 8 characters' });
    }

    const db = getDb();

    // Check if user already exists
    const existing = await db.queryOne(
      'SELECT id FROM users WHERE email = $1',
      [email]
    );

    if (existing) {
      return res.status(409).json({ error: 'User already exists' });
    }

    // Hash password
    const passwordHash = await hashPassword(password);

    // Create user
    const user = await db.queryOne<{ id: string; email: string; name: string }>(
      `INSERT INTO users (email, password_hash, name, created_at)
       VALUES ($1, $2, $3, NOW())
       RETURNING id, email, name`,
      [email, passwordHash, name]
    );

    if (!user) {
      throw new Error('Failed to create user');
    }

    // Generate tokens
    const accessToken = generateToken({ userId: user.id, email: user.email });
    const refreshToken = generateRefreshToken({ userId: user.id, email: user.email });

    res.status(201).json({
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
      accessToken,
      refreshToken,
    });
  } catch (error: any) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Registration failed' });
  }
});

/**
 * Login
 * POST /api/auth/login
 */
router.post('/login', async (req: Request, res: Response) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    const db = getDb();

    // Get user
    const user = await db.queryOne<{
      id: string;
      email: string;
      name: string;
      password_hash: string;
      is_active: boolean;
    }>(
      'SELECT id, email, name, password_hash, is_active FROM users WHERE email = $1',
      [email]
    );

    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    if (!user.is_active) {
      return res.status(403).json({ error: 'Account is inactive' });
    }

    // Verify password
    const isValid = await comparePassword(password, user.password_hash);

    if (!isValid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Update last login
    await db.query(
      'UPDATE users SET last_login = NOW() WHERE id = $1',
      [user.id]
    );

    // Generate tokens
    const accessToken = generateToken({ userId: user.id, email: user.email });
    const refreshToken = generateRefreshToken({ userId: user.id, email: user.email });

    res.json({
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
      accessToken,
      refreshToken,
    });
  } catch (error: any) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Login failed' });
  }
});

/**
 * Get current user
 * GET /api/auth/me
 */
router.get('/me', authenticateToken, async (req: AuthRequest, res: Response) => {
  try {
    const db = getDb();

    const user = await db.queryOne<{
      id: string;
      email: string;
      name: string;
      created_at: Date;
    }>(
      'SELECT id, email, name, created_at FROM users WHERE id = $1',
      [req.user!.userId]
    );

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({ user });
  } catch (error: any) {
    console.error('Get user error:', error);
    res.status(500).json({ error: 'Failed to get user' });
  }
});

/**
 * Logout
 * POST /api/auth/logout
 */
router.post('/logout', authenticateToken, async (req: AuthRequest, res: Response) => {
  // In a JWT-based system, logout is typically handled client-side by removing the token
  // For additional security, you could implement a token blacklist in Redis
  res.json({ message: 'Logged out successfully' });
});

export default router;
