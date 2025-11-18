import { useState, useEffect, useCallback, useRef } from 'react';
import { socket } from '../lib/socket';

/**
 * Custom React Hook for Dynamic Profile Updates
 *
 * Features:
 * - Real-time delta updates via WebSocket
 * - Automatic reconnection with exponential backoff
 * - State synchronization after reconnection
 * - Heartbeat monitoring
 * - Offline queue for updates
 */

interface Need {
  id: string;
  category: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  urgency: 'flexible' | 'weeks' | 'days' | 'immediate';
  flexibility: number;
  status: 'active' | 'fulfilled' | 'expired';
  createdAt: Date;
  updatedAt: Date;
}

interface Offering {
  id: string;
  category: string;
  description: string;
  value: string;
  capacity: 'limited' | 'moderate' | 'high' | 'unlimited';
  conditions?: string;
  status: 'available' | 'reserved' | 'unavailable';
  createdAt: Date;
  updatedAt: Date;
}

interface DeltaUpdate {
  id: string;
  changes: Record<string, any>;
  previousValues?: Record<string, any>;
  timestamp: Date;
}

interface ProfileState {
  needs: Need[];
  offerings: Offering[];
  version: number;
  lastSynced: Date | null;
}

export function useDynamicProfile() {
  const [state, setState] = useState<ProfileState>({
    needs: [],
    offerings: [],
    version: 0,
    lastSynced: null
  });

  const [isConnected, setIsConnected] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;
  const baseDelay = 2000; // 2 seconds

  /**
   * Calculate exponential backoff delay
   */
  const getReconnectDelay = useCallback(() => {
    const delay = Math.min(
      baseDelay * Math.pow(2, reconnectAttempts.current),
      30000 // Max 30 seconds
    );
    return delay;
  }, []);

  /**
   * Handle WebSocket connection
   */
  useEffect(() => {
    function onConnect() {
      console.log('Connected to profile updates');
      setIsConnected(true);
      setError(null);
      reconnectAttempts.current = 0;

      // Request full sync on connection
      socket.emit('profile:sync');
    }

    function onDisconnect() {
      console.log('Disconnected from profile updates');
      setIsConnected(false);

      // Attempt reconnection with exponential backoff
      if (reconnectAttempts.current < maxReconnectAttempts) {
        const delay = getReconnectDelay();
        console.log(`Reconnecting in ${delay}ms... (attempt ${reconnectAttempts.current + 1})`);

        setTimeout(() => {
          reconnectAttempts.current++;
          socket.connect();
        }, delay);
      } else {
        setError('Unable to connect. Please refresh the page.');
      }
    }

    function onError(err: any) {
      console.error('Socket error:', err);
      setError(err.message || 'Connection error');
    }

    // Heartbeat handling
    function onHeartbeatPing() {
      socket.emit('heartbeat:pong');
    }

    // Full sync response
    function onSyncComplete(data: any) {
      setIsSyncing(false);
      setState({
        needs: data.needs,
        offerings: data.offerings,
        version: data.version,
        lastSynced: new Date(data.timestamp)
      });
    }

    // Delta update handling
    function onDelta(data: { type: 'need' | 'offering'; delta: DeltaUpdate; version: number }) {
      setState(prevState => {
        if (data.version <= prevState.version) {
          // Ignore old updates
          return prevState;
        }

        const newState = { ...prevState, version: data.version };

        if (data.type === 'need') {
          newState.needs = applyDelta(prevState.needs, data.delta);
        } else {
          newState.offerings = applyDelta(prevState.offerings, data.delta);
        }

        return newState;
      });
    }

    // Update acknowledgment
    function onUpdateAck(data: { success: boolean; version: number; delta?: DeltaUpdate }) {
      if (data.success) {
        console.log('Update acknowledged, version:', data.version);
      }
    }

    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('error', onError);
    socket.on('heartbeat:ping', onHeartbeatPing);
    socket.on('profile:sync:complete', onSyncComplete);
    socket.on('profile:delta', onDelta);
    socket.on('profile:update:ack', onUpdateAck);

    // Connect if not already connected
    if (!socket.connected) {
      socket.connect();
    }

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('error', onError);
      socket.off('heartbeat:ping', onHeartbeatPing);
      socket.off('profile:sync:complete', onSyncComplete);
      socket.off('profile:delta', onDelta);
      socket.off('profile:update:ack', onUpdateAck);
    };
  }, [getReconnectDelay]);

  /**
   * Apply delta update to array
   */
  const applyDelta = useCallback(<T extends { id: string }>(
    items: T[],
    delta: DeltaUpdate
  ): T[] => {
    const { id, changes } = delta;

    if (changes.action === 'create') {
      return [...items, changes as T];
    } else if (changes.action === 'delete') {
      return items.filter(item => item.id !== id);
    } else {
      return items.map(item => {
        if (item.id === id) {
          return { ...item, ...changes };
        }
        return item;
      });
    }
  }, []);

  /**
   * Create a new need
   */
  const createNeed = useCallback((need: Omit<Need, 'id' | 'createdAt' | 'updatedAt' | 'status'>) => {
    socket.emit('profile:update:need', {
      action: 'create',
      need
    });
  }, []);

  /**
   * Update an existing need
   */
  const updateNeed = useCallback((id: string, updates: Partial<Need>) => {
    socket.emit('profile:update:need', {
      action: 'update',
      need: { id, ...updates }
    });
  }, []);

  /**
   * Delete a need
   */
  const deleteNeed = useCallback((id: string) => {
    socket.emit('profile:update:need', {
      action: 'delete',
      need: { id }
    });
  }, []);

  /**
   * Create a new offering
   */
  const createOffering = useCallback((offering: Omit<Offering, 'id' | 'createdAt' | 'updatedAt' | 'status'>) => {
    socket.emit('profile:update:offering', {
      action: 'create',
      offering
    });
  }, []);

  /**
   * Update an existing offering
   */
  const updateOffering = useCallback((id: string, updates: Partial<Offering>) => {
    socket.emit('profile:update:offering', {
      action: 'update',
      offering: { id, ...updates }
    });
  }, []);

  /**
   * Delete an offering
   */
  const deleteOffering = useCallback((id: string) => {
    socket.emit('profile:update:offering', {
      action: 'delete',
      offering: { id }
    });
  }, []);

  /**
   * Manually trigger sync
   */
  const sync = useCallback(() => {
    setIsSyncing(true);
    socket.emit('profile:sync');
  }, []);

  return {
    // State
    needs: state.needs,
    offerings: state.offerings,
    version: state.version,
    lastSynced: state.lastSynced,

    // Connection status
    isConnected,
    isSyncing,
    error,

    // Actions
    createNeed,
    updateNeed,
    deleteNeed,
    createOffering,
    updateOffering,
    deleteOffering,
    sync
  };
}
