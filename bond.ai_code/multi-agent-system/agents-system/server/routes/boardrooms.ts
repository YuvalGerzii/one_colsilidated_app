import { Router, Response } from 'express';
import { Pool } from 'pg';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createBoardRoomRoutes(pool: Pool): Router {
  const router = Router();

  // GET /api/boardrooms - Get all predefined board rooms
  router.get('/', async (req, res: Response) => {
    try {
      const result = await pool.query(
        `SELECT
          br.id, br.name, br.description, br.focus_sectors as "focusSectors",
          br.decision_style as "decisionStyle", br.consensus_threshold as "consensusThreshold",
          json_agg(json_build_object(
            'agentId', ba.id,
            'agentKey', ba.agent_key,
            'name', ba.name,
            'votingWeight', brm.voting_weight,
            'avatarUrl', ba.avatar_url
          ) ORDER BY ba.sort_order) as members
        FROM board_rooms br
        JOIN board_room_members brm ON br.id = brm.board_room_id
        JOIN behavior_agents ba ON brm.agent_id = ba.id
        WHERE br.is_predefined = true AND br.is_active = true
        GROUP BY br.id, br.name, br.description, br.focus_sectors,
                 br.decision_style, br.consensus_threshold
        ORDER BY br.created_at`
      );

      res.json({
        success: true,
        boardRooms: result.rows,
      });
    } catch (error) {
      console.error('Error fetching board rooms:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch board rooms' });
    }
  });

  // GET /api/boardrooms/my-boards - Get user's custom board rooms (requires auth)
  router.get('/my-boards', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          br.id, br.name, br.description, br.focus_sectors as "focusSectors",
          br.decision_style as "decisionStyle", br.consensus_threshold as "consensusThreshold",
          br.created_at as "createdAt",
          json_agg(json_build_object(
            'agentId', ba.id,
            'agentKey', ba.agent_key,
            'name', ba.name,
            'votingWeight', brm.voting_weight,
            'avatarUrl', ba.avatar_url
          ) ORDER BY ba.sort_order) as members
        FROM board_rooms br
        JOIN board_room_members brm ON br.id = brm.board_room_id
        JOIN behavior_agents ba ON brm.agent_id = ba.id
        WHERE br.user_id = $1 AND br.is_active = true
        GROUP BY br.id
        ORDER BY br.created_at DESC`,
        [userId]
      );

      res.json({
        success: true,
        boardRooms: result.rows,
      });
    } catch (error) {
      console.error('Error fetching custom board rooms:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch custom board rooms' });
    }
  });

  // GET /api/boardrooms/:id - Get specific board room
  router.get('/:id', async (req, res: Response) => {
    try {
      const { id } = req.params;

      const result = await pool.query(
        `SELECT
          br.id, br.name, br.description, br.focus_sectors as "focusSectors",
          br.decision_style as "decisionStyle", br.consensus_threshold as "consensusThreshold",
          br.is_predefined as "isPredefined",
          json_agg(json_build_object(
            'agentId', ba.id,
            'agentKey', ba.agent_key,
            'name', ba.name,
            'title', ba.title,
            'votingWeight', brm.voting_weight,
            'avatarUrl', ba.avatar_url
          ) ORDER BY ba.sort_order) as members
        FROM board_rooms br
        JOIN board_room_members brm ON br.id = brm.board_room_id
        JOIN behavior_agents ba ON brm.agent_id = ba.id
        WHERE br.id = $1 AND br.is_active = true
        GROUP BY br.id`,
        [id]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Board room not found' });
        return;
      }

      res.json({
        success: true,
        boardRoom: result.rows[0],
      });
    } catch (error) {
      console.error('Error fetching board room:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch board room' });
    }
  });

  // POST /api/boardrooms - Create custom board room (requires auth)
  router.post('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    const client = await pool.connect();

    try {
      const userId = req.user!.userId;
      const {
        name,
        description,
        focusSectors,
        decisionStyle,
        consensusThreshold,
        members, // Array of { agentKey: string, votingWeight: number }
      } = req.body;

      // Validation
      if (!name || !members || members.length === 0) {
        res.status(400).json({
          success: false,
          error: 'Name and at least one member are required',
        });
        return;
      }

      await client.query('BEGIN');

      // Create board room
      const boardResult = await client.query(
        `INSERT INTO board_rooms (
          user_id, name, description, focus_sectors,
          decision_style, consensus_threshold, is_predefined
        )
        VALUES ($1, $2, $3, $4, $5, $6, false)
        RETURNING id`,
        [
          userId,
          name,
          description || null,
          focusSectors || [],
          decisionStyle || 'majority',
          consensusThreshold || 0.6,
        ]
      );

      const boardRoomId = boardResult.rows[0].id;

      // Add members
      for (const member of members) {
        const agentResult = await client.query(
          'SELECT id FROM behavior_agents WHERE agent_key = $1',
          [member.agentKey]
        );

        if (agentResult.rows.length === 0) {
          throw new Error(`Agent ${member.agentKey} not found`);
        }

        await client.query(
          `INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
          VALUES ($1, $2, $3)`,
          [boardRoomId, agentResult.rows[0].id, member.votingWeight || 1.0]
        );
      }

      await client.query('COMMIT');

      res.status(201).json({
        success: true,
        boardRoomId,
        message: 'Custom board room created successfully',
      });
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error creating board room:', error);
      res.status(500).json({ success: false, error: 'Failed to create board room' });
    } finally {
      client.release();
    }
  });

  // PUT /api/boardrooms/:id - Update custom board room (requires auth)
  router.put('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    const client = await pool.connect();

    try {
      const { id } = req.params;
      const userId = req.user!.userId;
      const {
        name,
        description,
        focusSectors,
        decisionStyle,
        consensusThreshold,
        members,
      } = req.body;

      // Check ownership
      const ownerCheck = await client.query(
        'SELECT id FROM board_rooms WHERE id = $1 AND user_id = $2 AND is_predefined = false',
        [id, userId]
      );

      if (ownerCheck.rows.length === 0) {
        res.status(404).json({
          success: false,
          error: 'Board room not found or you do not have permission to update it',
        });
        return;
      }

      await client.query('BEGIN');

      // Update board room
      await client.query(
        `UPDATE board_rooms
        SET name = $1, description = $2, focus_sectors = $3,
            decision_style = $4, consensus_threshold = $5
        WHERE id = $6`,
        [name, description, focusSectors, decisionStyle, consensusThreshold, id]
      );

      // Update members if provided
      if (members) {
        // Delete existing members
        await client.query('DELETE FROM board_room_members WHERE board_room_id = $1', [id]);

        // Add new members
        for (const member of members) {
          const agentResult = await client.query(
            'SELECT id FROM behavior_agents WHERE agent_key = $1',
            [member.agentKey]
          );

          if (agentResult.rows.length > 0) {
            await client.query(
              `INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
              VALUES ($1, $2, $3)`,
              [id, agentResult.rows[0].id, member.votingWeight || 1.0]
            );
          }
        }
      }

      await client.query('COMMIT');

      res.json({
        success: true,
        message: 'Board room updated successfully',
      });
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error updating board room:', error);
      res.status(500).json({ success: false, error: 'Failed to update board room' });
    } finally {
      client.release();
    }
  });

  // DELETE /api/boardrooms/:id - Delete custom board room (requires auth)
  router.delete('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      // Soft delete by setting is_active to false
      const result = await pool.query(
        `UPDATE board_rooms
        SET is_active = false
        WHERE id = $1 AND user_id = $2 AND is_predefined = false
        RETURNING id`,
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({
          success: false,
          error: 'Board room not found or you do not have permission to delete it',
        });
        return;
      }

      res.json({
        success: true,
        message: 'Board room deleted successfully',
      });
    } catch (error) {
      console.error('Error deleting board room:', error);
      res.status(500).json({ success: false, error: 'Failed to delete board room' });
    }
  });

  return router;
}
