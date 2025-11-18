/**
 * LinkedIn OAuth Integration Service
 * Import connections and profile data from LinkedIn
 */

import axios, { AxiosInstance } from 'axios';
import { getDb } from '../database/connection';

export interface LinkedInConfig {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
}

export interface LinkedInProfile {
  id: string;
  firstName: string;
  lastName: string;
  email?: string;
  headline?: string;
  profilePicture?: string;
  industry?: string;
  location?: string;
}

export interface LinkedInConnection {
  id: string;
  firstName: string;
  lastName: string;
  headline?: string;
  industry?: string;
  company?: string;
  position?: string;
}

export class LinkedInService {
  private config: LinkedInConfig;
  private client: AxiosInstance;

  constructor(config?: Partial<LinkedInConfig>) {
    this.config = {
      clientId: config?.clientId || process.env.LINKEDIN_CLIENT_ID || '',
      clientSecret: config?.clientSecret || process.env.LINKEDIN_CLIENT_SECRET || '',
      redirectUri: config?.redirectUri || process.env.LINKEDIN_REDIRECT_URI || 'http://localhost:3000/api/linkedin/callback',
    };

    this.client = axios.create({
      baseURL: 'https://api.linkedin.com/v2',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!this.config.clientId || !this.config.clientSecret) {
      console.warn('⚠ LinkedIn OAuth not configured. Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET environment variables.');
    }
  }

  /**
   * Get authorization URL for OAuth flow
   */
  getAuthorizationUrl(state?: string): string {
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: this.config.clientId,
      redirect_uri: this.config.redirectUri,
      scope: 'r_liteprofile r_emailaddress w_member_social',
      state: state || Math.random().toString(36).substring(7),
    });

    return `https://www.linkedin.com/oauth/v2/authorization?${params.toString()}`;
  }

  /**
   * Exchange authorization code for access token
   */
  async getAccessToken(code: string): Promise<{
    accessToken: string;
    expiresIn: number;
    refreshToken?: string;
  }> {
    try {
      const response = await axios.post(
        'https://www.linkedin.com/oauth/v2/accessToken',
        new URLSearchParams({
          grant_type: 'authorization_code',
          code,
          client_id: this.config.clientId,
          client_secret: this.config.clientSecret,
          redirect_uri: this.config.redirectUri,
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      return {
        accessToken: response.data.access_token,
        expiresIn: response.data.expires_in,
        refreshToken: response.data.refresh_token,
      };
    } catch (error: any) {
      console.error('LinkedIn token exchange error:', error.response?.data || error.message);
      throw new Error('Failed to exchange authorization code for access token');
    }
  }

  /**
   * Get user's LinkedIn profile
   */
  async getProfile(accessToken: string): Promise<LinkedInProfile> {
    try {
      const response = await this.client.get('/me', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const profileData = response.data;

      // Get email address (separate endpoint)
      let email: string | undefined;
      try {
        const emailResponse = await this.client.get('/emailAddress?q=members&projection=(elements*(handle~))', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        email = emailResponse.data.elements?.[0]?.['handle~']?.emailAddress;
      } catch (error) {
        console.warn('Could not fetch email address from LinkedIn');
      }

      return {
        id: profileData.id,
        firstName: profileData.localizedFirstName || profileData.firstName?.localized?.en_US || '',
        lastName: profileData.localizedLastName || profileData.lastName?.localized?.en_US || '',
        email,
        headline: profileData.headline?.localized?.en_US,
        profilePicture: profileData.profilePicture?.['displayImage~']?.elements?.[0]?.identifiers?.[0]?.identifier,
        industry: profileData.industryName,
        location: profileData.location?.name,
      };
    } catch (error: any) {
      console.error('LinkedIn profile fetch error:', error.response?.data || error.message);
      throw new Error('Failed to fetch LinkedIn profile');
    }
  }

  /**
   * Get user's connections
   * Note: LinkedIn API has restrictions on connection data access
   * This is a simplified version - in production, you may need to use LinkedIn's People Search API or other methods
   */
  async getConnections(accessToken: string): Promise<LinkedInConnection[]> {
    try {
      // Note: LinkedIn deprecated direct connections API
      // This is a placeholder - you would need to implement alternative methods:
      // 1. Use LinkedIn's People Search API
      // 2. Use scraping (against ToS)
      // 3. Use LinkedIn Marketing API if you have access
      // 4. Use LinkedIn's official Connections API if you have partner access

      console.warn('LinkedIn connections API is restricted. Implement alternative method.');

      // For demo purposes, return empty array
      return [];

      // If you have access to connections API:
      // const response = await this.client.get('/connections', {
      //   headers: {
      //     Authorization: `Bearer ${accessToken}`,
      //   },
      //   params: {
      //     start: 0,
      //     count: 500,
      //   },
      // });
      //
      // return response.data.values?.map((conn: any) => ({
      //   id: conn.id,
      //   firstName: conn.firstName,
      //   lastName: conn.lastName,
      //   headline: conn.headline,
      //   industry: conn.industry,
      //   company: conn.company?.name,
      //   position: conn.positions?.values?.[0]?.title,
      // })) || [];
    } catch (error: any) {
      console.error('LinkedIn connections fetch error:', error.response?.data || error.message);
      throw new Error('Failed to fetch LinkedIn connections');
    }
  }

  /**
   * Store OAuth token in database
   */
  async storeToken(userId: string, tokenData: {
    accessToken: string;
    refreshToken?: string;
    expiresIn: number;
  }): Promise<void> {
    const db = getDb();

    const expiresAt = new Date(Date.now() + tokenData.expiresIn * 1000);

    await db.query(
      `INSERT INTO oauth_tokens (user_id, provider, access_token, refresh_token, token_type, expires_at, created_at)
       VALUES ($1, 'linkedin', $2, $3, 'Bearer', $4, NOW())
       ON CONFLICT (user_id, provider) DO UPDATE
       SET access_token = $2, refresh_token = $3, expires_at = $4, updated_at = NOW()`,
      [userId, tokenData.accessToken, tokenData.refreshToken, expiresAt]
    );
  }

  /**
   * Get stored token from database
   */
  async getToken(userId: string): Promise<{
    accessToken: string;
    refreshToken?: string;
    expiresAt: Date;
  } | null> {
    const db = getDb();

    const result = await db.queryOne<{
      access_token: string;
      refresh_token?: string;
      expires_at: Date;
    }>(
      `SELECT access_token, refresh_token, expires_at
       FROM oauth_tokens
       WHERE user_id = $1 AND provider = 'linkedin'`,
      [userId]
    );

    if (!result) return null;

    return {
      accessToken: result.access_token,
      refreshToken: result.refresh_token,
      expiresAt: result.expires_at,
    };
  }

  /**
   * Check if token is valid (not expired)
   */
  async isTokenValid(userId: string): Promise<boolean> {
    const token = await this.getToken(userId);

    if (!token) return false;

    return new Date() < new Date(token.expiresAt);
  }

  /**
   * Import LinkedIn profile to Bond.AI
   */
  async importProfile(userId: string, profile: LinkedInProfile): Promise<string> {
    const db = getDb();

    // Create or update contact
    const contact = await db.queryOne<{ id: string }>(
      `INSERT INTO contacts (
        user_id, name, email, title, industry, location,
        source, external_id, social_profiles, created_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, 'linkedin', $7, $8, NOW())
      ON CONFLICT (user_id, source, external_id) DO UPDATE
      SET
        name = $2,
        email = $3,
        title = $4,
        industry = $5,
        location = $6,
        social_profiles = $8,
        updated_at = NOW()
      RETURNING id`,
      [
        userId,
        `${profile.firstName} ${profile.lastName}`,
        profile.email,
        profile.headline,
        profile.industry,
        profile.location,
        profile.id,
        JSON.stringify({
          linkedin: `https://linkedin.com/in/${profile.id}`,
          profilePicture: profile.profilePicture,
        }),
      ]
    );

    return contact!.id;
  }

  /**
   * Import LinkedIn connections
   */
  async importConnections(
    userId: string,
    connections: LinkedInConnection[]
  ): Promise<{ imported: number; skipped: number }> {
    const db = getDb();
    let imported = 0;
    let skipped = 0;

    for (const conn of connections) {
      try {
        // Create contact
        await db.query(
          `INSERT INTO contacts (
            user_id, name, title, industry, company,
            source, external_id, created_at
          )
          VALUES ($1, $2, $3, $4, $5, 'linkedin', $6, NOW())
          ON CONFLICT (user_id, source, external_id) DO UPDATE
          SET
            name = $2,
            title = $3,
            industry = $4,
            company = $5,
            updated_at = NOW()`,
          [
            userId,
            `${conn.firstName} ${conn.lastName}`,
            conn.headline || conn.position,
            conn.industry,
            conn.company,
            conn.id,
          ]
        );

        imported++;
      } catch (error) {
        console.error('Failed to import connection:', conn.id, error);
        skipped++;
      }
    }

    return { imported, skipped };
  }

  /**
   * Revoke access (delete token)
   */
  async revokeAccess(userId: string): Promise<void> {
    const db = getDb();

    await db.query(
      `DELETE FROM oauth_tokens WHERE user_id = $1 AND provider = 'linkedin'`,
      [userId]
    );
  }
}

// Singleton instance
let linkedInServiceInstance: LinkedInService | null = null;

/**
 * Get LinkedIn service instance
 */
export function getLinkedInService(): LinkedInService {
  if (!linkedInServiceInstance) {
    linkedInServiceInstance = new LinkedInService();
  }
  return linkedInServiceInstance;
}
