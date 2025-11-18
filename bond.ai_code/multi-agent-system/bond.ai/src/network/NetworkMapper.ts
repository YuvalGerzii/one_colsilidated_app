/**
 * Network Mapping Module
 * Imports and aggregates connections, builds professional graph with relationship indicators
 */

import {
  Contact,
  Connection,
  NetworkGraph,
  NetworkSource,
  RelationshipType,
  ConnectionPath
} from '../types';

export class NetworkMapper {
  private contacts: Map<string, Contact>;
  private connections: Map<string, Connection>;
  private degreeMap: Map<string, number>;
  private userId: string;

  constructor(userId: string) {
    this.userId = userId;
    this.contacts = new Map();
    this.connections = new Map();
    this.degreeMap = new Map();

    // User is always degree 0
    this.degreeMap.set(userId, 0);
  }

  /**
   * Import contacts from multiple sources
   */
  async importFromSource(source: NetworkSource): Promise<{
    contactsImported: number;
    connectionsCreated: number;
  }> {
    const stats = { contactsImported: 0, connectionsCreated: 0 };

    switch (source.type) {
      case 'csv':
        const result = await this.importFromCSV(source.config?.filePath);
        stats.contactsImported += result.contactsImported;
        stats.connectionsCreated += result.connectionsCreated;
        break;

      case 'manual':
        // Manual import handled separately
        break;

      // Add more source types as needed
      default:
        throw new Error(`Unsupported source type: ${source.type}`);
    }

    return stats;
  }

  /**
   * Import contacts from CSV file
   */
  private async importFromCSV(filePath: string): Promise<{
    contactsImported: number;
    connectionsCreated: number;
  }> {
    // Placeholder for CSV import logic
    // In real implementation, would parse CSV and create contacts
    return { contactsImported: 0, connectionsCreated: 0 };
  }

  /**
   * Add a contact to the network
   */
  addContact(contact: Contact): void {
    this.contacts.set(contact.id, contact);
  }

  /**
   * Add a connection between two contacts
   */
  addConnection(connection: Connection): void {
    this.connections.set(connection.id, connection);

    // Update degree map
    this.updateDegreeMap();
  }

  /**
   * Get contact by ID
   */
  getContact(contactId: string): Contact | undefined {
    return this.contacts.get(contactId);
  }

  /**
   * Get all contacts at a specific degree of separation
   */
  getContactsByDegree(degree: number): Contact[] {
    const contactIds = Array.from(this.degreeMap.entries())
      .filter(([_, d]) => d === degree)
      .map(([id, _]) => id);

    return contactIds
      .map(id => this.contacts.get(id))
      .filter(c => c !== undefined) as Contact[];
  }

  /**
   * Get degree of separation for a contact
   */
  getDegreeOfSeparation(contactId: string): number | undefined {
    return this.degreeMap.get(contactId);
  }

  /**
   * Build network graph up to specified degree
   */
  buildNetworkGraph(maxDegree: number = 3): NetworkGraph {
    this.updateDegreeMap(maxDegree);

    return {
      contacts: new Map(this.contacts),
      connections: new Map(this.connections),
      degreeMap: new Map(this.degreeMap)
    };
  }

  /**
   * Update degree map using BFS
   */
  private updateDegreeMap(maxDegree: number = 3): void {
    const queue: Array<{ contactId: string; degree: number }> = [
      { contactId: this.userId, degree: 0 }
    ];
    const visited = new Set<string>([this.userId]);

    while (queue.length > 0) {
      const { contactId, degree } = queue.shift()!;

      if (degree >= maxDegree) continue;

      // Find all connections for this contact
      const contactConnections = Array.from(this.connections.values())
        .filter(c => c.fromContactId === contactId || c.toContactId === contactId);

      for (const connection of contactConnections) {
        const neighborId = connection.fromContactId === contactId
          ? connection.toContactId
          : connection.fromContactId;

        if (!visited.has(neighborId)) {
          visited.add(neighborId);
          this.degreeMap.set(neighborId, degree + 1);
          queue.push({ contactId: neighborId, degree: degree + 1 });
        }
      }
    }
  }

  /**
   * Find all connection paths between two contacts
   */
  findConnectionPaths(
    fromContactId: string,
    toContactId: string,
    maxDepth: number = 3
  ): ConnectionPath[] {
    const paths: ConnectionPath[] = [];
    const visited = new Set<string>();

    const dfs = (
      currentId: string,
      targetId: string,
      currentPath: Contact[],
      currentConnections: Connection[],
      depth: number
    ) => {
      if (depth > maxDepth) return;
      if (currentId === targetId) {
        const trustScore = this.calculatePathTrustScore(currentConnections);
        const totalStrength = this.calculatePathStrength(currentConnections);

        paths.push({
          contacts: [...currentPath],
          connections: [...currentConnections],
          totalStrength,
          trustScore
        });
        return;
      }

      visited.add(currentId);

      const connections = Array.from(this.connections.values())
        .filter(c => c.fromContactId === currentId || c.toContactId === currentId);

      for (const connection of connections) {
        const nextId = connection.fromContactId === currentId
          ? connection.toContactId
          : connection.fromContactId;

        if (!visited.has(nextId)) {
          const nextContact = this.contacts.get(nextId);
          if (nextContact) {
            currentPath.push(nextContact);
            currentConnections.push(connection);
            dfs(nextId, targetId, currentPath, currentConnections, depth + 1);
            currentPath.pop();
            currentConnections.pop();
          }
        }
      }

      visited.delete(currentId);
    };

    const startContact = this.contacts.get(fromContactId);
    if (startContact) {
      dfs(fromContactId, toContactId, [startContact], [], 0);
    }

    return paths.sort((a, b) => b.trustScore - a.trustScore);
  }

  /**
   * Find shortest path between two contacts
   */
  findShortestPath(fromContactId: string, toContactId: string): ConnectionPath | null {
    const paths = this.findConnectionPaths(fromContactId, toContactId);
    if (paths.length === 0) return null;

    return paths.reduce((shortest, current) =>
      current.contacts.length < shortest.contacts.length ? current : shortest
    );
  }

  /**
   * Calculate relationship strength between two contacts
   */
  calculateRelationshipStrength(connection: Connection): number {
    let strength = connection.strength || 0.5;

    // Adjust based on interaction frequency
    if (connection.interactionFrequency) {
      strength *= (1 + Math.min(connection.interactionFrequency / 10, 0.5));
    }

    // Adjust based on last interaction recency
    if (connection.lastInteraction) {
      const daysSince = (Date.now() - connection.lastInteraction.getTime()) / (1000 * 60 * 60 * 24);
      const recencyFactor = Math.max(0, 1 - daysSince / 365);
      strength *= (0.7 + 0.3 * recencyFactor);
    }

    return Math.min(strength, 1);
  }

  /**
   * Calculate trust score for a connection path
   */
  private calculatePathTrustScore(connections: Connection[]): number {
    if (connections.length === 0) return 1;

    const trustLevels = connections.map(c => c.trustLevel || 0.5);
    const avgTrust = trustLevels.reduce((sum, t) => sum + t, 0) / trustLevels.length;

    // Decay trust over multiple hops
    const decayFactor = Math.pow(0.85, connections.length - 1);

    return avgTrust * decayFactor;
  }

  /**
   * Calculate total strength for a connection path
   */
  private calculatePathStrength(connections: Connection[]): number {
    if (connections.length === 0) return 1;

    const strengths = connections.map(c => this.calculateRelationshipStrength(c));

    // Product of strengths (weakest link matters)
    return strengths.reduce((product, s) => product * s, 1);
  }

  /**
   * Get network statistics
   */
  getNetworkStats(): {
    totalContacts: number;
    totalConnections: number;
    contactsByDegree: Record<number, number>;
    averageConnectionsPerContact: number;
  } {
    const contactsByDegree: Record<number, number> = {};

    for (const degree of this.degreeMap.values()) {
      contactsByDegree[degree] = (contactsByDegree[degree] || 0) + 1;
    }

    return {
      totalContacts: this.contacts.size,
      totalConnections: this.connections.size,
      contactsByDegree,
      averageConnectionsPerContact: this.connections.size / Math.max(this.contacts.size, 1)
    };
  }

  /**
   * Get all contacts
   */
  getAllContacts(): Contact[] {
    return Array.from(this.contacts.values());
  }

  /**
   * Get all connections
   */
  getAllConnections(): Connection[] {
    return Array.from(this.connections.values());
  }

  /**
   * Get direct connections for a contact
   */
  getDirectConnections(contactId: string): Connection[] {
    return Array.from(this.connections.values())
      .filter(c => c.fromContactId === contactId || c.toContactId === contactId);
  }

  /**
   * Get contacts directly connected to a contact
   */
  getDirectContacts(contactId: string): Contact[] {
    const connections = this.getDirectConnections(contactId);
    const contactIds = connections.map(c =>
      c.fromContactId === contactId ? c.toContactId : c.fromContactId
    );

    return contactIds
      .map(id => this.contacts.get(id))
      .filter(c => c !== undefined) as Contact[];
  }
}
