"""Deal scoring algorithm for prioritization and success prediction."""

from typing import Dict, Any, Optional, Tuple
import logging
from datetime import datetime, date
from sqlalchemy.orm import Session

from app.models.crm import Deal, DealScore, Broker, Comp, DealStage, DealTask, DealDocument, TaskStatus, DocumentStatus
from app.settings import settings

logger = logging.getLogger(__name__)


class DealScoringService:
    """Service for calculating deal scores and success predictions."""

    VERSION = "1.0.0"

    def __init__(self):
        """Initialize deal scoring service."""
        pass

    def calculate_deal_score(
        self,
        db: Session,
        deal: Deal,
        save_to_db: bool = True
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate comprehensive deal score.

        Args:
            db: Database session
            deal: Deal object
            save_to_db: Whether to save score to database

        Returns:
            Tuple of (total_score, detailed_factors)
        """
        # Calculate individual component scores
        financial_score = self._calculate_financial_score(deal)
        market_score = self._calculate_market_score(db, deal)
        location_score = self._calculate_location_score(db, deal)
        property_score = self._calculate_property_score(deal)
        timing_score = self._calculate_timing_score(deal)
        relationship_score = self._calculate_relationship_score(db, deal)
        progress_score = self._calculate_progress_score(db, deal)

        # Weighted average (customize weights as needed)
        weights = {
            'financial': 0.30,
            'market': 0.15,
            'location': 0.10,
            'property': 0.15,
            'timing': 0.10,
            'relationship': 0.10,
            'progress': 0.10,
        }

        total_score = (
            financial_score * weights['financial'] +
            market_score * weights['market'] +
            location_score * weights['location'] +
            property_score * weights['property'] +
            timing_score * weights['timing'] +
            relationship_score * weights['relationship'] +
            progress_score * weights['progress']
        )

        # Predict success probability
        success_probability = self._predict_success_probability(
            db, deal, total_score
        )

        # Estimate days to close
        estimated_days = self._estimate_days_to_close(db, deal)

        # Detailed factors
        factors = {
            'financial_score': financial_score,
            'market_score': market_score,
            'location_score': location_score,
            'property_score': property_score,
            'timing_score': timing_score,
            'relationship_score': relationship_score,
            'progress_score': progress_score,
            'weights': weights,
            'scoring_date': datetime.utcnow().isoformat(),
        }

        # Save to database
        if save_to_db:
            deal_score = DealScore(
                deal_id=deal.id,
                total_score=total_score,
                financial_score=financial_score,
                market_score=market_score,
                location_score=location_score,
                property_score=property_score,
                timing_score=timing_score,
                relationship_score=relationship_score,
                success_probability=success_probability,
                estimated_days_to_close=estimated_days,
                scoring_model_version=self.VERSION,
                factors=factors,
                confidence=85.0,  # Model confidence
            )
            db.add(deal_score)
            db.commit()

        return total_score, factors

    def _calculate_financial_score(self, deal: Deal) -> float:
        """Calculate financial metrics score (0-100)."""
        score = 0.0
        components = 0

        # Cap rate evaluation
        if deal.cap_rate:
            if deal.cap_rate >= 7.0:
                score += 100
            elif deal.cap_rate >= 5.0:
                score += 70
            elif deal.cap_rate >= 3.0:
                score += 40
            else:
                score += 20
            components += 1

        # IRR target evaluation
        if deal.irr_target:
            if deal.irr_target >= 20.0:
                score += 100
            elif deal.irr_target >= 15.0:
                score += 80
            elif deal.irr_target >= 10.0:
                score += 60
            else:
                score += 30
            components += 1

        # Price comparison (estimated value vs asking price)
        if deal.estimated_value and deal.asking_price and deal.asking_price > 0:
            discount = ((deal.estimated_value - deal.asking_price) / deal.asking_price) * 100
            if discount >= 20:  # 20%+ discount
                score += 100
            elif discount >= 10:  # 10-20% discount
                score += 80
            elif discount >= 0:  # At or below estimate
                score += 60
            elif discount >= -10:  # Up to 10% premium
                score += 40
            else:  # More than 10% premium
                score += 20
            components += 1

        # Confidence level
        if deal.confidence_level:
            score += deal.confidence_level
            components += 1

        return score / components if components > 0 else 50.0

    def _calculate_market_score(self, db: Session, deal: Deal) -> float:
        """Calculate market conditions score (0-100)."""
        score = 50.0  # Default neutral score

        if not deal.market or not deal.property_type:
            return score

        # Get comparable sales in the market
        comps = db.query(Comp).filter(
            Comp.market == deal.market,
            Comp.property_type == deal.property_type,
        ).limit(10).all()

        if not comps:
            return score

        # Calculate average cap rate in market
        cap_rates = [c.cap_rate for c in comps if c.cap_rate]
        if cap_rates:
            avg_cap_rate = sum(cap_rates) / len(cap_rates)
            # Compare to deal cap rate
            if deal.cap_rate:
                if deal.cap_rate >= avg_cap_rate + 1.0:
                    score = 90  # Better than market
                elif deal.cap_rate >= avg_cap_rate:
                    score = 75
                elif deal.cap_rate >= avg_cap_rate - 0.5:
                    score = 60
                else:
                    score = 40  # Below market

        # Recent transaction velocity
        recent_comps = [c for c in comps if c.sale_date and
                        (datetime.now().date() - c.sale_date).days <= 180]

        if len(recent_comps) >= 5:
            score += 10  # Active market bonus
        elif len(recent_comps) <= 1:
            score -= 10  # Illiquid market penalty

        return max(0, min(100, score))

    def _calculate_location_score(self, db: Session, deal: Deal) -> float:
        """Calculate location quality score (0-100)."""
        score = 50.0  # Default neutral

        # Could integrate with external APIs for:
        # - Crime statistics
        # - School ratings
        # - Demographics
        # - Economic indicators
        # - Job growth

        # For now, use market-based heuristics
        if deal.market:
            # Tier 1 markets (example)
            tier1_markets = ['New York', 'San Francisco', 'Boston', 'Seattle', 'Austin']
            tier2_markets = ['Atlanta', 'Denver', 'Nashville', 'Charlotte', 'Phoenix']

            if any(t1 in deal.market for t1 in tier1_markets):
                score = 85
            elif any(t2 in deal.market for t2 in tier2_markets):
                score = 70
            else:
                score = 55

        return score

    def _calculate_property_score(self, deal: Deal) -> float:
        """Calculate property condition/quality score (0-100)."""
        score = 50.0  # Default

        # Property size (larger = more stable)
        if deal.units:
            if deal.units >= 100:
                score += 20
            elif deal.units >= 50:
                score += 15
            elif deal.units >= 20:
                score += 10
            elif deal.units >= 5:
                score += 5

        # Square footage
        if deal.square_feet:
            if deal.square_feet >= 100000:
                score += 15
            elif deal.square_feet >= 50000:
                score += 10
            elif deal.square_feet >= 20000:
                score += 5

        return min(100, score)

    def _calculate_timing_score(self, deal: Deal) -> float:
        """Calculate deal timing score (0-100)."""
        score = 50.0

        today = datetime.now().date()

        # Time in pipeline (too long = red flag)
        if deal.date_identified:
            days_in_pipeline = (today - deal.date_identified).days
            if days_in_pipeline <= 30:
                score = 90  # Fresh deal
            elif days_in_pipeline <= 90:
                score = 75  # Normal
            elif days_in_pipeline <= 180:
                score = 50  # Getting stale
            else:
                score = 30  # Very stale

        # Expected closing proximity
        if deal.expected_closing:
            days_to_close = (deal.expected_closing - today).days
            if 30 <= days_to_close <= 90:
                score += 10  # Good timing
            elif days_to_close < 0:
                score -= 20  # Overdue

        return max(0, min(100, score))

    def _calculate_relationship_score(self, db: Session, deal: Deal) -> float:
        """Calculate broker relationship score (0-100)."""
        score = 50.0  # Default

        if not deal.broker_id:
            return score

        broker = db.query(Broker).filter(Broker.id == deal.broker_id).first()
        if not broker:
            return score

        # Broker success rate
        if broker.success_rate >= 80:
            score = 90
        elif broker.success_rate >= 60:
            score = 75
        elif broker.success_rate >= 40:
            score = 60
        else:
            score = 40

        # Relationship strength
        if broker.relationship_strength:
            score += (broker.relationship_strength - 3) * 5  # Adjust based on strength

        return max(0, min(100, score))

    def _calculate_progress_score(self, db: Session, deal: Deal) -> float:
        """Calculate deal progress score based on tasks and documents (0-100)."""
        score = 0.0

        # Task completion rate
        tasks = db.query(DealTask).filter(DealTask.deal_id == deal.id).all()
        if tasks:
            completed = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
            task_completion_rate = (completed / len(tasks)) * 100
            score += task_completion_rate * 0.5
        else:
            score += 25  # No tasks yet

        # Document approval rate
        documents = db.query(DealDocument).filter(DealDocument.deal_id == deal.id).all()
        if documents:
            approved = len([d for d in documents if d.status == DocumentStatus.APPROVED])
            doc_approval_rate = (approved / len(documents)) * 100
            score += doc_approval_rate * 0.5
        else:
            score += 25  # No documents yet

        return min(100, score)

    def _predict_success_probability(
        self, db: Session, deal: Deal, total_score: float
    ) -> float:
        """
        Predict probability of deal closing (0-100).

        This is a simplified heuristic. In production, you would use
        the existing ML model in app/ml/deal_success.py
        """
        # Base probability from score
        base_prob = total_score

        # Adjust based on stage
        stage_multipliers = {
            DealStage.RESEARCH: 0.3,
            DealStage.LOI: 0.5,
            DealStage.DUE_DILIGENCE: 0.7,
            DealStage.CLOSING: 0.9,
            DealStage.CLOSED: 1.0,
            DealStage.DEAD: 0.0,
        }

        multiplier = stage_multipliers.get(deal.stage, 0.5)
        probability = base_prob * multiplier

        return max(0, min(100, probability))

    def _estimate_days_to_close(self, db: Session, deal: Deal) -> int:
        """Estimate days to close based on stage and historical data."""
        # Default estimates by stage
        stage_days = {
            DealStage.RESEARCH: 120,
            DealStage.LOI: 90,
            DealStage.DUE_DILIGENCE: 60,
            DealStage.CLOSING: 30,
            DealStage.CLOSED: 0,
            DealStage.DEAD: 0,
        }

        base_days = stage_days.get(deal.stage, 90)

        # Adjust based on expected closing date
        if deal.expected_closing:
            days_to_expected = (deal.expected_closing - datetime.now().date()).days
            if days_to_expected > 0:
                return days_to_expected

        return base_days

    def get_latest_score(self, db: Session, deal_id: str) -> Optional[DealScore]:
        """Get the latest score for a deal."""
        return db.query(DealScore).filter(
            DealScore.deal_id == deal_id
        ).order_by(DealScore.created_at.desc()).first()

    def recalculate_all_scores(self, db: Session) -> int:
        """Recalculate scores for all active deals."""
        deals = db.query(Deal).filter(
            Deal.status == 'active'
        ).all()

        count = 0
        for deal in deals:
            try:
                self.calculate_deal_score(db, deal, save_to_db=True)
                count += 1
            except Exception as e:
                logger.error(f"Error scoring deal {deal.id}: {e}")

        return count


# Global deal scoring service instance
deal_scoring_service = DealScoringService()
