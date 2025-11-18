"""Integration between Deal Pipeline and Due Diligence Model."""

from typing import Dict, Any, Optional
import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.crm import Deal, DealTask, DealDocument, DealActivity, ActivityType
from app.models.saved_calculation import SavedCalculation, CalculationType

logger = logging.getLogger(__name__)


class DueDiligenceIntegration:
    """Service for integrating CRM deals with due diligence models."""

    def create_dd_model_for_deal(
        self,
        db: Session,
        deal: Deal,
        user_id: UUID,
    ) -> SavedCalculation:
        """
        Create a new Due Diligence model for a deal.

        Args:
            db: Database session
            deal: Deal object
            user_id: User creating the DD model

        Returns:
            SavedCalculation object
        """
        # Build input data from deal
        input_data = {
            'property_name': deal.property_name,
            'property_address': deal.property_address,
            'property_type': deal.property_type,
            'market': deal.market,
            'purchase_price': deal.asking_price,
            'units': deal.units,
            'square_feet': deal.square_feet,
            'cap_rate': deal.cap_rate,
            # Add more fields as needed
        }

        # Initialize output data structure
        output_data = {
            'deal_id': str(deal.id),
            'status': 'in_progress',
            'completion_percentage': 0,
            'categories': {
                'financial': {'complete': False, 'findings': []},
                'legal': {'complete': False, 'findings': []},
                'environmental': {'complete': False, 'findings': []},
                'physical': {'complete': False, 'findings': []},
                'market': {'complete': False, 'findings': []},
            },
            'risk_rating': 'medium',
            'recommendation': None,
        }

        # Create saved calculation
        dd_model = SavedCalculation(
            user_id=user_id,
            calculation_type=CalculationType.DUE_DILIGENCE,
            property_name=deal.property_name,
            property_address=deal.property_address,
            input_data=input_data,
            output_data=output_data,
            notes=f"Due diligence for deal: {deal.property_name}",
            tags=['due-diligence', deal.stage.value],
        )

        db.add(dd_model)

        # Log activity
        activity = DealActivity(
            deal_id=deal.id,
            activity_type=ActivityType.NOTE_ADDED,
            title="Due Diligence Model Created",
            description=f"Created due diligence model for {deal.property_name}",
            metadata={'dd_model_id': str(dd_model.id)}
        )
        db.add(activity)

        db.commit()
        db.refresh(dd_model)

        logger.info(f"Created DD model {dd_model.id} for deal {deal.id}")

        return dd_model

    def update_dd_progress_from_tasks(
        self,
        db: Session,
        deal: Deal,
        dd_model: SavedCalculation,
    ) -> SavedCalculation:
        """
        Update due diligence model progress based on completed tasks.

        Args:
            db: Database session
            deal: Deal object
            dd_model: Due diligence SavedCalculation

        Returns:
            Updated SavedCalculation
        """
        # Get all tasks for deal
        tasks = db.query(DealTask).filter(DealTask.deal_id == deal.id).all()

        if not tasks:
            return dd_model

        # Calculate completion by category
        category_mapping = {
            'Financial Review': 'financial',
            'Legal': 'legal',
            'Environmental': 'environmental',
            'Physical': 'physical',
            'Site Visit': 'physical',
            'Market Research': 'market',
        }

        category_tasks = {}
        for task in tasks:
            category = category_mapping.get(task.task_type, 'other')
            if category not in category_tasks:
                category_tasks[category] = {'total': 0, 'completed': 0}

            category_tasks[category]['total'] += 1
            if task.status == 'completed':
                category_tasks[category]['completed'] += 1

        # Update output data
        output_data = dd_model.output_data.copy()

        for category, counts in category_tasks.items():
            if category in output_data['categories']:
                completion = (counts['completed'] / counts['total']) * 100
                output_data['categories'][category]['complete'] = completion >= 100
                output_data['categories'][category]['completion_percentage'] = completion

        # Calculate overall completion
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == 'completed'])
        output_data['completion_percentage'] = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Update status
        if output_data['completion_percentage'] >= 100:
            output_data['status'] = 'complete'
        elif output_data['completion_percentage'] > 0:
            output_data['status'] = 'in_progress'
        else:
            output_data['status'] = 'not_started'

        dd_model.output_data = output_data

        db.commit()
        db.refresh(dd_model)

        return dd_model

    def sync_documents_to_dd_model(
        self,
        db: Session,
        deal: Deal,
        dd_model: SavedCalculation,
    ) -> SavedCalculation:
        """
        Sync document checklist to due diligence model.

        Args:
            db: Database session
            deal: Deal object
            dd_model: Due diligence SavedCalculation

        Returns:
            Updated SavedCalculation
        """
        # Get all documents
        documents = db.query(DealDocument).filter(DealDocument.deal_id == deal.id).all()

        if not documents:
            return dd_model

        # Group by category
        category_mapping = {
            'Financial': 'financial',
            'Legal': 'legal',
            'Environmental': 'environmental',
            'Physical': 'physical',
        }

        output_data = dd_model.output_data.copy()

        for doc in documents:
            category = category_mapping.get(doc.document_type, 'other')
            if category in output_data['categories']:
                if 'documents' not in output_data['categories'][category]:
                    output_data['categories'][category]['documents'] = []

                doc_info = {
                    'name': doc.document_name,
                    'status': doc.status.value,
                    'received_date': str(doc.received_date) if doc.received_date else None,
                    'approved_date': str(doc.approved_date) if doc.approved_date else None,
                    'is_required': doc.is_required,
                }
                output_data['categories'][category]['documents'].append(doc_info)

        dd_model.output_data = output_data

        db.commit()
        db.refresh(dd_model)

        return dd_model

    def add_finding_to_dd_model(
        self,
        db: Session,
        dd_model: SavedCalculation,
        category: str,
        finding: Dict[str, Any],
    ) -> SavedCalculation:
        """
        Add a finding to a due diligence category.

        Args:
            db: Database session
            dd_model: Due diligence SavedCalculation
            category: Category name (financial, legal, etc.)
            finding: Finding data

        Returns:
            Updated SavedCalculation
        """
        output_data = dd_model.output_data.copy()

        if category in output_data['categories']:
            if 'findings' not in output_data['categories'][category]:
                output_data['categories'][category]['findings'] = []

            output_data['categories'][category]['findings'].append(finding)

            dd_model.output_data = output_data
            db.commit()
            db.refresh(dd_model)

        return dd_model

    def calculate_risk_rating(
        self,
        db: Session,
        dd_model: SavedCalculation,
    ) -> str:
        """
        Calculate overall risk rating based on findings.

        Args:
            db: Database session
            dd_model: Due diligence SavedCalculation

        Returns:
            Risk rating: 'low', 'medium', 'high'
        """
        output_data = dd_model.output_data

        # Count findings by severity
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0

        for category_data in output_data['categories'].values():
            findings = category_data.get('findings', [])
            for finding in findings:
                severity = finding.get('severity', 'medium')
                if severity == 'high':
                    high_risk_count += 1
                elif severity == 'medium':
                    medium_risk_count += 1
                else:
                    low_risk_count += 1

        # Determine overall risk
        if high_risk_count >= 3:
            risk_rating = 'high'
        elif high_risk_count >= 1 or medium_risk_count >= 5:
            risk_rating = 'medium-high'
        elif medium_risk_count >= 2:
            risk_rating = 'medium'
        elif medium_risk_count >= 1 or low_risk_count >= 3:
            risk_rating = 'medium-low'
        else:
            risk_rating = 'low'

        # Update model
        output_data['risk_rating'] = risk_rating
        dd_model.output_data = output_data
        db.commit()

        return risk_rating

    def generate_recommendation(
        self,
        db: Session,
        deal: Deal,
        dd_model: SavedCalculation,
    ) -> str:
        """
        Generate a recommendation based on due diligence findings.

        Args:
            db: Database session
            deal: Deal object
            dd_model: Due diligence SavedCalculation

        Returns:
            Recommendation: 'proceed', 'proceed_with_caution', 'renegotiate', 'pass'
        """
        output_data = dd_model.output_data
        risk_rating = output_data.get('risk_rating', 'medium')
        completion = output_data.get('completion_percentage', 0)

        # Can't recommend if not complete
        if completion < 80:
            recommendation = 'incomplete'
        elif risk_rating in ['high', 'medium-high']:
            recommendation = 'pass'
        elif risk_rating == 'medium':
            # Check if deal fundamentals are strong
            if deal.cap_rate and deal.cap_rate >= 6.0:
                recommendation = 'proceed_with_caution'
            else:
                recommendation = 'renegotiate'
        else:  # Low or medium-low risk
            recommendation = 'proceed'

        # Update model
        output_data['recommendation'] = recommendation
        dd_model.output_data = output_data
        db.commit()

        return recommendation

    def get_dd_model_for_deal(
        self,
        db: Session,
        deal_id: UUID,
    ) -> Optional[SavedCalculation]:
        """
        Get the due diligence model for a deal.

        Args:
            db: Database session
            deal_id: Deal UUID

        Returns:
            SavedCalculation or None
        """
        # Search in output_data JSON for deal_id
        dd_models = db.query(SavedCalculation).filter(
            SavedCalculation.calculation_type == CalculationType.DUE_DILIGENCE,
            SavedCalculation.is_current_version == True,
        ).all()

        for model in dd_models:
            if model.output_data.get('deal_id') == str(deal_id):
                return model

        return None


# Global due diligence integration instance
due_diligence_integration = DueDiligenceIntegration()
