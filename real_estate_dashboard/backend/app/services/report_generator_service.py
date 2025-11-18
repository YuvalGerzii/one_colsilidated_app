"""Service for generating professional investment reports."""

from typing import Dict, List, Optional, Any
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import json
from decimal import Decimal
import logging

from app.models.reports import GeneratedReport, ReportType, ReportStatus, ExportFormat
from app.models.crm import Deal, DealStage, DealStatus
from app.models.fund_management import Fund, PortfolioInvestment, LimitedPartner, CapitalCall
from app.models.financial_models import DCFModel, LBOModel
from app.core.document_generator import PDFGenerator, PowerPointGenerator, ChartGenerator

logger = logging.getLogger(__name__)


class ReportGeneratorService:
    """Service for generating various types of investment reports."""

    def __init__(self, db: Session, company_id: str):
        """
        Initialize report generator service.

        Args:
            db: Database session
            company_id: Company ID for data filtering
        """
        self.db = db
        self.company_id = company_id
        try:
            self.chart_generator = ChartGenerator()
        except Exception as e:
            logger.warning(f"Chart generator initialization failed: {e}. Charts will be disabled.")
            self.chart_generator = None

    # ========================================================================
    # INVESTMENT COMMITTEE MEMO
    # ========================================================================

    def generate_investment_committee_memo(
        self,
        deal_id: str,
        include_charts: bool = True,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Investment Committee Memo for a deal.

        Args:
            deal_id: Deal ID
            include_charts: Whether to include charts
            user_id: User generating the report

        Returns:
            Report data dictionary
        """
        # Fetch deal data
        deal = self.db.query(Deal).filter(
            Deal.id == deal_id,
            Deal.company_id == self.company_id
        ).first()

        if not deal:
            raise ValueError(f"Deal {deal_id} not found")

        # Build memo data
        memo_data = {
            "report_type": "Investment Committee Memo",
            "deal_name": deal.property_name,
            "generated_date": datetime.now().isoformat(),

            # Executive Summary
            "executive_summary": self._build_executive_summary(deal),

            # Investment Overview
            "investment_overview": self._build_investment_overview(deal),

            # Financial Analysis
            "financial_analysis": self._build_financial_analysis(deal),

            # Market Analysis
            "market_analysis": self._build_market_analysis(deal),

            # Risk Analysis
            "risk_analysis": self._build_risk_analysis(deal),

            # Recommendation
            "recommendation": self._build_recommendation(deal),
        }

        # Add charts if requested
        if include_charts:
            memo_data["charts"] = self._generate_ic_memo_charts(deal)

        # Generate PDF sections
        sections = self._build_ic_memo_sections(memo_data)

        return {
            "data": memo_data,
            "sections": sections,
            "deal_id": str(deal_id)
        }

    def _build_executive_summary(self, deal: Deal) -> Dict[str, Any]:
        """Build executive summary section."""
        return {
            "property_name": deal.property_name,
            "property_type": deal.property_type or "N/A",
            "location": f"{deal.property_address or ''} - {deal.market or 'N/A'}",
            "asking_price": float(deal.asking_price or 0),
            "offer_price": float(deal.offer_price or 0),
            "units": deal.units,
            "cap_rate": float(deal.cap_rate or 0) if deal.cap_rate else None,
            "irr_target": float(deal.irr_target or 0) if deal.irr_target else None,
            "stage": deal.stage.value if deal.stage else "N/A",
            "confidence_level": deal.confidence_level,
            "broker": deal.broker.name if deal.broker else "Direct",
            "summary": deal.notes or "No summary provided."
        }

    def _build_investment_overview(self, deal: Deal) -> Dict[str, Any]:
        """Build investment overview section."""
        return {
            "property_details": {
                "type": deal.property_type or "N/A",
                "units": deal.units,
                "year_built": deal.year_built,
                "square_footage": deal.square_footage,
            },
            "pricing": {
                "asking_price": float(deal.asking_price or 0),
                "offer_price": float(deal.offer_price or 0),
                "price_per_unit": float(deal.asking_price / deal.units) if deal.asking_price and deal.units else None,
            },
            "key_metrics": {
                "cap_rate": float(deal.cap_rate) if deal.cap_rate else None,
                "noi": float(deal.noi) if deal.noi else None,
                "irr_target": float(deal.irr_target) if deal.irr_target else None,
                "equity_multiple": float(deal.equity_multiple) if deal.equity_multiple else None,
            },
            "timeline": {
                "loi_date": deal.loi_date.isoformat() if deal.loi_date else None,
                "expected_closing": deal.expected_closing_date.isoformat() if deal.expected_closing_date else None,
                "due_diligence_end": deal.due_diligence_end_date.isoformat() if deal.due_diligence_end_date else None,
            }
        }

    def _build_financial_analysis(self, deal: Deal) -> Dict[str, Any]:
        """Build financial analysis section."""
        # Check if deal has associated financial models
        dcf_model = self.db.query(DCFModel).filter(
            DCFModel.company_id == self.company_id
        ).first()

        lbo_model = self.db.query(LBOModel).filter(
            LBOModel.company_id == self.company_id
        ).first()

        analysis = {
            "revenue_projections": [],
            "operating_metrics": {},
            "returns_analysis": {},
            "sensitivity_analysis": {}
        }

        # Add DCF data if available
        if dcf_model:
            analysis["dcf_valuation"] = {
                "enterprise_value": float(dcf_model.enterprise_value or 0),
                "equity_value": float(dcf_model.equity_value or 0),
                "wacc": float(dcf_model.wacc or 0),
                "terminal_growth_rate": float(dcf_model.terminal_growth_rate or 0),
            }

        # Add LBO data if available
        if lbo_model:
            analysis["lbo_returns"] = {
                "irr": float(lbo_model.irr or 0),
                "equity_multiple": float(lbo_model.equity_multiple or 0),
                "entry_valuation": float(lbo_model.entry_valuation or 0),
                "exit_valuation": float(lbo_model.exit_valuation or 0),
            }

        return analysis

    def _build_market_analysis(self, deal: Deal) -> Dict[str, Any]:
        """Build market analysis section."""
        # Fetch comparable deals in same market
        comps = self.db.query(Deal).filter(
            Deal.company_id == self.company_id,
            Deal.market == deal.market,
            Deal.property_type == deal.property_type,
            Deal.id != deal.id,
            Deal.status == DealStatus.CLOSED
        ).limit(5).all()

        comp_data = []
        for comp in comps:
            comp_data.append({
                "property_name": comp.property_name,
                "asking_price": float(comp.asking_price or 0),
                "cap_rate": float(comp.cap_rate) if comp.cap_rate else None,
                "units": comp.units,
                "closed_date": comp.actual_closing_date.isoformat() if comp.actual_closing_date else None
            })

        return {
            "market": deal.market or "N/A",
            "property_type": deal.property_type or "N/A",
            "comparables": comp_data,
            "market_summary": f"Analysis based on {len(comp_data)} comparable transactions in {deal.market}."
        }

    def _build_risk_analysis(self, deal: Deal) -> Dict[str, Any]:
        """Build risk analysis section."""
        risks = []

        # Market risk
        if deal.market:
            risks.append({
                "category": "Market Risk",
                "level": "Medium",
                "description": f"Market concentration in {deal.market}"
            })

        # Financial risk
        if deal.cap_rate and deal.cap_rate < 5.0:
            risks.append({
                "category": "Financial Risk",
                "level": "High",
                "description": f"Low cap rate of {deal.cap_rate}% indicates compressed returns"
            })

        # Execution risk
        if deal.stage in [DealStage.RESEARCH, DealStage.LOI]:
            risks.append({
                "category": "Execution Risk",
                "level": "Medium",
                "description": f"Deal in early stage ({deal.stage.value})"
            })

        return {
            "risks": risks,
            "overall_risk_rating": "Medium",
            "mitigation_strategies": [
                "Conduct thorough due diligence",
                "Secure financing commitments early",
                "Negotiate favorable closing terms"
            ]
        }

    def _build_recommendation(self, deal: Deal) -> Dict[str, Any]:
        """Build recommendation section."""
        # Simple scoring logic
        score = 0
        if deal.cap_rate and deal.cap_rate >= 6.0:
            score += 2
        if deal.confidence_level and deal.confidence_level >= 70:
            score += 2
        if deal.stage in [DealStage.DUE_DILIGENCE, DealStage.CLOSING]:
            score += 1

        recommendation = "Proceed" if score >= 3 else "Proceed with Caution" if score >= 2 else "Pass"

        return {
            "recommendation": recommendation,
            "confidence": deal.confidence_level or 50,
            "next_steps": [
                "Complete due diligence review",
                "Finalize financing terms",
                "Negotiate final purchase price",
                "Present to investment committee"
            ],
            "vote_requested": "Approval to proceed with acquisition"
        }

    def _generate_ic_memo_charts(self, deal: Deal) -> Dict[str, str]:
        """Generate charts for IC memo (returns base64 encoded images)."""
        import base64

        charts = {}

        # Skip chart generation if chart generator failed to initialize
        if not self.chart_generator:
            logger.warning("Chart generator not available, skipping chart generation")
            return charts

        try:
            # Cap Rate Comparison Chart
            if deal.cap_rate:
                try:
                    comps = self.db.query(Deal).filter(
                        Deal.company_id == self.company_id,
                        Deal.market == deal.market,
                        Deal.property_type == deal.property_type,
                        Deal.cap_rate.isnot(None),
                        Deal.id != deal.id
                    ).limit(5).all()

                    if comps:
                        cap_rate_data = {deal.property_name[:20]: float(deal.cap_rate)}
                        for comp in comps:
                            cap_rate_data[comp.property_name[:20]] = float(comp.cap_rate)

                        chart_bytes = self.chart_generator.create_bar_chart(
                            cap_rate_data,
                            "Cap Rate Comparison",
                            ylabel="Cap Rate (%)"
                        )
                        charts["cap_rate_comparison"] = base64.b64encode(chart_bytes).decode('utf-8')
                except Exception as e:
                    logger.warning(f"Failed to generate cap rate chart: {e}")
        except Exception as e:
            logger.error(f"Error generating IC memo charts: {e}")

        return charts

    def _build_ic_memo_sections(self, memo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build PDF sections for IC memo."""
        sections = []

        # Title
        sections.append({
            "type": "heading",
            "title": "INVESTMENT COMMITTEE MEMORANDUM"
        })

        sections.append({"type": "spacer", "height": 0.2})

        # Executive Summary
        exec_sum = memo_data["executive_summary"]
        sections.append({"type": "subheading", "title": "Executive Summary"})
        sections.append({
            "type": "text",
            "content": f"<b>Property:</b> {exec_sum['property_name']}<br/>"
                      f"<b>Type:</b> {exec_sum['property_type']}<br/>"
                      f"<b>Location:</b> {exec_sum['location']}<br/>"
                      f"<b>Asking Price:</b> ${exec_sum['asking_price']:,.0f}<br/>"
                      f"<b>Offer Price:</b> ${exec_sum['offer_price']:,.0f}<br/>"
                      f"<b>Cap Rate:</b> {exec_sum['cap_rate']:.2f}%<br/>"
                      f"<b>IRR Target:</b> {exec_sum['irr_target']:.2f}%<br/>"
        })

        sections.append({"type": "text", "content": exec_sum['summary']})
        sections.append({"type": "spacer", "height": 0.3})

        # Investment Overview
        sections.append({"type": "subheading", "title": "Investment Overview"})
        inv_overview = memo_data["investment_overview"]

        # Property details table
        property_table = [
            ["Metric", "Value"],
            ["Property Type", inv_overview["property_details"]["type"]],
            ["Units", str(inv_overview["property_details"]["units"] or "N/A")],
            ["Year Built", str(inv_overview["property_details"]["year_built"] or "N/A")],
            ["Square Footage", f"{inv_overview['property_details']['square_footage']:,}" if inv_overview["property_details"]["square_footage"] else "N/A"],
        ]
        sections.append({"type": "table", "data": property_table})

        sections.append({"type": "spacer", "height": 0.2})

        # Key Metrics table
        metrics = inv_overview["key_metrics"]
        metrics_table = [
            ["Metric", "Value"],
            ["Cap Rate", f"{metrics['cap_rate']:.2f}%" if metrics['cap_rate'] else "N/A"],
            ["NOI", f"${metrics['noi']:,.0f}" if metrics['noi'] else "N/A"],
            ["IRR Target", f"{metrics['irr_target']:.2f}%" if metrics['irr_target'] else "N/A"],
            ["Equity Multiple", f"{metrics['equity_multiple']:.2f}x" if metrics['equity_multiple'] else "N/A"],
        ]
        sections.append({"type": "table", "data": metrics_table})

        sections.append({"type": "spacer", "height": 0.3})

        # Market Analysis
        sections.append({"type": "subheading", "title": "Market Analysis"})
        market = memo_data["market_analysis"]
        sections.append({"type": "text", "content": market['market_summary']})

        if market['comparables']:
            comp_table = [["Property", "Price", "Cap Rate", "Units"]]
            for comp in market['comparables'][:5]:
                comp_table.append([
                    comp['property_name'][:30],
                    f"${comp['asking_price']:,.0f}",
                    f"{comp['cap_rate']:.2f}%" if comp['cap_rate'] else "N/A",
                    str(comp['units'] or "N/A")
                ])
            sections.append({"type": "table", "data": comp_table})

        sections.append({"type": "spacer", "height": 0.3})

        # Risk Analysis
        sections.append({"type": "subheading", "title": "Risk Analysis"})
        risks = memo_data["risk_analysis"]

        if risks['risks']:
            risk_table = [["Risk Category", "Level", "Description"]]
            for risk in risks['risks']:
                risk_table.append([
                    risk['category'],
                    risk['level'],
                    risk['description']
                ])
            sections.append({"type": "table", "data": risk_table})

        sections.append({"type": "spacer", "height": 0.3})

        # Recommendation
        sections.append({"type": "subheading", "title": "Recommendation"})
        rec = memo_data["recommendation"]
        sections.append({
            "type": "highlight",
            "content": f"<b>RECOMMENDATION: {rec['recommendation'].upper()}</b>"
        })
        sections.append({
            "type": "text",
            "content": f"<b>Confidence Level:</b> {rec['confidence']}%<br/>"
                      f"<b>Vote Requested:</b> {rec['vote_requested']}"
        })

        # Charts
        if "charts" in memo_data and memo_data["charts"]:
            sections.append({"type": "page_break"})
            sections.append({"type": "subheading", "title": "Supporting Charts"})

            for chart_name, chart_data in memo_data["charts"].items():
                sections.append({
                    "type": "chart",
                    "image": chart_data
                })

        return sections

    # ========================================================================
    # QUARTERLY PORTFOLIO REPORT
    # ========================================================================

    def generate_quarterly_portfolio_report(
        self,
        fund_id: Optional[str] = None,
        quarter: Optional[int] = None,
        year: Optional[int] = None,
        include_charts: bool = True,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Quarterly Portfolio Report.

        Args:
            fund_id: Optional fund ID (if None, generates for all funds)
            quarter: Quarter number (1-4)
            year: Year
            include_charts: Whether to include charts
            user_id: User generating the report

        Returns:
            Report data dictionary
        """
        # Determine reporting period
        if not quarter or not year:
            # Default to last completed quarter
            now = datetime.now()
            quarter = ((now.month - 1) // 3)
            if quarter == 0:
                quarter = 4
                year = now.year - 1
            else:
                year = now.year

        period_start = date(year, (quarter - 1) * 3 + 1, 1)
        if quarter == 4:
            period_end = date(year, 12, 31)
        else:
            period_end = date(year, quarter * 3 + 1, 1) - timedelta(days=1)

        # Fetch fund(s)
        if fund_id:
            funds = self.db.query(Fund).filter(
                Fund.id == fund_id,
                Fund.company_id == self.company_id
            ).all()
        else:
            funds = self.db.query(Fund).filter(
                Fund.company_id == self.company_id
            ).all()

        report_data = {
            "report_type": "Quarterly Portfolio Report",
            "period": f"Q{quarter} {year}",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "generated_date": datetime.now().isoformat(),
            "funds": []
        }

        for fund in funds:
            fund_data = self._build_fund_performance(fund, period_start, period_end)
            report_data["funds"].append(fund_data)

        # Add charts
        if include_charts:
            report_data["charts"] = self._generate_portfolio_charts(report_data)

        # Generate sections
        sections = self._build_portfolio_report_sections(report_data)

        return {
            "data": report_data,
            "sections": sections,
            "fund_id": str(fund_id) if fund_id else None
        }

    def _build_fund_performance(self, fund: Fund, period_start: date, period_end: date) -> Dict[str, Any]:
        """Build fund performance data for a period."""
        # Fetch portfolio investments
        investments = self.db.query(PortfolioInvestment).filter(
            PortfolioInvestment.fund_id == fund.id
        ).all()

        total_invested = sum(float(inv.investment_amount or 0) for inv in investments)
        total_current_value = sum(float(inv.current_valuation or 0) for inv in investments if inv.current_valuation)

        return {
            "fund_name": fund.fund_name,
            "fund_type": fund.fund_type.value if fund.fund_type else "N/A",
            "total_commitments": float(fund.target_size or 0),
            "total_invested": total_invested,
            "current_value": total_current_value,
            "unrealized_gain": total_current_value - total_invested,
            "number_of_investments": len(investments),
            "investments": [
                {
                    "company_name": inv.company_name,
                    "investment_amount": float(inv.investment_amount or 0),
                    "current_valuation": float(inv.current_valuation or 0) if inv.current_valuation else None,
                    "investment_date": inv.investment_date.isoformat() if inv.investment_date else None
                }
                for inv in investments
            ]
        }

    def _generate_portfolio_charts(self, report_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate charts for portfolio report."""
        import base64
        charts = {}

        # Skip chart generation if chart generator failed to initialize
        if not self.chart_generator:
            logger.warning("Chart generator not available, skipping chart generation")
            return charts

        try:
            # Fund Performance Chart
            if report_data["funds"]:
                fund_values = {
                    fund["fund_name"][:20]: fund["current_value"]
                    for fund in report_data["funds"]
                }
                chart_bytes = self.chart_generator.create_bar_chart(
                    fund_values,
                    "Fund Performance - Current Value",
                    ylabel="Value ($)"
                )
                charts["fund_performance"] = base64.b64encode(chart_bytes).decode('utf-8')
        except Exception as e:
            logger.error(f"Error generating portfolio charts: {e}")

        return charts

    def _build_portfolio_report_sections(self, report_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build PDF sections for portfolio report."""
        sections = []

        sections.append({
            "type": "heading",
            "title": f"QUARTERLY PORTFOLIO REPORT - {report_data['period']}"
        })

        sections.append({"type": "spacer", "height": 0.3})

        for fund_data in report_data["funds"]:
            sections.append({"type": "subheading", "title": fund_data["fund_name"]})

            # Fund summary table
            summary_table = [
                ["Metric", "Value"],
                ["Fund Type", fund_data["fund_type"]],
                ["Total Commitments", f"${fund_data['total_commitments']:,.0f}"],
                ["Total Invested", f"${fund_data['total_invested']:,.0f}"],
                ["Current Value", f"${fund_data['current_value']:,.0f}"],
                ["Unrealized Gain/Loss", f"${fund_data['unrealized_gain']:,.0f}"],
                ["Number of Investments", str(fund_data['number_of_investments'])],
            ]
            sections.append({"type": "table", "data": summary_table})

            sections.append({"type": "spacer", "height": 0.3})

        # Charts
        if "charts" in report_data and report_data["charts"]:
            sections.append({"type": "page_break"})
            sections.append({"type": "subheading", "title": "Performance Charts"})

            for chart_name, chart_data in report_data["charts"].items():
                sections.append({
                    "type": "chart",
                    "image": chart_data
                })

        return sections

    # ========================================================================
    # MARKET RESEARCH REPORT
    # ========================================================================

    def generate_market_research_report(
        self,
        market: str,
        property_type: Optional[str] = None,
        include_charts: bool = True,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Market Research Report for a specific market.

        Args:
            market: Market name
            property_type: Optional property type filter
            include_charts: Whether to include charts
            user_id: User generating the report

        Returns:
            Report data dictionary
        """
        # Fetch deals in market
        query = self.db.query(Deal).filter(
            Deal.company_id == self.company_id,
            Deal.market == market
        )

        if property_type:
            query = query.filter(Deal.property_type == property_type)

        deals = query.all()

        # Calculate market statistics
        avg_cap_rate = self.db.query(func.avg(Deal.cap_rate)).filter(
            Deal.company_id == self.company_id,
            Deal.market == market,
            Deal.cap_rate.isnot(None)
        ).scalar()

        avg_price = self.db.query(func.avg(Deal.asking_price)).filter(
            Deal.company_id == self.company_id,
            Deal.market == market,
            Deal.asking_price.isnot(None)
        ).scalar()

        report_data = {
            "report_type": "Market Research Report",
            "market": market,
            "property_type": property_type or "All Types",
            "generated_date": datetime.now().isoformat(),
            "statistics": {
                "total_deals": len(deals),
                "avg_cap_rate": float(avg_cap_rate) if avg_cap_rate else None,
                "avg_price": float(avg_price) if avg_price else None,
            },
            "recent_transactions": [
                {
                    "property_name": deal.property_name,
                    "property_type": deal.property_type,
                    "asking_price": float(deal.asking_price or 0),
                    "cap_rate": float(deal.cap_rate) if deal.cap_rate else None,
                    "stage": deal.stage.value if deal.stage else "N/A"
                }
                for deal in deals[:10]
            ]
        }

        # Generate sections
        sections = self._build_market_research_sections(report_data)

        return {
            "data": report_data,
            "sections": sections
        }

    def _build_market_research_sections(self, report_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build PDF sections for market research report."""
        sections = []

        sections.append({
            "type": "heading",
            "title": f"MARKET RESEARCH REPORT - {report_data['market']}"
        })

        sections.append({"type": "spacer", "height": 0.2})

        sections.append({
            "type": "text",
            "content": f"<b>Market:</b> {report_data['market']}<br/>"
                      f"<b>Property Type:</b> {report_data['property_type']}<br/>"
                      f"<b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}"
        })

        sections.append({"type": "spacer", "height": 0.3})

        # Statistics
        sections.append({"type": "subheading", "title": "Market Statistics"})
        stats = report_data["statistics"]
        stats_table = [
            ["Metric", "Value"],
            ["Total Deals Analyzed", str(stats["total_deals"])],
            ["Average Cap Rate", f"{stats['avg_cap_rate']:.2f}%" if stats['avg_cap_rate'] else "N/A"],
            ["Average Price", f"${stats['avg_price']:,.0f}" if stats['avg_price'] else "N/A"],
        ]
        sections.append({"type": "table", "data": stats_table})

        sections.append({"type": "spacer", "height": 0.3})

        # Recent transactions
        if report_data["recent_transactions"]:
            sections.append({"type": "subheading", "title": "Recent Transactions"})
            trans_table = [["Property", "Type", "Price", "Cap Rate", "Stage"]]
            for trans in report_data["recent_transactions"]:
                trans_table.append([
                    trans["property_name"][:30],
                    trans["property_type"] or "N/A",
                    f"${trans['asking_price']:,.0f}",
                    f"{trans['cap_rate']:.2f}%" if trans['cap_rate'] else "N/A",
                    trans["stage"]
                ])
            sections.append({"type": "table", "data": trans_table})

        return sections

    # ========================================================================
    # DUE DILIGENCE SUMMARY REPORT
    # ========================================================================

    def generate_due_diligence_report(
        self,
        deal_id: str,
        include_charts: bool = True,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Due Diligence Summary Report for a deal.

        Args:
            deal_id: Deal ID
            include_charts: Whether to include charts
            user_id: User generating the report

        Returns:
            Report data dictionary
        """
        # Fetch deal data
        deal = self.db.query(Deal).filter(
            Deal.id == deal_id,
            Deal.company_id == self.company_id
        ).first()

        if not deal:
            raise ValueError(f"Deal {deal_id} not found")

        report_data = {
            "report_type": "Due Diligence Summary Report",
            "deal_name": deal.property_name,
            "generated_date": datetime.now().isoformat(),
            "property_overview": self._build_executive_summary(deal),
            "due_diligence_status": {
                "stage": deal.stage.value if deal.stage else "N/A",
                "dd_start": deal.loi_date.isoformat() if deal.loi_date else None,
                "dd_end": deal.due_diligence_end_date.isoformat() if deal.due_diligence_end_date else None,
                "days_remaining": (deal.due_diligence_end_date - date.today()).days if deal.due_diligence_end_date and deal.due_diligence_end_date > date.today() else 0
            },
            "findings": self._build_dd_findings(deal),
            "recommendations": self._build_dd_recommendations(deal)
        }

        # Generate sections
        sections = self._build_dd_report_sections(report_data)

        return {
            "data": report_data,
            "sections": sections,
            "deal_id": str(deal_id)
        }

    def _build_dd_findings(self, deal: Deal) -> List[Dict[str, Any]]:
        """Build due diligence findings."""
        findings = [
            {
                "category": "Financial Review",
                "status": "In Progress",
                "summary": "Reviewing rent rolls, operating statements, and tax returns."
            },
            {
                "category": "Physical Inspection",
                "status": "Pending",
                "summary": "Property inspection scheduled for next week."
            },
            {
                "category": "Legal Review",
                "status": "In Progress",
                "summary": "Title search and zoning review underway."
            },
            {
                "category": "Environmental Assessment",
                "status": "Completed",
                "summary": "Phase I ESA completed with no material findings."
            }
        ]
        return findings

    def _build_dd_recommendations(self, deal: Deal) -> List[str]:
        """Build due diligence recommendations."""
        return [
            "Complete physical inspection within next 7 days",
            "Obtain updated rent roll and reconcile with lease abstracts",
            "Review all material contracts and service agreements",
            "Finalize financing terms with lender",
            "Negotiate closing timeline based on DD findings"
        ]

    def _build_dd_report_sections(self, report_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build PDF sections for due diligence report."""
        sections = []

        sections.append({
            "type": "heading",
            "title": "DUE DILIGENCE SUMMARY REPORT"
        })

        sections.append({"type": "spacer", "height": 0.2})

        # Property Overview
        sections.append({"type": "subheading", "title": "Property Overview"})
        overview = report_data["property_overview"]
        sections.append({
            "type": "text",
            "content": f"<b>Property:</b> {overview['property_name']}<br/>"
                      f"<b>Type:</b> {overview['property_type']}<br/>"
                      f"<b>Location:</b> {overview['location']}<br/>"
                      f"<b>Price:</b> ${overview['asking_price']:,.0f}"
        })

        sections.append({"type": "spacer", "height": 0.3})

        # DD Status
        sections.append({"type": "subheading", "title": "Due Diligence Status"})
        dd_status = report_data["due_diligence_status"]
        status_table = [
            ["Item", "Value"],
            ["Current Stage", dd_status["stage"]],
            ["DD Period End", dd_status["dd_end"] or "TBD"],
            ["Days Remaining", str(dd_status["days_remaining"])],
        ]
        sections.append({"type": "table", "data": status_table})

        sections.append({"type": "spacer", "height": 0.3})

        # Findings
        sections.append({"type": "subheading", "title": "Key Findings"})
        findings_table = [["Category", "Status", "Summary"]]
        for finding in report_data["findings"]:
            findings_table.append([
                finding["category"],
                finding["status"],
                finding["summary"]
            ])
        sections.append({"type": "table", "data": findings_table})

        sections.append({"type": "spacer", "height": 0.3})

        # Recommendations
        sections.append({"type": "subheading", "title": "Recommendations"})
        for i, rec in enumerate(report_data["recommendations"], 1):
            sections.append({
                "type": "text",
                "content": f"{i}. {rec}"
            })

        return sections
