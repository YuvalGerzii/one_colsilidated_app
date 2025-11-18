"""
AI-Enhanced PDF Financial Extractor
====================================
Uses GPT-4 Vision API for intelligent extraction when traditional parsing fails.
Falls back to pdfplumber for standard extraction.
"""

import base64
import os
from typing import Dict, List, Optional
import json
import logging
from decimal import Decimal

# Note: In production, you'd use: from openai import OpenAI
# For now, we'll create a mock interface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIFinancialExtractor:
    """Enhanced extractor using AI vision models"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        # In production: self.client = OpenAI(api_key=self.api_key)
        
    def extract_with_vision(self, pdf_path: str, page_num: int) -> Dict:
        """
        Extract financial data using GPT-4 Vision
        
        Args:
            pdf_path: Path to PDF
            page_num: Page number to extract
            
        Returns:
            Extracted financial data as dictionary
        """
        logger.info(f"Using AI vision to extract from page {page_num}")
        
        # Convert PDF page to image
        image_data = self._pdf_page_to_image(pdf_path, page_num)
        
        # Create prompt for financial statement extraction
        prompt = self._create_extraction_prompt()
        
        # Call GPT-4 Vision (mock for now)
        response = self._call_vision_api(image_data, prompt)
        
        return response
    
    def _pdf_page_to_image(self, pdf_path: str, page_num: int) -> str:
        """Convert PDF page to base64-encoded image"""
        try:
            import pdf2image
            from PIL import Image
            import io
            
            # Convert specific page to image
            images = pdf2image.convert_from_path(
                pdf_path,
                first_page=page_num,
                last_page=page_num,
                dpi=300
            )
            
            if not images:
                raise ValueError(f"Failed to convert page {page_num}")
            
            # Convert to base64
            img = images[0]
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except ImportError:
            logger.error("pdf2image not installed. Install with: pip install pdf2image")
            raise
    
    def _create_extraction_prompt(self) -> str:
        """Create prompt for AI extraction"""
        return """
You are a financial analyst AI specialized in extracting structured data from financial statements.

Analyze this image of a financial statement and extract the following information:

**If this is an Income Statement (P&L), extract:**
- Revenue (Total Revenue, Net Sales, Operating Revenue)
- Cost of Revenue (COGS, Cost of Sales)
- Gross Profit
- Operating Expenses (R&D, SG&A, Marketing, G&A)
- EBITDA
- Depreciation & Amortization
- EBIT / Operating Income
- Interest Expense
- Interest Income
- Pretax Income (Income Before Tax, EBT)
- Income Tax (Tax Expense, Provision for Income Taxes)
- Net Income (Net Earnings, Profit)

**If this is a Balance Sheet, extract:**
ASSETS:
- Cash and Cash Equivalents
- Marketable Securities
- Accounts Receivable
- Inventory
- Total Current Assets
- Property, Plant & Equipment (Net)
- Goodwill
- Intangible Assets
- Total Assets

LIABILITIES:
- Accounts Payable
- Short-term Debt
- Total Current Liabilities
- Long-term Debt
- Total Liabilities

EQUITY:
- Common Stock
- Retained Earnings
- Total Equity

**If this is a Cash Flow Statement, extract:**
- Cash from Operations (Operating Cash Flow)
- Capital Expenditures (CapEx)
- Cash from Investing
- Cash from Financing
- Dividends Paid
- Share Repurchases
- Free Cash Flow

**Period Information:**
- Period End Date (e.g., September 30, 2025)
- Period Type (Quarterly, Annual, TTM, Nine Months, etc.)
- Fiscal Year and Quarter (if applicable)

**Return the data as valid JSON with this structure:**
```json
{
  "statement_type": "income_statement|balance_sheet|cash_flow",
  "period": {
    "period_date": "YYYY-MM-DD",
    "period_type": "Quarterly|Annual|TTM",
    "fiscal_year": 2025,
    "fiscal_quarter": 3
  },
  "data": {
    // All extracted line items as key-value pairs
    // Use null for items not present or not applicable
    // Values should be in millions or thousands (note the unit)
  },
  "metadata": {
    "currency": "USD",
    "unit": "millions|thousands|actual",
    "confidence": 0.95,
    "notes": "Any relevant notes about the extraction"
  }
}
```

**Important Guidelines:**
1. Extract ALL numbers as raw values (without $ or commas)
2. Preserve negative values with minus sign (-)
3. Note the unit (millions, thousands, or actual amount)
4. If a value appears in parentheses (), treat it as negative
5. Only extract data that is clearly visible - use null for missing items
6. Include a confidence score (0-1) for the extraction quality
7. If multiple periods are shown, extract the MOST RECENT period
8. Look for footnotes or annotations that clarify the numbers

Return ONLY the JSON object, no additional text.
"""
    
    def _call_vision_api(self, image_data: str, prompt: str) -> Dict:
        """
        Call GPT-4 Vision API
        
        In production, this would be:
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data}}
                ]
            }],
            max_tokens=2000,
            temperature=0.1
        )
        """
        # Mock response for demonstration
        logger.warning("Using mock AI response - in production, would call OpenAI API")
        
        return {
            "statement_type": "income_statement",
            "period": {
                "period_date": "2025-09-30",
                "period_type": "Quarterly",
                "fiscal_year": 2025,
                "fiscal_quarter": 3
            },
            "data": {
                "revenue": 51242,
                "cost_of_revenue": 9206,
                "gross_profit": None,
                "operating_expenses": 21501,
                "ebit": 20535,
                "net_income": 2709
            },
            "metadata": {
                "currency": "USD",
                "unit": "millions",
                "confidence": 0.92,
                "notes": "Mock extraction - replace with actual API call"
            }
        }


class HybridExtractor:
    """
    Hybrid extraction approach:
    1. Try pdfplumber first (fast, no API costs)
    2. Fall back to AI vision for complex layouts
    3. Validate and merge results
    """
    
    def __init__(self, pdf_path: str, use_ai: bool = False, api_key: Optional[str] = None):
        self.pdf_path = pdf_path
        self.use_ai = use_ai
        self.ai_extractor = AIFinancialExtractor(api_key) if use_ai else None
    
    def extract(self) -> Dict:
        """Extract using hybrid approach"""
        results = {
            'extraction_method': 'hybrid',
            'traditional_extraction': None,
            'ai_extraction': None,
            'final_data': None
        }
        
        # Step 1: Traditional extraction
        logger.info("Step 1: Attempting traditional PDF parsing...")
        try:
            from pdf_financial_extractor import extract_financial_statements
            traditional_results = extract_financial_statements(self.pdf_path)
            results['traditional_extraction'] = traditional_results
            
            # Check quality
            confidence = self._assess_extraction_quality(traditional_results)
            logger.info(f"Traditional extraction confidence: {confidence:.2%}")
            
            if confidence >= 0.85:
                logger.info("Traditional extraction sufficient - skipping AI")
                results['final_data'] = traditional_results
                return results
                
        except Exception as e:
            logger.warning(f"Traditional extraction failed: {e}")
        
        # Step 2: AI extraction (if needed and enabled)
        if self.use_ai and self.ai_extractor:
            logger.info("Step 2: Using AI vision for enhanced extraction...")
            try:
                # Extract from key pages (typically first few pages have statements)
                ai_results = []
                for page_num in range(1, min(6, self._get_page_count() + 1)):
                    page_data = self.ai_extractor.extract_with_vision(
                        self.pdf_path, 
                        page_num
                    )
                    if page_data and page_data.get('data'):
                        ai_results.append(page_data)
                
                results['ai_extraction'] = ai_results
                
                # Merge traditional and AI results
                results['final_data'] = self._merge_results(
                    results['traditional_extraction'],
                    ai_results
                )
                
            except Exception as e:
                logger.error(f"AI extraction failed: {e}")
                results['final_data'] = results['traditional_extraction']
        else:
            results['final_data'] = results['traditional_extraction']
        
        return results
    
    def _assess_extraction_quality(self, results: Dict) -> float:
        """Assess quality of extraction"""
        if not results:
            return 0.0
        
        # Count extracted data points
        total_statements = 0
        total_confidence = 0.0
        
        for stmt_type in ['income_statements', 'balance_sheets', 'cash_flows']:
            statements = results.get(stmt_type, [])
            total_statements += len(statements)
            
            for stmt in statements:
                total_confidence += stmt.get('confidence_score', 0.0)
        
        if total_statements == 0:
            return 0.0
        
        return total_confidence / total_statements
    
    def _merge_results(self, traditional: Dict, ai: List[Dict]) -> Dict:
        """Merge traditional and AI results, preferring higher confidence"""
        if not traditional and not ai:
            return {}
        
        if not ai:
            return traditional
        
        if not traditional:
            return {'ai_extracted_data': ai}
        
        # In production, implement sophisticated merging logic
        # For now, keep both
        merged = traditional.copy()
        merged['ai_enhanced_data'] = ai
        
        return merged
    
    def _get_page_count(self) -> int:
        """Get number of pages in PDF"""
        import pdfplumber
        with pdfplumber.open(self.pdf_path) as pdf:
            return len(pdf.pages)


# Confidence scoring system
class ExtractionValidator:
    """Validates extracted financial data"""
    
    @staticmethod
    def validate_income_statement(data: Dict) -> tuple[bool, List[str]]:
        """
        Validate income statement data
        
        Returns:
            (is_valid, list_of_issues)
        """
        issues = []
        
        # Check for required fields
        required = ['revenue', 'net_income']
        for field in required:
            if not data.get(field):
                issues.append(f"Missing required field: {field}")
        
        # Logical checks
        revenue = data.get('revenue')
        net_income = data.get('net_income')
        gross_profit = data.get('gross_profit')
        
        if revenue and gross_profit:
            if abs(gross_profit) > abs(revenue):
                issues.append("Gross profit exceeds revenue - possible error")
        
        if revenue and net_income:
            if abs(net_income) > abs(revenue):
                issues.append("Net income exceeds revenue - possible error")
        
        # Check for unrealistic values (e.g., revenue = 0)
        if revenue == 0:
            issues.append("Revenue is zero - possible extraction error")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    @staticmethod
    def validate_balance_sheet(data: Dict) -> tuple[bool, List[str]]:
        """Validate balance sheet data"""
        issues = []
        
        # Fundamental accounting equation: Assets = Liabilities + Equity
        assets = data.get('total_assets')
        liabilities = data.get('total_liabilities')
        equity = data.get('total_equity')
        
        if assets and liabilities and equity:
            calculated_assets = liabilities + equity
            diff_pct = abs(assets - calculated_assets) / assets if assets != 0 else 0
            
            if diff_pct > 0.01:  # Allow 1% difference for rounding
                issues.append(
                    f"Balance sheet doesn't balance: "
                    f"Assets ({assets}) != Liabilities ({liabilities}) + Equity ({equity})"
                )
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    @staticmethod
    def validate_cash_flow(data: Dict) -> tuple[bool, List[str]]:
        """Validate cash flow data"""
        issues = []
        
        # Check reconciliation
        ops = data.get('cash_from_operations')
        inv = data.get('cash_from_investing')
        fin = data.get('cash_from_financing')
        net_change = data.get('net_change_in_cash')
        
        if all([ops, inv, fin, net_change]):
            calculated_change = ops + inv + fin
            diff_pct = abs(net_change - calculated_change) / abs(net_change) if net_change != 0 else 0
            
            if diff_pct > 0.01:
                issues.append(
                    f"Cash flow doesn't reconcile: "
                    f"Sum of activities ({calculated_change}) != Net change ({net_change})"
                )
        
        is_valid = len(issues) == 0
        return is_valid, issues


if __name__ == '__main__':
    # Example usage
    pdf_path = '/mnt/user-data/uploads/Meta-Reports-Third-Quarter-2025-Results-2025.pdf'
    
    # Create hybrid extractor
    extractor = HybridExtractor(pdf_path, use_ai=False)  # Set to True to enable AI
    
    # Extract data
    results = extractor.extract()
    
    # Print results
    print(json.dumps(results, indent=2, default=str))
