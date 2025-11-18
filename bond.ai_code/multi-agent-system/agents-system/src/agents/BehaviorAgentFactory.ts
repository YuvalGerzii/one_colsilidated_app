/**
 * Behavior Agent Factory
 *
 * Factory for creating behavior analysis agents and pre-configured board rooms.
 * Makes it easy to instantiate agents and create specialized advisory boards.
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import { ElonMuskBehaviorAgent } from './ElonMuskBehaviorAgent';
import { SteveJobsBehaviorAgent } from './SteveJobsBehaviorAgent';
import { MarkZuckerbergBehaviorAgent } from './MarkZuckerbergBehaviorAgent';
import { DonaldTrumpBehaviorAgent } from './DonaldTrumpBehaviorAgent';
import { LarryFinkBehaviorAgent } from './LarryFinkBehaviorAgent';
import { JeffBezosBehaviorAgent } from './JeffBezosBehaviorAgent';
import { SamZellBehaviorAgent } from './SamZellBehaviorAgent';
import { DonaldBrenBehaviorAgent } from './DonaldBrenBehaviorAgent';
import { BoardRoomAgent } from './BoardRoomAgent';
import { IBehaviorAgent, BoardRoomConfig, BusinessSector } from './BehaviorAgentTypes';

export class BehaviorAgentFactory {
  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Create individual agents
   */

  createElonMuskAgent(): ElonMuskBehaviorAgent {
    return new ElonMuskBehaviorAgent(this.pool, this.redis);
  }

  createSteveJobsAgent(): SteveJobsBehaviorAgent {
    return new SteveJobsBehaviorAgent(this.pool, this.redis);
  }

  createMarkZuckerbergAgent(): MarkZuckerbergBehaviorAgent {
    return new MarkZuckerbergBehaviorAgent(this.pool, this.redis);
  }

  createDonaldTrumpAgent(): DonaldTrumpBehaviorAgent {
    return new DonaldTrumpBehaviorAgent(this.pool, this.redis);
  }

  createLarryFinkAgent(): LarryFinkBehaviorAgent {
    return new LarryFinkBehaviorAgent(this.pool, this.redis);
  }

  createJeffBezosAgent(): JeffBezosBehaviorAgent {
    return new JeffBezosBehaviorAgent(this.pool, this.redis);
  }

  createSamZellAgent(): SamZellBehaviorAgent {
    return new SamZellBehaviorAgent(this.pool, this.redis);
  }

  createDonaldBrenAgent(): DonaldBrenBehaviorAgent {
    return new DonaldBrenBehaviorAgent(this.pool, this.redis);
  }

  /**
   * Create all agents
   */
  createAllAgents(): IBehaviorAgent[] {
    return [
      this.createElonMuskAgent(),
      this.createSteveJobsAgent(),
      this.createMarkZuckerbergAgent(),
      this.createDonaldTrumpAgent(),
      this.createLarryFinkAgent(),
      this.createJeffBezosAgent(),
      this.createSamZellAgent(),
      this.createDonaldBrenAgent(),
    ];
  }

  /**
   * Create board room agent
   */
  createBoardRoomAgent(): BoardRoomAgent {
    return new BoardRoomAgent(this.pool, this.redis);
  }

  /**
   * Create pre-configured board rooms
   */

  /**
   * Technology Innovation Board
   * Focus: Product development, innovation, technology strategy
   */
  createTechInnovationBoard(): { boardRoom: BoardRoomAgent; config: BoardRoomConfig } {
    const boardRoom = this.createBoardRoomAgent();

    const config = boardRoom.createAdHocBoardRoom(
      'Tech Innovation Board',
      [
        this.createElonMuskAgent(),
        this.createSteveJobsAgent(),
        this.createMarkZuckerbergAgent(),
        this.createJeffBezosAgent(),
      ],
      [BusinessSector.TECHNOLOGY, BusinessSector.E_COMMERCE, BusinessSector.SOCIAL_MEDIA],
      'majority'
    );

    return { boardRoom, config };
  }

  /**
   * Investment & Finance Board
   * Focus: Investment decisions, financial strategy, capital allocation
   */
  createInvestmentBoard(): { boardRoom: BoardRoomAgent; config: BoardRoomConfig } {
    const boardRoom = this.createBoardRoomAgent();

    const config = boardRoom.createAdHocBoardRoom(
      'Investment & Finance Board',
      [
        this.createLarryFinkAgent(),
        this.createSamZellAgent(),
        this.createDonaldBrenAgent(),
      ],
      [BusinessSector.FINANCE, BusinessSector.REAL_ESTATE],
      'weighted'
    );

    // Set voting weights
    config.votingWeights = new Map([
      ['Larry Fink', 0.4], // Higher weight for primary finance expert
      ['Sam Zell', 0.3],
      ['Donald Bren', 0.3],
    ]);

    return { boardRoom, config };
  }

  /**
   * Real Estate Development Board
   * Focus: Real estate strategy, development, property investment
   */
  createRealEstateBoard(): { boardRoom: BoardRoomAgent; config: BoardRoomConfig } {
    const boardRoom = this.createBoardRoomAgent();

    const config = boardRoom.createAdHocBoardRoom(
      'Real Estate Development Board',
      [
        this.createSamZellAgent(),
        this.createDonaldBrenAgent(),
        this.createDonaldTrumpAgent(),
      ],
      [BusinessSector.REAL_ESTATE],
      'majority'
    );

    return { boardRoom, config };
  }

  /**
   * Negotiation & Deal Making Board
   * Focus: Negotiations, partnerships, deal structuring
   */
  createNegotiationBoard(): { boardRoom: BoardRoomAgent; config: BoardRoomConfig } {
    const boardRoom = this.createBoardRoomAgent();

    const config = boardRoom.createAdHocBoardRoom(
      'Negotiation & Deal Making Board',
      [
        this.createDonaldTrumpAgent(),
        this.createSamZellAgent(),
        this.createElonMuskAgent(),
        this.createLarryFinkAgent(),
      ],
      [BusinessSector.GENERAL],
      'advisory'
    );

    return { boardRoom, config };
  }

  /**
   * Product Strategy Board
   * Focus: Product development, user experience, go-to-market
   */
  createProductStrategyBoard(): { boardRoom: BoardRoomAgent; config: BoardRoomConfig } {
    const boardRoom = this.createBoardRoomAgent();

    const config = boardRoom.createAdHocBoardRoom(
      'Product Strategy Board',
      [
        this.createSteveJobsAgent(),
        this.createMarkZuckerbergAgent(),
        this.createJeffBezosAgent(),
        this.createElonMuskAgent(),
      ],
      [BusinessSector.TECHNOLOGY, BusinessSector.E_COMMERCE],
      'majority'
    );

    return { boardRoom, config };
  }

  /**
   * Growth & Scale Board
   * Focus: Scaling operations, market expansion, growth strategy
   */
  createGrowthBoard(): { boardRoom: BoardRoomAgent; config: BoardRoomConfig } {
    const boardRoom = this.createBoardRoomAgent();

    const config = boardRoom.createAdHocBoardRoom(
      'Growth & Scale Board',
      [
        this.createJeffBezosAgent(),
        this.createMarkZuckerbergAgent(),
        this.createElonMuskAgent(),
        this.createLarryFinkAgent(),
      ],
      [BusinessSector.TECHNOLOGY, BusinessSector.E_COMMERCE, BusinessSector.FINANCE],
      'majority'
    );

    return { boardRoom, config };
  }

  /**
   * Crisis Management Board
   * Focus: Crisis response, rapid decision-making, damage control
   */
  createCrisisBoard(): { boardRoom: BoardRoomAgent; config: BoardRoomConfig } {
    const boardRoom = this.createBoardRoomAgent();

    const config = boardRoom.createAdHocBoardRoom(
      'Crisis Management Board',
      [
        this.createElonMuskAgent(),
        this.createDonaldTrumpAgent(),
        this.createLarryFinkAgent(),
        this.createSamZellAgent(),
      ],
      [BusinessSector.GENERAL],
      'advisory'
    );

    return { boardRoom, config };
  }

  /**
   * Executive Leadership Board
   * All leaders for comprehensive strategic decisions
   */
  createExecutiveBoard(): { boardRoom: BoardRoomAgent; config: BoardRoomConfig } {
    const boardRoom = this.createBoardRoomAgent();

    const config = boardRoom.createAdHocBoardRoom(
      'Executive Leadership Board',
      this.createAllAgents(),
      [
        BusinessSector.TECHNOLOGY,
        BusinessSector.FINANCE,
        BusinessSector.REAL_ESTATE,
        BusinessSector.E_COMMERCE,
        BusinessSector.SOCIAL_MEDIA,
      ],
      'weighted'
    );

    // Equal weight for all members
    config.votingWeights = new Map(
      config.members.map(m => [m.profile.name, 1 / config.members.length])
    );

    return { boardRoom, config };
  }

  /**
   * Create custom board room with specific agents
   */
  createCustomBoardRoom(
    name: string,
    agentNames: Array<
      'musk' | 'jobs' | 'zuckerberg' | 'trump' | 'fink' | 'bezos' | 'zell' | 'bren'
    >,
    focus: BusinessSector[],
    decisionStyle: 'unanimous' | 'majority' | 'weighted' | 'advisory' = 'majority'
  ): { boardRoom: BoardRoomAgent; config: BoardRoomConfig } {
    const boardRoom = this.createBoardRoomAgent();

    const agentMap = {
      musk: this.createElonMuskAgent(),
      jobs: this.createSteveJobsAgent(),
      zuckerberg: this.createMarkZuckerbergAgent(),
      trump: this.createDonaldTrumpAgent(),
      fink: this.createLarryFinkAgent(),
      bezos: this.createJeffBezosAgent(),
      zell: this.createSamZellAgent(),
      bren: this.createDonaldBrenAgent(),
    };

    const members = agentNames.map(name => agentMap[name]);

    const config = boardRoom.createAdHocBoardRoom(name, members, focus, decisionStyle);

    return { boardRoom, config };
  }

  /**
   * Get agent by name
   */
  getAgentByName(
    name: 'musk' | 'jobs' | 'zuckerberg' | 'trump' | 'fink' | 'bezos' | 'zell' | 'bren'
  ): IBehaviorAgent {
    const agentMap = {
      musk: this.createElonMuskAgent(),
      jobs: this.createSteveJobsAgent(),
      zuckerberg: this.createMarkZuckerbergAgent(),
      trump: this.createDonaldTrumpAgent(),
      fink: this.createLarryFinkAgent(),
      bezos: this.createJeffBezosAgent(),
      zell: this.createSamZellAgent(),
      bren: this.createDonaldBrenAgent(),
    };

    return agentMap[name];
  }
}

/**
 * Convenience function to create factory
 */
export function createBehaviorAgentFactory(pool: Pool, redis: Redis): BehaviorAgentFactory {
  return new BehaviorAgentFactory(pool, redis);
}
