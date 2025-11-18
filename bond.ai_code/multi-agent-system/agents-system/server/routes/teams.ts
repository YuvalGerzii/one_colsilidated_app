import { Router, Response } from 'express';
import { Pool } from 'pg';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createTeamRoutes(pool: Pool): Router {
  const router = Router();

  // POST /api/teams - Create a new team (requires auth)
  router.post('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { name, description, subscriptionTier = 'free' } = req.body;

      if (!name) {
        res.status(400).json({ success: false, error: 'Team name is required' });
        return;
      }

      const result = await pool.query(
        `INSERT INTO teams (name, description, owner_id, subscription_tier)
        VALUES ($1, $2, $3, $4)
        RETURNING id, name, description, subscription_tier as "subscriptionTier", created_at as "createdAt"`,
        [name, description || null, userId, subscriptionTier]
      );

      // Add owner as team member with owner role
      await pool.query(
        `INSERT INTO team_members (team_id, user_id, role, permissions)
        VALUES ($1, $2, 'owner', '{"all": true}'::jsonb)`,
        [result.rows[0].id, userId]
      );

      res.status(201).json({
        success: true,
        team: result.rows[0],
      });
    } catch (error) {
      console.error('Error creating team:', error);
      res.status(500).json({ success: false, error: 'Failed to create team' });
    }
  });

  // GET /api/teams - Get user's teams (requires auth)
  router.get('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          t.id,
          t.name,
          t.description,
          t.subscription_tier as "subscriptionTier",
          t.created_at as "createdAt",
          tm.role as "userRole",
          json_build_object(
            'id', owner.id,
            'email', owner.email,
            'fullName', owner.full_name
          ) as owner,
          (
            SELECT COUNT(*)::int
            FROM team_members
            WHERE team_id = t.id
          ) as "memberCount"
        FROM teams t
        JOIN team_members tm ON t.id = tm.team_id
        JOIN users owner ON t.owner_id = owner.id
        WHERE tm.user_id = $1 AND t.is_active = true
        ORDER BY t.created_at DESC`,
        [userId]
      );

      res.json({
        success: true,
        teams: result.rows,
      });
    } catch (error) {
      console.error('Error fetching teams:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch teams' });
    }
  });

  // GET /api/teams/:id - Get team details (requires auth)
  router.get('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      // Check membership
      const memberCheck = await pool.query(
        'SELECT role, permissions FROM team_members WHERE team_id = $1 AND user_id = $2',
        [id, userId]
      );

      if (memberCheck.rows.length === 0) {
        res.status(403).json({ success: false, error: 'Access denied' });
        return;
      }

      // Get team details
      const teamResult = await pool.query(
        `SELECT
          t.id,
          t.name,
          t.description,
          t.subscription_tier as "subscriptionTier",
          t.created_at as "createdAt",
          json_build_object(
            'id', owner.id,
            'email', owner.email,
            'fullName', owner.full_name
          ) as owner
        FROM teams t
        JOIN users owner ON t.owner_id = owner.id
        WHERE t.id = $1 AND t.is_active = true`,
        [id]
      );

      if (teamResult.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Team not found' });
        return;
      }

      // Get members
      const membersResult = await pool.query(
        `SELECT
          tm.id,
          tm.role,
          tm.permissions,
          tm.joined_at as "joinedAt",
          json_build_object(
            'id', u.id,
            'email', u.email,
            'fullName', u.full_name
          ) as user
        FROM team_members tm
        JOIN users u ON tm.user_id = u.id
        WHERE tm.team_id = $1
        ORDER BY tm.joined_at ASC`,
        [id]
      );

      res.json({
        success: true,
        team: {
          ...teamResult.rows[0],
          members: membersResult.rows,
          userRole: memberCheck.rows[0].role,
        },
      });
    } catch (error) {
      console.error('Error fetching team details:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch team details' });
    }
  });

  // POST /api/teams/:id/members - Add team member (requires auth + admin)
  router.post('/:id/members', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;
      const { email, role = 'member' } = req.body;

      if (!email) {
        res.status(400).json({ success: false, error: 'Email is required' });
        return;
      }

      // Check if requester has admin/owner privileges
      const requesterCheck = await pool.query(
        'SELECT role FROM team_members WHERE team_id = $1 AND user_id = $2',
        [id, userId]
      );

      if (
        requesterCheck.rows.length === 0 ||
        !['owner', 'admin'].includes(requesterCheck.rows[0].role)
      ) {
        res.status(403).json({ success: false, error: 'Insufficient permissions' });
        return;
      }

      // Find user by email
      const userResult = await pool.query(
        'SELECT id, email, full_name as "fullName" FROM users WHERE email = $1',
        [email]
      );

      if (userResult.rows.length === 0) {
        res.status(404).json({ success: false, error: 'User not found' });
        return;
      }

      const newMemberId = userResult.rows[0].id;

      // Check if already a member
      const existingMember = await pool.query(
        'SELECT id FROM team_members WHERE team_id = $1 AND user_id = $2',
        [id, newMemberId]
      );

      if (existingMember.rows.length > 0) {
        res.status(409).json({ success: false, error: 'User is already a team member' });
        return;
      }

      // Add member
      const result = await pool.query(
        `INSERT INTO team_members (team_id, user_id, role)
        VALUES ($1, $2, $3)
        RETURNING id, role, joined_at as "joinedAt"`,
        [id, newMemberId, role]
      );

      res.status(201).json({
        success: true,
        member: {
          ...result.rows[0],
          user: userResult.rows[0],
        },
      });
    } catch (error) {
      console.error('Error adding team member:', error);
      res.status(500).json({ success: false, error: 'Failed to add team member' });
    }
  });

  // PUT /api/teams/:id/members/:memberId - Update member role (requires auth + admin)
  router.put('/:id/members/:memberId', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id, memberId } = req.params;
      const userId = req.user!.userId;
      const { role, permissions } = req.body;

      // Check if requester has owner privileges
      const requesterCheck = await pool.query(
        'SELECT role FROM team_members WHERE team_id = $1 AND user_id = $2',
        [id, userId]
      );

      if (requesterCheck.rows.length === 0 || requesterCheck.rows[0].role !== 'owner') {
        res.status(403).json({ success: false, error: 'Only team owners can update member roles' });
        return;
      }

      // Can't change owner's own role
      const targetMember = await pool.query(
        'SELECT user_id FROM team_members WHERE id = $1 AND team_id = $2',
        [memberId, id]
      );

      if (targetMember.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Member not found' });
        return;
      }

      if (targetMember.rows[0].user_id === userId) {
        res.status(400).json({ success: false, error: 'Cannot change your own role' });
        return;
      }

      // Update member
      const result = await pool.query(
        `UPDATE team_members
        SET role = COALESCE($1, role),
            permissions = COALESCE($2, permissions)
        WHERE id = $3 AND team_id = $4
        RETURNING id, role, permissions`,
        [role, permissions ? JSON.stringify(permissions) : null, memberId, id]
      );

      res.json({
        success: true,
        member: result.rows[0],
      });
    } catch (error) {
      console.error('Error updating team member:', error);
      res.status(500).json({ success: false, error: 'Failed to update team member' });
    }
  });

  // DELETE /api/teams/:id/members/:memberId - Remove team member (requires auth + admin)
  router.delete('/:id/members/:memberId', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id, memberId } = req.params;
      const userId = req.user!.userId;

      // Check if requester has admin/owner privileges
      const requesterCheck = await pool.query(
        'SELECT role FROM team_members WHERE team_id = $1 AND user_id = $2',
        [id, userId]
      );

      if (
        requesterCheck.rows.length === 0 ||
        !['owner', 'admin'].includes(requesterCheck.rows[0].role)
      ) {
        res.status(403).json({ success: false, error: 'Insufficient permissions' });
        return;
      }

      // Can't remove owner
      const targetMember = await pool.query(
        'SELECT user_id, role FROM team_members WHERE id = $1 AND team_id = $2',
        [memberId, id]
      );

      if (targetMember.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Member not found' });
        return;
      }

      if (targetMember.rows[0].role === 'owner') {
        res.status(400).json({ success: false, error: 'Cannot remove team owner' });
        return;
      }

      // Remove member
      await pool.query('DELETE FROM team_members WHERE id = $1 AND team_id = $2', [memberId, id]);

      res.json({
        success: true,
        message: 'Team member removed successfully',
      });
    } catch (error) {
      console.error('Error removing team member:', error);
      res.status(500).json({ success: false, error: 'Failed to remove team member' });
    }
  });

  // DELETE /api/teams/:id - Delete team (requires auth + owner)
  router.delete('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      // Check if requester is owner
      const ownerCheck = await pool.query(
        'SELECT id FROM teams WHERE id = $1 AND owner_id = $2',
        [id, userId]
      );

      if (ownerCheck.rows.length === 0) {
        res.status(403).json({ success: false, error: 'Only team owner can delete the team' });
        return;
      }

      // Soft delete
      await pool.query('UPDATE teams SET is_active = false WHERE id = $1', [id]);

      res.json({
        success: true,
        message: 'Team deleted successfully',
      });
    } catch (error) {
      console.error('Error deleting team:', error);
      res.status(500).json({ success: false, error: 'Failed to delete team' });
    }
  });

  return router;
}
