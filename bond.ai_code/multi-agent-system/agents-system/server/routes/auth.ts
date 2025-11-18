import { Router, Request, Response } from 'express';
import { Pool } from 'pg';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';
import { authenticateToken, AuthRequest } from '../middleware/auth';

dotenv.config();

export function createAuthRoutes(pool: Pool): Router {
  const router = Router();

  // POST /api/auth/register - Register new user
  router.post('/register', async (req: Request, res: Response) => {
    try {
      const { email, password, fullName } = req.body;

      // Validation
      if (!email || !password) {
        res.status(400).json({
          success: false,
          error: 'Email and password are required',
        });
        return;
      }

      // Email format validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        res.status(400).json({
          success: false,
          error: 'Invalid email format',
        });
        return;
      }

      // Password strength validation
      if (password.length < 8) {
        res.status(400).json({
          success: false,
          error: 'Password must be at least 8 characters long',
        });
        return;
      }

      // Check if user already exists
      const existingUser = await pool.query(
        'SELECT id FROM users WHERE email = $1',
        [email.toLowerCase()]
      );

      if (existingUser.rows.length > 0) {
        res.status(409).json({
          success: false,
          error: 'User with this email already exists',
        });
        return;
      }

      // Hash password
      const saltRounds = 10;
      const passwordHash = await bcrypt.hash(password, saltRounds);

      // Create user
      const result = await pool.query(
        `INSERT INTO users (email, password_hash, full_name)
        VALUES ($1, $2, $3)
        RETURNING id, email, full_name as "fullName", created_at as "createdAt"`,
        [email.toLowerCase(), passwordHash, fullName || null]
      );

      const user = result.rows[0];

      // Generate JWT token
      const secret = process.env.JWT_SECRET || 'your-secret-key-change-this-in-production';
      const expiresIn = process.env.JWT_EXPIRES_IN || '7d';

      const token = jwt.sign(
        { userId: user.id, email: user.email },
        secret,
        { expiresIn }
      );

      res.status(201).json({
        success: true,
        message: 'User registered successfully',
        user: {
          id: user.id,
          email: user.email,
          fullName: user.fullName,
        },
        token,
      });
    } catch (error) {
      console.error('Error registering user:', error);
      res.status(500).json({ success: false, error: 'Failed to register user' });
    }
  });

  // POST /api/auth/login - Login user
  router.post('/login', async (req: Request, res: Response) => {
    try {
      const { email, password } = req.body;

      // Validation
      if (!email || !password) {
        res.status(400).json({
          success: false,
          error: 'Email and password are required',
        });
        return;
      }

      // Get user
      const result = await pool.query(
        `SELECT id, email, password_hash, full_name as "fullName", is_active as "isActive"
        FROM users
        WHERE email = $1`,
        [email.toLowerCase()]
      );

      if (result.rows.length === 0) {
        res.status(401).json({
          success: false,
          error: 'Invalid email or password',
        });
        return;
      }

      const user = result.rows[0];

      // Check if user is active
      if (!user.isActive) {
        res.status(403).json({
          success: false,
          error: 'Account is deactivated',
        });
        return;
      }

      // Verify password
      const passwordMatch = await bcrypt.compare(password, user.password_hash);
      if (!passwordMatch) {
        res.status(401).json({
          success: false,
          error: 'Invalid email or password',
        });
        return;
      }

      // Generate JWT token
      const secret = process.env.JWT_SECRET || 'your-secret-key-change-this-in-production';
      const expiresIn = process.env.JWT_EXPIRES_IN || '7d';

      const token = jwt.sign(
        { userId: user.id, email: user.email },
        secret,
        { expiresIn }
      );

      res.json({
        success: true,
        message: 'Login successful',
        user: {
          id: user.id,
          email: user.email,
          fullName: user.fullName,
        },
        token,
      });
    } catch (error) {
      console.error('Error logging in:', error);
      res.status(500).json({ success: false, error: 'Failed to login' });
    }
  });

  // GET /api/auth/me - Get current user profile (requires auth)
  router.get('/me', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT id, email, full_name as "fullName", created_at as "createdAt"
        FROM users
        WHERE id = $1`,
        [userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({
          success: false,
          error: 'User not found',
        });
        return;
      }

      res.json({
        success: true,
        user: result.rows[0],
      });
    } catch (error) {
      console.error('Error fetching user profile:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch user profile' });
    }
  });

  // PUT /api/auth/profile - Update user profile (requires auth)
  router.put('/profile', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { fullName } = req.body;

      const result = await pool.query(
        `UPDATE users
        SET full_name = $1
        WHERE id = $2
        RETURNING id, email, full_name as "fullName"`,
        [fullName, userId]
      );

      res.json({
        success: true,
        message: 'Profile updated successfully',
        user: result.rows[0],
      });
    } catch (error) {
      console.error('Error updating profile:', error);
      res.status(500).json({ success: false, error: 'Failed to update profile' });
    }
  });

  // POST /api/auth/change-password - Change password (requires auth)
  router.post('/change-password', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { currentPassword, newPassword } = req.body;

      // Validation
      if (!currentPassword || !newPassword) {
        res.status(400).json({
          success: false,
          error: 'Current password and new password are required',
        });
        return;
      }

      if (newPassword.length < 8) {
        res.status(400).json({
          success: false,
          error: 'New password must be at least 8 characters long',
        });
        return;
      }

      // Get current password hash
      const userResult = await pool.query(
        'SELECT password_hash FROM users WHERE id = $1',
        [userId]
      );

      if (userResult.rows.length === 0) {
        res.status(404).json({ success: false, error: 'User not found' });
        return;
      }

      // Verify current password
      const passwordMatch = await bcrypt.compare(
        currentPassword,
        userResult.rows[0].password_hash
      );

      if (!passwordMatch) {
        res.status(401).json({
          success: false,
          error: 'Current password is incorrect',
        });
        return;
      }

      // Hash new password
      const saltRounds = 10;
      const newPasswordHash = await bcrypt.hash(newPassword, saltRounds);

      // Update password
      await pool.query(
        'UPDATE users SET password_hash = $1 WHERE id = $2',
        [newPasswordHash, userId]
      );

      res.json({
        success: true,
        message: 'Password changed successfully',
      });
    } catch (error) {
      console.error('Error changing password:', error);
      res.status(500).json({ success: false, error: 'Failed to change password' });
    }
  });

  return router;
}
