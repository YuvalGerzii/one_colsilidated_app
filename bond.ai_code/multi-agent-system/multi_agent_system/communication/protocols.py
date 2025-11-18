"""
Advanced communication protocols for agent interaction.

Includes:
- Negotiation protocols (bargaining, bidding)
- Competition protocols (auctions, contests)
- Collaboration protocols (consensus, voting)
- Coordination protocols (leader election, task allocation)
"""

import asyncio
from typing import Any, Dict, List, Optional, Set, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
import uuid


class NegotiationStatus(Enum):
    """Status of a negotiation."""
    PROPOSED = "proposed"
    COUNTER_OFFERED = "counter_offered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class AuctionType(Enum):
    """Types of auctions."""
    FIRST_PRICE = "first_price"  # Highest bid wins, pays their bid
    SECOND_PRICE = "second_price"  # Highest bid wins, pays second-highest bid
    DUTCH = "dutch"  # Price starts high and decreases
    ENGLISH = "english"  # Price starts low and increases


class VotingMethod(Enum):
    """Voting methods for consensus."""
    MAJORITY = "majority"  # >50% required
    PLURALITY = "plurality"  # Most votes wins
    UNANIMOUS = "unanimous"  # All must agree
    WEIGHTED = "weighted"  # Votes weighted by agent score


@dataclass
class Proposal:
    """A proposal in a negotiation."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    proposer: str = ""
    recipient: str = ""
    subject: str = ""
    offer: Dict[str, Any] = field(default_factory=dict)
    counter_offer: Optional[Dict[str, Any]] = None
    status: NegotiationStatus = NegotiationStatus.PROPOSED
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Bid:
    """A bid in an auction."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    bidder: str = ""
    amount: float = 0.0
    resource_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Vote:
    """A vote in a consensus decision."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    voter: str = ""
    choice: str = ""
    weight: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class NegotiationProtocol:
    """
    Protocol for agent-to-agent negotiation.

    Supports:
    - Proposals and counter-proposals
    - Multi-round bargaining
    - Timeout and expiration
    - Conflict resolution
    """

    def __init__(self):
        """Initialize the negotiation protocol."""
        self.active_negotiations: Dict[str, Proposal] = {}
        self.completed_negotiations: List[Proposal] = []
        self.max_history = 1000

        logger.info("NegotiationProtocol initialized")

    async def propose(
        self,
        proposer: str,
        recipient: str,
        subject: str,
        offer: Dict[str, Any],
        timeout: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new proposal.

        Args:
            proposer: Agent making the proposal
            recipient: Agent receiving the proposal
            subject: Subject of the negotiation
            offer: The offer being made
            timeout: Time until proposal expires (seconds)
            metadata: Additional metadata

        Returns:
            Proposal ID
        """
        expires_at = None
        if timeout:
            expires_at = datetime.now() + timedelta(seconds=timeout)

        proposal = Proposal(
            proposer=proposer,
            recipient=recipient,
            subject=subject,
            offer=offer,
            expires_at=expires_at,
            metadata=metadata or {}
        )

        self.active_negotiations[proposal.id] = proposal

        logger.info(f"Negotiation proposed: {proposer} -> {recipient} on '{subject}'")

        return proposal.id

    async def counter_offer(
        self,
        proposal_id: str,
        agent_id: str,
        counter_offer: Dict[str, Any]
    ) -> bool:
        """
        Make a counter-offer to a proposal.

        Args:
            proposal_id: ID of the proposal
            agent_id: Agent making the counter-offer
            counter_offer: The counter-offer

        Returns:
            True if counter-offer was accepted
        """
        if proposal_id not in self.active_negotiations:
            logger.warning(f"Proposal {proposal_id} not found")
            return False

        proposal = self.active_negotiations[proposal_id]

        # Check if expired
        if proposal.expires_at and datetime.now() > proposal.expires_at:
            proposal.status = NegotiationStatus.EXPIRED
            self._complete_negotiation(proposal_id)
            return False

        # Check if agent is the recipient
        if agent_id != proposal.recipient:
            logger.warning(f"Agent {agent_id} is not the recipient of proposal {proposal_id}")
            return False

        proposal.counter_offer = counter_offer
        proposal.status = NegotiationStatus.COUNTER_OFFERED

        logger.info(f"Counter-offer made on proposal {proposal_id} by {agent_id}")

        return True

    async def accept(
        self,
        proposal_id: str,
        agent_id: str,
        accept_counter: bool = False
    ) -> bool:
        """
        Accept a proposal or counter-offer.

        Args:
            proposal_id: ID of the proposal
            agent_id: Agent accepting
            accept_counter: If True, proposer is accepting the counter-offer

        Returns:
            True if accepted successfully
        """
        if proposal_id not in self.active_negotiations:
            logger.warning(f"Proposal {proposal_id} not found")
            return False

        proposal = self.active_negotiations[proposal_id]

        # Check if expired
        if proposal.expires_at and datetime.now() > proposal.expires_at:
            proposal.status = NegotiationStatus.EXPIRED
            self._complete_negotiation(proposal_id)
            return False

        # Validate acceptance
        if accept_counter:
            # Proposer accepting counter-offer
            if agent_id != proposal.proposer:
                logger.warning(f"Agent {agent_id} is not the proposer")
                return False
            if not proposal.counter_offer:
                logger.warning("No counter-offer to accept")
                return False
        else:
            # Recipient accepting original offer
            if agent_id != proposal.recipient:
                logger.warning(f"Agent {agent_id} is not the recipient")
                return False

        proposal.status = NegotiationStatus.ACCEPTED
        self._complete_negotiation(proposal_id)

        logger.info(f"Proposal {proposal_id} accepted by {agent_id}")

        return True

    async def reject(
        self,
        proposal_id: str,
        agent_id: str
    ) -> bool:
        """
        Reject a proposal.

        Args:
            proposal_id: ID of the proposal
            agent_id: Agent rejecting

        Returns:
            True if rejected successfully
        """
        if proposal_id not in self.active_negotiations:
            logger.warning(f"Proposal {proposal_id} not found")
            return False

        proposal = self.active_negotiations[proposal_id]

        # Validate rejection
        if agent_id not in [proposal.proposer, proposal.recipient]:
            logger.warning(f"Agent {agent_id} is not part of this negotiation")
            return False

        proposal.status = NegotiationStatus.REJECTED
        self._complete_negotiation(proposal_id)

        logger.info(f"Proposal {proposal_id} rejected by {agent_id}")

        return True

    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        """Get a proposal by ID."""
        return self.active_negotiations.get(proposal_id)

    def get_agent_proposals(
        self,
        agent_id: str,
        active_only: bool = True
    ) -> List[Proposal]:
        """
        Get all proposals involving an agent.

        Args:
            agent_id: ID of the agent
            active_only: Only return active negotiations

        Returns:
            List of proposals
        """
        proposals = []

        if active_only:
            proposals = [
                p for p in self.active_negotiations.values()
                if p.proposer == agent_id or p.recipient == agent_id
            ]
        else:
            proposals = [
                p for p in self.completed_negotiations
                if p.proposer == agent_id or p.recipient == agent_id
            ]

        return proposals

    def _complete_negotiation(self, proposal_id: str) -> None:
        """Move a negotiation to completed."""
        if proposal_id in self.active_negotiations:
            proposal = self.active_negotiations.pop(proposal_id)
            self.completed_negotiations.append(proposal)

            # Trim history
            if len(self.completed_negotiations) > self.max_history:
                self.completed_negotiations = self.completed_negotiations[-self.max_history:]


class AuctionProtocol:
    """
    Protocol for competitive bidding/auctions.

    Supports multiple auction types and resource allocation.
    """

    def __init__(self):
        """Initialize the auction protocol."""
        self.active_auctions: Dict[str, Dict[str, Any]] = {}
        self.completed_auctions: List[Dict[str, Any]] = []
        self.max_history = 1000

        logger.info("AuctionProtocol initialized")

    async def create_auction(
        self,
        auctioneer: str,
        resource_id: str,
        auction_type: AuctionType,
        starting_price: float,
        reserve_price: Optional[float] = None,
        duration: float = 60.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new auction.

        Args:
            auctioneer: Agent running the auction
            resource_id: Resource being auctioned
            auction_type: Type of auction
            starting_price: Starting price
            reserve_price: Minimum acceptable price
            duration: Duration in seconds
            metadata: Additional metadata

        Returns:
            Auction ID
        """
        auction_id = str(uuid.uuid4())

        auction = {
            "id": auction_id,
            "auctioneer": auctioneer,
            "resource_id": resource_id,
            "auction_type": auction_type,
            "starting_price": starting_price,
            "reserve_price": reserve_price,
            "current_price": starting_price,
            "bids": [],
            "winner": None,
            "winning_bid": None,
            "created_at": datetime.now(),
            "ends_at": datetime.now() + timedelta(seconds=duration),
            "metadata": metadata or {},
            "status": "active"
        }

        self.active_auctions[auction_id] = auction

        logger.info(
            f"Auction created by {auctioneer} for resource {resource_id} "
            f"(type={auction_type.value}, starting_price={starting_price})"
        )

        # Schedule auction end
        asyncio.create_task(self._end_auction_after_timeout(auction_id, duration))

        return auction_id

    async def place_bid(
        self,
        auction_id: str,
        bidder: str,
        amount: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Place a bid in an auction.

        Args:
            auction_id: ID of the auction
            bidder: Agent placing the bid
            amount: Bid amount
            metadata: Additional metadata

        Returns:
            True if bid was accepted
        """
        if auction_id not in self.active_auctions:
            logger.warning(f"Auction {auction_id} not found")
            return False

        auction = self.active_auctions[auction_id]

        # Check if auction is still active
        if auction["status"] != "active":
            logger.warning(f"Auction {auction_id} is not active")
            return False

        if datetime.now() > auction["ends_at"]:
            await self._end_auction(auction_id)
            return False

        # Validate bid based on auction type
        auction_type = auction["auction_type"]

        if auction_type in [AuctionType.FIRST_PRICE, AuctionType.SECOND_PRICE, AuctionType.ENGLISH]:
            # Bid must be higher than current price
            if amount <= auction["current_price"]:
                logger.info(f"Bid {amount} is not higher than current price {auction['current_price']}")
                return False

        bid = Bid(
            bidder=bidder,
            amount=amount,
            resource_id=auction["resource_id"],
            metadata=metadata or {}
        )

        auction["bids"].append(bid)
        auction["current_price"] = amount

        logger.info(f"Bid placed in auction {auction_id}: {bidder} bid {amount}")

        return True

    async def _end_auction_after_timeout(self, auction_id: str, duration: float) -> None:
        """End an auction after the specified duration."""
        await asyncio.sleep(duration)
        await self._end_auction(auction_id)

    async def _end_auction(self, auction_id: str) -> None:
        """End an auction and determine the winner."""
        if auction_id not in self.active_auctions:
            return

        auction = self.active_auctions[auction_id]
        auction["status"] = "completed"

        if not auction["bids"]:
            logger.info(f"Auction {auction_id} ended with no bids")
            self._complete_auction(auction_id)
            return

        # Determine winner based on auction type
        auction_type = auction["auction_type"]

        if auction_type == AuctionType.FIRST_PRICE:
            # Highest bidder wins and pays their bid
            winning_bid = max(auction["bids"], key=lambda b: b.amount)
            auction["winner"] = winning_bid.bidder
            auction["winning_bid"] = winning_bid.amount

        elif auction_type == AuctionType.SECOND_PRICE:
            # Highest bidder wins but pays second-highest bid
            sorted_bids = sorted(auction["bids"], key=lambda b: b.amount, reverse=True)
            winning_bid = sorted_bids[0]
            second_price = sorted_bids[1].amount if len(sorted_bids) > 1 else winning_bid.amount

            auction["winner"] = winning_bid.bidder
            auction["winning_bid"] = second_price

        elif auction_type in [AuctionType.ENGLISH, AuctionType.DUTCH]:
            # Highest bid wins
            winning_bid = max(auction["bids"], key=lambda b: b.amount)
            auction["winner"] = winning_bid.bidder
            auction["winning_bid"] = winning_bid.amount

        # Check reserve price
        if auction["reserve_price"] and auction["winning_bid"] < auction["reserve_price"]:
            logger.info(f"Auction {auction_id} ended: winning bid did not meet reserve price")
            auction["winner"] = None
            auction["winning_bid"] = None
        else:
            logger.info(
                f"Auction {auction_id} ended: winner={auction['winner']}, "
                f"price={auction['winning_bid']}"
            )

        self._complete_auction(auction_id)

    def get_auction(self, auction_id: str) -> Optional[Dict[str, Any]]:
        """Get auction details."""
        return self.active_auctions.get(auction_id)

    def list_active_auctions(self) -> List[Dict[str, Any]]:
        """List all active auctions."""
        return list(self.active_auctions.values())

    def _complete_auction(self, auction_id: str) -> None:
        """Move auction to completed."""
        if auction_id in self.active_auctions:
            auction = self.active_auctions.pop(auction_id)
            self.completed_auctions.append(auction)

            # Trim history
            if len(self.completed_auctions) > self.max_history:
                self.completed_auctions = self.completed_auctions[-self.max_history:]


class ConsensusProtocol:
    """
    Protocol for collaborative decision-making and consensus.

    Supports multiple voting methods and collective decisions.
    """

    def __init__(self):
        """Initialize the consensus protocol."""
        self.active_votes: Dict[str, Dict[str, Any]] = {}
        self.completed_votes: List[Dict[str, Any]] = []
        self.max_history = 1000

        logger.info("ConsensusProtocol initialized")

    async def initiate_vote(
        self,
        initiator: str,
        subject: str,
        choices: List[str],
        eligible_voters: Set[str],
        voting_method: VotingMethod = VotingMethod.MAJORITY,
        duration: float = 60.0,
        voter_weights: Optional[Dict[str, float]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Initiate a vote.

        Args:
            initiator: Agent initiating the vote
            subject: What is being voted on
            choices: Available choices
            eligible_voters: Set of agents eligible to vote
            voting_method: Method for determining outcome
            duration: Duration in seconds
            voter_weights: Optional weights for weighted voting
            metadata: Additional metadata

        Returns:
            Vote ID
        """
        vote_id = str(uuid.uuid4())

        vote = {
            "id": vote_id,
            "initiator": initiator,
            "subject": subject,
            "choices": choices,
            "eligible_voters": eligible_voters,
            "voting_method": voting_method,
            "votes": [],
            "voter_weights": voter_weights or {},
            "result": None,
            "created_at": datetime.now(),
            "ends_at": datetime.now() + timedelta(seconds=duration),
            "metadata": metadata or {},
            "status": "active"
        }

        self.active_votes[vote_id] = vote

        logger.info(
            f"Vote initiated by {initiator} on '{subject}' "
            f"(method={voting_method.value}, voters={len(eligible_voters)})"
        )

        # Schedule vote end
        asyncio.create_task(self._end_vote_after_timeout(vote_id, duration))

        return vote_id

    async def cast_vote(
        self,
        vote_id: str,
        voter: str,
        choice: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Cast a vote.

        Args:
            vote_id: ID of the vote
            voter: Agent voting
            choice: Their choice
            metadata: Additional metadata

        Returns:
            True if vote was cast successfully
        """
        if vote_id not in self.active_votes:
            logger.warning(f"Vote {vote_id} not found")
            return False

        vote = self.active_votes[vote_id]

        # Check if still active
        if vote["status"] != "active":
            logger.warning(f"Vote {vote_id} is not active")
            return False

        # Check if voter is eligible
        if voter not in vote["eligible_voters"]:
            logger.warning(f"Agent {voter} is not eligible to vote")
            return False

        # Check if already voted
        if any(v.voter == voter for v in vote["votes"]):
            logger.warning(f"Agent {voter} has already voted")
            return False

        # Check if choice is valid
        if choice not in vote["choices"]:
            logger.warning(f"Choice '{choice}' is not valid")
            return False

        # Get weight
        weight = vote["voter_weights"].get(voter, 1.0)

        ballot = Vote(
            voter=voter,
            choice=choice,
            weight=weight,
            metadata=metadata or {}
        )

        vote["votes"].append(ballot)

        logger.info(f"Vote cast in {vote_id}: {voter} chose '{choice}'")

        return True

    async def _end_vote_after_timeout(self, vote_id: str, duration: float) -> None:
        """End a vote after the specified duration."""
        await asyncio.sleep(duration)
        await self._end_vote(vote_id)

    async def _end_vote(self, vote_id: str) -> None:
        """End a vote and determine the result."""
        if vote_id not in self.active_votes:
            return

        vote = self.active_votes[vote_id]
        vote["status"] = "completed"

        if not vote["votes"]:
            logger.info(f"Vote {vote_id} ended with no votes cast")
            self._complete_vote(vote_id)
            return

        # Tally votes based on voting method
        voting_method = vote["voting_method"]
        choice_scores = {choice: 0.0 for choice in vote["choices"]}

        for ballot in vote["votes"]:
            choice_scores[ballot.choice] += ballot.weight

        total_weight = sum(choice_scores.values())
        eligible_weight = sum(
            vote["voter_weights"].get(v, 1.0)
            for v in vote["eligible_voters"]
        )

        if voting_method == VotingMethod.PLURALITY:
            # Choice with most votes wins
            winner = max(choice_scores.items(), key=lambda x: x[1])
            vote["result"] = winner[0]

        elif voting_method == VotingMethod.MAJORITY:
            # Requires >50% of votes
            winner = max(choice_scores.items(), key=lambda x: x[1])
            if winner[1] > total_weight / 2:
                vote["result"] = winner[0]
            else:
                vote["result"] = None  # No majority

        elif voting_method == VotingMethod.UNANIMOUS:
            # All votes must be the same
            if len(set(choice_scores.values())) == 1 and choice_scores[vote["choices"][0]] > 0:
                vote["result"] = vote["choices"][0]
            else:
                vote["result"] = None  # Not unanimous

        elif voting_method == VotingMethod.WEIGHTED:
            # Weighted voting (already applied via weights)
            winner = max(choice_scores.items(), key=lambda x: x[1])
            vote["result"] = winner[0]

        vote["choice_scores"] = choice_scores
        vote["participation_rate"] = len(vote["votes"]) / len(vote["eligible_voters"])

        logger.info(
            f"Vote {vote_id} ended: result='{vote['result']}', "
            f"participation={vote['participation_rate']:.1%}"
        )

        self._complete_vote(vote_id)

    def get_vote(self, vote_id: str) -> Optional[Dict[str, Any]]:
        """Get vote details."""
        return self.active_votes.get(vote_id)

    def list_active_votes(self) -> List[Dict[str, Any]]:
        """List all active votes."""
        return list(self.active_votes.values())

    def _complete_vote(self, vote_id: str) -> None:
        """Move vote to completed."""
        if vote_id in self.active_votes:
            vote = self.active_votes.pop(vote_id)
            self.completed_votes.append(vote)

            # Trim history
            if len(self.completed_votes) > self.max_history:
                self.completed_votes = self.completed_votes[-self.max_history:]
