"""
PDF Extraction Service

Comprehensive service for:
- PDF document upload and management
- Financial statement extraction from PDFs
- Database storage of extracted data
- Integration with DCF/LBO models
- Historical valuation tracking
- Comparison and analysis

This service bridges the PDF extraction pipeline with the database models
and provides high-level methods for the API endpoints.
"""

import os
import uuid
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from app.models.pdf_documents import (
    FinancialDocument,
    ExtractedIncomeStatement,
    ExtractedBalanceSheet,
    ExtractedCashFlow,
    ValuationSnapshot,
    ValuationComparison,
    DocumentType,
    ExtractionStatus,
    PeriodType,
)
from app.models.financial_models import DCFModel, LBOModel
from app.models.company import Company

logger = logging.getLogger(__name__)


class PDFExtractionService:
    """
    Main service for PDF extraction and financial data management
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================================
    # PDF UPLOAD AND EXTRACTION
    # =====================================================================

    async def upload_and_extract(
        self,
        file_path: str,
        filename: str,
        document_type: DocumentType,
        company_id: Optional[str] = None,
        user_id: Optional[str] = None,
        use_ai: bool = False
    ) -> Dict:
        """
        Complete workflow: Upload PDF → Extract data → Store in database

        Args:
            file_path: Path to uploaded PDF
            filename: Original filename
            document_type: Type of document
            company_id: Optional company UUID
            user_id: User who uploaded
            use_ai: Whether to use AI-enhanced extraction

        Returns:
            Dictionary with document_id, extraction status, and results
        """
        logger.info(f"Starting PDF extraction for {filename}")

        # Step 1: Create document record
        document = FinancialDocument(
            id=uuid.uuid4(),
            document_name=filename,
            document_type=document_type,
            company_id=uuid.UUID(company_id) if company_id else None,
            file_path=file_path,
            file_size_kb=os.path.getsize(file_path) // 1024 if os.path.exists(file_path) else None,
            uploaded_by=uuid.UUID(user_id) if user_id else None,
            extraction_status=ExtractionStatus.PROCESSING,
            user_id=uuid.UUID(user_id) if user_id else None,
        )

        try:
            self.db.add(document)
            self.db.commit()
            logger.info(f"Created document record: {document.id}")

            # Step 2: Extract financial data from PDF
            extracted_data = await self._extract_from_pdf(file_path, use_ai)

            # Step 3: Parse and validate extracted data
            validation_results = self._validate_extraction(extracted_data)

            # Step 4: Store extracted financial statements
            stored_records = await self._store_extracted_data(
                document.id,
                company_id,
                extracted_data,
                validation_results
            )

            # Step 5: Update document record
            document.extraction_status = (
                ExtractionStatus.NEEDS_REVIEW if validation_results['needs_review']
                else ExtractionStatus.COMPLETED
            )
            document.extraction_date = datetime.utcnow()
            document.extraction_method = extracted_data.get('extraction_method', 'pdfplumber')
            document.extraction_confidence = validation_results.get('overall_confidence', 0.0)
            document.needs_review = validation_results['needs_review']
            document.company_name = extracted_data.get('company_name')
            document.periods_detected = extracted_data.get('periods', [])
            document.statements_found = {
                'income_statements': len(extracted_data.get('income_statements', [])),
                'balance_sheets': len(extracted_data.get('balance_sheets', [])),
                'cash_flows': len(extracted_data.get('cash_flows', []))
            }
            document.extraction_errors = validation_results.get('issues', [])

            self.db.commit()

            logger.info(f"PDF extraction completed: {document.id}")

            return {
                'document_id': str(document.id),
                'status': document.extraction_status.value,
                'confidence': document.extraction_confidence,
                'needs_review': document.needs_review,
                'statements_extracted': document.statements_found,
                'periods': document.periods_detected,
                'records_created': len(stored_records)
            }

        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            document.extraction_status = ExtractionStatus.FAILED
            document.extraction_errors = [str(e)]
            self.db.commit()
            raise

    async def _extract_from_pdf(self, file_path: str, use_ai: bool = False) -> Dict:
        """
        Run the PDF extraction pipeline

        This method would integrate with the PDF extraction code from
        /financial_platform/pdf extraction/

        For now, returns a placeholder structure.
        """
        # In production, this would be:
        # from financial_platform.pdf_extraction.pdf_financial_extractor import extract_financial_statements
        # return extract_financial_statements(file_path)

        # Placeholder structure matching the extraction output format
        return {
            'document_type': 'Quarterly Report',
            'company_name': 'Example Corp',
            'periods': [
                {
                    'period_date': '2025-09-30',
                    'period_type': 'Quarterly',
                    'fiscal_year': 2025,
                    'fiscal_quarter': 3
                }
            ],
            'extraction_method': 'hybrid' if use_ai else 'pdfplumber',
            'income_statements': [],
            'balance_sheets': [],
            'cash_flows': []
        }

    def _validate_extraction(self, extracted_data: Dict) -> Dict:
        """
        Validate extracted financial data

        Returns validation results with confidence scores and issues
        """
        validation = {
            'overall_confidence': 0.0,
            'needs_review': False,
            'issues': [],
            'statement_validations': {}
        }

        # Validate each income statement
        for idx, stmt in enumerate(extracted_data.get('income_statements', [])):
            is_valid, issues = self._validate_income_statement(stmt)
            confidence = stmt.get('confidence_score', 0.0)

            validation['statement_validations'][f'income_{idx}'] = {
                'valid': is_valid,
                'issues': issues,
                'confidence': confidence
            }

            if not is_valid or confidence < 0.85:
                validation['needs_review'] = True
                validation['issues'].extend(issues)

        # Validate balance sheets
        for idx, stmt in enumerate(extracted_data.get('balance_sheets', [])):
            is_valid, issues = self._validate_balance_sheet(stmt)
            confidence = stmt.get('confidence_score', 0.0)

            validation['statement_validations'][f'balance_{idx}'] = {
                'valid': is_valid,
                'issues': issues,
                'confidence': confidence
            }

            if not is_valid or confidence < 0.85:
                validation['needs_review'] = True
                validation['issues'].extend(issues)

        # Calculate overall confidence
        all_confidences = [
            v['confidence'] for v in validation['statement_validations'].values()
        ]
        if all_confidences:
            validation['overall_confidence'] = sum(all_confidences) / len(all_confidences)

        return validation

    def _validate_income_statement(self, data: Dict) -> Tuple[bool, List[str]]:
        """Validate income statement data"""
        issues = []

        # Check for required fields
        revenue = data.get('revenue')
        net_income = data.get('net_income')

        if not revenue:
            issues.append("Missing revenue")
        if not net_income:
            issues.append("Missing net income")

        # Logical checks
        if revenue and net_income:
            if abs(net_income) > abs(revenue):
                issues.append("Net income exceeds revenue - possible error")

        is_valid = len(issues) == 0
        return is_valid, issues

    def _validate_balance_sheet(self, data: Dict) -> Tuple[bool, List[str]]:
        """Validate balance sheet data"""
        issues = []

        # Check accounting equation: Assets = Liabilities + Equity
        assets = data.get('total_assets')
        liabilities = data.get('total_liabilities')
        equity = data.get('total_equity')

        if assets and liabilities and equity:
            calculated_assets = liabilities + equity
            diff_pct = abs(assets - calculated_assets) / assets if assets != 0 else 0

            if diff_pct > 0.01:  # Allow 1% difference for rounding
                issues.append(
                    f"Balance sheet doesn't balance: "
                    f"Assets ({assets}) != L ({liabilities}) + E ({equity})"
                )

        is_valid = len(issues) == 0
        return is_valid, issues

    async def _store_extracted_data(
        self,
        document_id: uuid.UUID,
        company_id: Optional[str],
        extracted_data: Dict,
        validation: Dict
    ) -> List[str]:
        """Store all extracted financial statements in database"""
        stored_ids = []

        # Store income statements
        for stmt in extracted_data.get('income_statements', []):
            income_id = self._store_income_statement(
                document_id,
                company_id,
                stmt,
                validation
            )
            if income_id:
                stored_ids.append(str(income_id))

        # Store balance sheets
        for stmt in extracted_data.get('balance_sheets', []):
            balance_id = self._store_balance_sheet(
                document_id,
                company_id,
                stmt,
                validation
            )
            if balance_id:
                stored_ids.append(str(balance_id))

        # Store cash flows
        for stmt in extracted_data.get('cash_flows', []):
            cashflow_id = self._store_cash_flow(
                document_id,
                company_id,
                stmt,
                validation
            )
            if cashflow_id:
                stored_ids.append(str(cashflow_id))

        self.db.commit()
        return stored_ids

    def _store_income_statement(
        self,
        document_id: uuid.UUID,
        company_id: Optional[str],
        data: Dict,
        validation: Dict
    ) -> Optional[uuid.UUID]:
        """Store income statement in database"""
        try:
            period = data.get('period', {})

            statement = ExtractedIncomeStatement(
                id=uuid.uuid4(),
                document_id=document_id,
                company_id=uuid.UUID(company_id) if company_id else None,

                # Period
                period_date=period.get('period_date', ''),
                period_type=PeriodType(period.get('period_type', 'Quarterly')),
                fiscal_year=period.get('fiscal_year', 2025),
                fiscal_quarter=period.get('fiscal_quarter'),

                # Income statement fields
                revenue=float(data['revenue']) if data.get('revenue') else None,
                cost_of_revenue=float(data['cost_of_revenue']) if data.get('cost_of_revenue') else None,
                gross_profit=float(data['gross_profit']) if data.get('gross_profit') else None,
                operating_expenses=float(data['operating_expenses']) if data.get('operating_expenses') else None,
                ebitda=float(data['ebitda']) if data.get('ebitda') else None,
                depreciation_amortization=float(data['depreciation_amortization']) if data.get('depreciation_amortization') else None,
                ebit=float(data['ebit']) if data.get('ebit') else None,
                interest_expense=float(data['interest_expense']) if data.get('interest_expense') else None,
                pretax_income=float(data['pretax_income']) if data.get('pretax_income') else None,
                income_tax_expense=float(data['income_tax']) if data.get('income_tax') else None,
                net_income=float(data['net_income']) if data.get('net_income') else None,

                # Metadata
                source_page=data.get('source_page'),
                confidence_score=data.get('confidence_score', 0.0),
                currency=data.get('currency', 'USD'),
                unit=data.get('unit', 'millions'),
                extraction_notes=data.get('notes'),
            )

            self.db.add(statement)
            logger.info(f"Stored income statement: {statement.id}")
            return statement.id

        except Exception as e:
            logger.error(f"Failed to store income statement: {e}")
            return None

    def _store_balance_sheet(
        self,
        document_id: uuid.UUID,
        company_id: Optional[str],
        data: Dict,
        validation: Dict
    ) -> Optional[uuid.UUID]:
        """Store balance sheet in database"""
        try:
            period = data.get('period', {})

            statement = ExtractedBalanceSheet(
                id=uuid.uuid4(),
                document_id=document_id,
                company_id=uuid.UUID(company_id) if company_id else None,

                # Period
                period_date=period.get('period_date', ''),
                period_type=PeriodType(period.get('period_type', 'Quarterly')),
                fiscal_year=period.get('fiscal_year', 2025),
                fiscal_quarter=period.get('fiscal_quarter'),

                # Assets
                cash_and_equivalents=float(data['cash_and_equivalents']) if data.get('cash_and_equivalents') else None,
                accounts_receivable=float(data['accounts_receivable']) if data.get('accounts_receivable') else None,
                inventory=float(data['inventory']) if data.get('inventory') else None,
                total_current_assets=float(data['total_current_assets']) if data.get('total_current_assets') else None,
                ppe_net=float(data['ppe_net']) if data.get('ppe_net') else None,
                goodwill=float(data['goodwill']) if data.get('goodwill') else None,
                total_assets=float(data['total_assets']) if data.get('total_assets') else None,

                # Liabilities
                accounts_payable=float(data['accounts_payable']) if data.get('accounts_payable') else None,
                short_term_debt=float(data['short_term_debt']) if data.get('short_term_debt') else None,
                total_current_liabilities=float(data['total_current_liabilities']) if data.get('total_current_liabilities') else None,
                long_term_debt=float(data['long_term_debt']) if data.get('long_term_debt') else None,
                total_liabilities=float(data['total_liabilities']) if data.get('total_liabilities') else None,

                # Equity
                total_equity=float(data['total_equity']) if data.get('total_equity') else None,

                # Metadata
                source_page=data.get('source_page'),
                confidence_score=data.get('confidence_score', 0.0),
                currency=data.get('currency', 'USD'),
                unit=data.get('unit', 'millions'),
            )

            self.db.add(statement)
            logger.info(f"Stored balance sheet: {statement.id}")
            return statement.id

        except Exception as e:
            logger.error(f"Failed to store balance sheet: {e}")
            return None

    def _store_cash_flow(
        self,
        document_id: uuid.UUID,
        company_id: Optional[str],
        data: Dict,
        validation: Dict
    ) -> Optional[uuid.UUID]:
        """Store cash flow statement in database"""
        try:
            period = data.get('period', {})

            statement = ExtractedCashFlow(
                id=uuid.uuid4(),
                document_id=document_id,
                company_id=uuid.UUID(company_id) if company_id else None,

                # Period
                period_date=period.get('period_date', ''),
                period_type=PeriodType(period.get('period_type', 'Quarterly')),
                fiscal_year=period.get('fiscal_year', 2025),
                fiscal_quarter=period.get('fiscal_quarter'),

                # Cash flow fields
                net_income=float(data['net_income']) if data.get('net_income') else None,
                depreciation_amortization=float(data['depreciation_amortization']) if data.get('depreciation_amortization') else None,
                change_in_working_capital=float(data['change_in_working_capital']) if data.get('change_in_working_capital') else None,
                cash_from_operations=float(data['cash_from_operations']) if data.get('cash_from_operations') else None,
                capex=float(data['capex']) if data.get('capex') else None,
                cash_from_investing=float(data['cash_from_investing']) if data.get('cash_from_investing') else None,
                cash_from_financing=float(data['cash_from_financing']) if data.get('cash_from_financing') else None,
                net_change_in_cash=float(data['net_change_in_cash']) if data.get('net_change_in_cash') else None,
                free_cash_flow=float(data['free_cash_flow']) if data.get('free_cash_flow') else None,

                # Metadata
                source_page=data.get('source_page'),
                confidence_score=data.get('confidence_score', 0.0),
                currency=data.get('currency', 'USD'),
                unit=data.get('unit', 'millions'),
            )

            self.db.add(statement)
            logger.info(f"Stored cash flow: {statement.id}")
            return statement.id

        except Exception as e:
            logger.error(f"Failed to store cash flow: {e}")
            return None

    # =====================================================================
    # HISTORICAL VALUATION TRACKING
    # =====================================================================

    def create_valuation_snapshot(
        self,
        company_id: str,
        model_type: str,
        enterprise_value: float,
        equity_value: float,
        dcf_model_id: Optional[str] = None,
        lbo_model_id: Optional[str] = None,
        key_assumptions: Optional[Dict] = None,
        user_id: Optional[str] = None
    ) -> ValuationSnapshot:
        """
        Create a historical valuation snapshot

        This allows tracking how valuations change over time as new data comes in
        """
        snapshot = ValuationSnapshot(
            id=uuid.uuid4(),
            company_id=uuid.UUID(company_id),
            dcf_model_id=uuid.UUID(dcf_model_id) if dcf_model_id else None,
            lbo_model_id=uuid.UUID(lbo_model_id) if lbo_model_id else None,
            model_type=model_type,
            enterprise_value=enterprise_value,
            equity_value=equity_value,
            key_assumptions=key_assumptions or {},
            created_by=uuid.UUID(user_id) if user_id else None,
        )

        self.db.add(snapshot)
        self.db.commit()

        logger.info(f"Created valuation snapshot: {snapshot.id}")
        return snapshot

    def get_valuation_history(
        self,
        company_id: str,
        model_type: Optional[str] = None,
        limit: int = 50
    ) -> List[ValuationSnapshot]:
        """
        Get historical valuations for a company

        Args:
            company_id: Company UUID
            model_type: Optional filter by model type (DCF, LBO, etc.)
            limit: Maximum number of snapshots to return

        Returns:
            List of valuation snapshots, most recent first
        """
        query = self.db.query(ValuationSnapshot).filter(
            ValuationSnapshot.company_id == uuid.UUID(company_id)
        )

        if model_type:
            query = query.filter(ValuationSnapshot.model_type == model_type)

        snapshots = query.order_by(desc(ValuationSnapshot.snapshot_date)).limit(limit).all()

        return snapshots

    def compare_valuations(
        self,
        baseline_snapshot_id: str,
        comparison_snapshot_id: str,
        user_id: Optional[str] = None
    ) -> ValuationComparison:
        """
        Create a comparison between two valuation snapshots

        Analyzes what drove the change in valuation
        """
        baseline = self.db.query(ValuationSnapshot).get(uuid.UUID(baseline_snapshot_id))
        comparison = self.db.query(ValuationSnapshot).get(uuid.UUID(comparison_snapshot_id))

        if not baseline or not comparison:
            raise ValueError("One or both snapshots not found")

        if baseline.company_id != comparison.company_id:
            raise ValueError("Snapshots must be for the same company")

        # Calculate changes
        ev_change = comparison.enterprise_value - baseline.enterprise_value
        ev_change_pct = (ev_change / baseline.enterprise_value * 100) if baseline.enterprise_value else 0

        equity_change = comparison.equity_value - baseline.equity_value
        equity_change_pct = (equity_change / baseline.equity_value * 100) if baseline.equity_value else 0

        comparison_record = ValuationComparison(
            id=uuid.uuid4(),
            company_id=baseline.company_id,
            baseline_snapshot_id=uuid.UUID(baseline_snapshot_id),
            comparison_snapshot_id=uuid.UUID(comparison_snapshot_id),
            ev_change=ev_change,
            ev_change_pct=ev_change_pct,
            equity_value_change=equity_change,
            equity_value_change_pct=equity_change_pct,
            prepared_by=uuid.UUID(user_id) if user_id else None,
        )

        self.db.add(comparison_record)
        self.db.commit()

        logger.info(f"Created valuation comparison: {comparison_record.id}")
        return comparison_record

    # =====================================================================
    # DOCUMENT MANAGEMENT
    # =====================================================================

    def get_document(self, document_id: str) -> Optional[FinancialDocument]:
        """Get a financial document by ID"""
        return self.db.query(FinancialDocument).get(uuid.UUID(document_id))

    def get_company_documents(
        self,
        company_id: str,
        document_type: Optional[DocumentType] = None,
        limit: int = 100
    ) -> List[FinancialDocument]:
        """Get all documents for a company"""
        query = self.db.query(FinancialDocument).filter(
            FinancialDocument.company_id == uuid.UUID(company_id)
        )

        if document_type:
            query = query.filter(FinancialDocument.document_type == document_type)

        return query.order_by(desc(FinancialDocument.upload_date)).limit(limit).all()

    def get_extracted_statements(
        self,
        document_id: str
    ) -> Dict:
        """Get all extracted financial statements for a document"""
        doc = self.get_document(document_id)
        if not doc:
            return {}

        return {
            'document': {
                'id': str(doc.id),
                'name': doc.document_name,
                'company_name': doc.company_name,
                'extraction_status': doc.extraction_status.value,
                'confidence': doc.extraction_confidence,
            },
            'income_statements': [
                self._serialize_income_statement(stmt)
                for stmt in doc.income_statements
            ],
            'balance_sheets': [
                self._serialize_balance_sheet(stmt)
                for stmt in doc.balance_sheets
            ],
            'cash_flows': [
                self._serialize_cash_flow(stmt)
                for stmt in doc.cash_flows
            ],
        }

    def _serialize_income_statement(self, stmt: ExtractedIncomeStatement) -> Dict:
        """Convert income statement model to dictionary"""
        return {
            'id': str(stmt.id),
            'period_date': stmt.period_date,
            'period_type': stmt.period_type.value,
            'fiscal_year': stmt.fiscal_year,
            'fiscal_quarter': stmt.fiscal_quarter,
            'revenue': stmt.revenue,
            'ebitda': stmt.ebitda,
            'net_income': stmt.net_income,
            'confidence_score': stmt.confidence_score,
        }

    def _serialize_balance_sheet(self, stmt: ExtractedBalanceSheet) -> Dict:
        """Convert balance sheet model to dictionary"""
        return {
            'id': str(stmt.id),
            'period_date': stmt.period_date,
            'period_type': stmt.period_type.value,
            'fiscal_year': stmt.fiscal_year,
            'total_assets': stmt.total_assets,
            'total_liabilities': stmt.total_liabilities,
            'total_equity': stmt.total_equity,
            'confidence_score': stmt.confidence_score,
        }

    def _serialize_cash_flow(self, stmt: ExtractedCashFlow) -> Dict:
        """Convert cash flow model to dictionary"""
        return {
            'id': str(stmt.id),
            'period_date': stmt.period_date,
            'period_type': stmt.period_type.value,
            'fiscal_year': stmt.fiscal_year,
            'cash_from_operations': stmt.cash_from_operations,
            'capex': stmt.capex,
            'free_cash_flow': stmt.free_cash_flow,
            'confidence_score': stmt.confidence_score,
        }


# Convenience functions for API use
def get_pdf_service(db: Session) -> PDFExtractionService:
    """Factory function to create PDF extraction service"""
    return PDFExtractionService(db)
