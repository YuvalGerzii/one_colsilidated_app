"""
PDF Financial Statement Extractor
==================================
Extracts financial data from PDF statements and maps to database schema.

Supports:
- Income Statements (P&L)
- Balance Sheets
- Cash Flow Statements
- Management Reports
- Scanned PDFs (via OCR)
"""

import pdfplumber
import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from decimal import Decimal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FinancialPeriod:
    """Represents a single financial period"""
    period_date: str  # YYYY-MM-DD
    period_type: str  # "Quarterly", "Annual", "TTM"
    fiscal_year: int
    fiscal_quarter: Optional[int] = None


@dataclass
class IncomeStatementData:
    """Income Statement extracted data"""
    period: FinancialPeriod
    revenue: Optional[Decimal] = None
    cost_of_revenue: Optional[Decimal] = None
    gross_profit: Optional[Decimal] = None
    operating_expenses: Optional[Decimal] = None
    ebitda: Optional[Decimal] = None
    depreciation_amortization: Optional[Decimal] = None
    ebit: Optional[Decimal] = None
    interest_expense: Optional[Decimal] = None
    interest_income: Optional[Decimal] = None
    pretax_income: Optional[Decimal] = None
    income_tax: Optional[Decimal] = None
    net_income: Optional[Decimal] = None
    
    # Additional metrics
    shares_outstanding_basic: Optional[Decimal] = None
    shares_outstanding_diluted: Optional[Decimal] = None
    eps_basic: Optional[Decimal] = None
    eps_diluted: Optional[Decimal] = None
    
    confidence_score: float = 0.0
    source_page: int = 0


@dataclass
class BalanceSheetData:
    """Balance Sheet extracted data"""
    period: FinancialPeriod
    
    # Assets
    cash_and_equivalents: Optional[Decimal] = None
    marketable_securities: Optional[Decimal] = None
    accounts_receivable: Optional[Decimal] = None
    inventory: Optional[Decimal] = None
    other_current_assets: Optional[Decimal] = None
    total_current_assets: Optional[Decimal] = None
    
    ppe_gross: Optional[Decimal] = None
    accumulated_depreciation: Optional[Decimal] = None
    ppe_net: Optional[Decimal] = None
    goodwill: Optional[Decimal] = None
    intangible_assets: Optional[Decimal] = None
    other_noncurrent_assets: Optional[Decimal] = None
    total_assets: Optional[Decimal] = None
    
    # Liabilities
    accounts_payable: Optional[Decimal] = None
    accrued_expenses: Optional[Decimal] = None
    short_term_debt: Optional[Decimal] = None
    current_portion_long_term_debt: Optional[Decimal] = None
    other_current_liabilities: Optional[Decimal] = None
    total_current_liabilities: Optional[Decimal] = None
    
    long_term_debt: Optional[Decimal] = None
    other_noncurrent_liabilities: Optional[Decimal] = None
    total_liabilities: Optional[Decimal] = None
    
    # Equity
    common_stock: Optional[Decimal] = None
    retained_earnings: Optional[Decimal] = None
    treasury_stock: Optional[Decimal] = None
    other_equity: Optional[Decimal] = None
    total_equity: Optional[Decimal] = None
    
    confidence_score: float = 0.0
    source_page: int = 0


@dataclass
class CashFlowData:
    """Cash Flow Statement extracted data"""
    period: FinancialPeriod
    
    # Operating Activities
    net_income: Optional[Decimal] = None
    depreciation_amortization: Optional[Decimal] = None
    stock_based_compensation: Optional[Decimal] = None
    deferred_taxes: Optional[Decimal] = None
    change_in_working_capital: Optional[Decimal] = None
    other_operating_activities: Optional[Decimal] = None
    cash_from_operations: Optional[Decimal] = None
    
    # Investing Activities
    capex: Optional[Decimal] = None
    acquisitions: Optional[Decimal] = None
    purchases_of_investments: Optional[Decimal] = None
    sales_of_investments: Optional[Decimal] = None
    other_investing_activities: Optional[Decimal] = None
    cash_from_investing: Optional[Decimal] = None
    
    # Financing Activities
    debt_issued: Optional[Decimal] = None
    debt_repaid: Optional[Decimal] = None
    equity_issued: Optional[Decimal] = None
    dividends_paid: Optional[Decimal] = None
    share_repurchases: Optional[Decimal] = None
    other_financing_activities: Optional[Decimal] = None
    cash_from_financing: Optional[Decimal] = None
    
    # Summary
    net_change_in_cash: Optional[Decimal] = None
    beginning_cash: Optional[Decimal] = None
    ending_cash: Optional[Decimal] = None
    free_cash_flow: Optional[Decimal] = None
    
    confidence_score: float = 0.0
    source_page: int = 0


class FinancialKeywords:
    """Keywords for identifying financial line items"""
    
    # Income Statement Keywords
    REVENUE = [
        'revenue', 'revenues', 'net sales', 'sales', 'total revenue', 
        'total net sales', 'net revenue', 'operating revenue'
    ]
    
    COST_OF_REVENUE = [
        'cost of revenue', 'cost of sales', 'cost of goods sold', 'cogs',
        'cost of products', 'cost of services'
    ]
    
    GROSS_PROFIT = [
        'gross profit', 'gross margin', 'gross income'
    ]
    
    OPERATING_EXPENSES = [
        'operating expenses', 'operating costs', 'total operating expenses',
        'research and development', 'r&d', 'selling, general and administrative',
        'sg&a', 'marketing and sales', 'general and administrative'
    ]
    
    EBITDA = [
        'ebitda', 'operating income before depreciation',
        'adjusted ebitda', 'normalized ebitda'
    ]
    
    EBIT = [
        'ebit', 'operating income', 'income from operations',
        'operating profit', 'earnings before interest and taxes'
    ]
    
    DEPRECIATION = [
        'depreciation', 'depreciation and amortization', 'd&a',
        'amortization', 'depreciation expense'
    ]
    
    INTEREST_EXPENSE = [
        'interest expense', 'interest paid', 'interest on debt',
        'finance costs', 'financing costs'
    ]
    
    PRETAX_INCOME = [
        'income before taxes', 'pretax income', 'earnings before tax',
        'income before provision for income taxes', 'ebt'
    ]
    
    TAX = [
        'income tax', 'provision for income taxes', 'tax expense',
        'income taxes', 'tax provision'
    ]
    
    NET_INCOME = [
        'net income', 'net earnings', 'profit', 'net profit',
        'bottom line', 'earnings', 'net income attributable'
    ]
    
    # Balance Sheet Keywords
    CASH = [
        'cash', 'cash and cash equivalents', 'cash and equivalents',
        'cash & cash equivalents'
    ]
    
    MARKETABLE_SECURITIES = [
        'marketable securities', 'short-term investments',
        'short term investments', 'available-for-sale securities'
    ]
    
    ACCOUNTS_RECEIVABLE = [
        'accounts receivable', 'receivables', 'trade receivables',
        'accounts receivable, net'
    ]
    
    INVENTORY = [
        'inventory', 'inventories', 'finished goods', 'raw materials'
    ]
    
    TOTAL_CURRENT_ASSETS = [
        'total current assets', 'current assets'
    ]
    
    PPE_NET = [
        'property, plant and equipment', 'property and equipment',
        'fixed assets', 'pp&e', 'ppe', 'property, plant and equipment, net'
    ]
    
    GOODWILL = [
        'goodwill'
    ]
    
    TOTAL_ASSETS = [
        'total assets'
    ]
    
    ACCOUNTS_PAYABLE = [
        'accounts payable', 'trade payables', 'payables'
    ]
    
    SHORT_TERM_DEBT = [
        'short-term debt', 'short term debt', 'current debt',
        'notes payable', 'commercial paper'
    ]
    
    LONG_TERM_DEBT = [
        'long-term debt', 'long term debt', 'term debt',
        'bonds payable', 'senior debt'
    ]
    
    TOTAL_LIABILITIES = [
        'total liabilities'
    ]
    
    EQUITY = [
        'total equity', "shareholders' equity", 'stockholders\' equity',
        "shareholder's equity", 'total shareholders\' equity'
    ]
    
    # Cash Flow Keywords
    CASH_FROM_OPERATIONS = [
        'cash from operations', 'operating cash flow',
        'cash from operating activities', 'cash provided by operations',
        'net cash provided by operating activities'
    ]
    
    CAPEX = [
        'capital expenditures', 'capex', 'purchases of property and equipment',
        'purchase of property', 'property and equipment expenditures',
        'payments for acquisition of property'
    ]
    
    FREE_CASH_FLOW = [
        'free cash flow', 'fcf'
    ]
    
    DIVIDENDS = [
        'dividends', 'dividend payments', 'cash dividends',
        'payments for dividends'
    ]
    
    SHARE_REPURCHASES = [
        'share repurchases', 'stock buyback', 'repurchases of common stock',
        'treasury stock purchased', 'buyback'
    ]


class PDFFinancialExtractor:
    """Main extractor class for financial PDFs"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pdf = None
        self.text_content = []
        self.tables = []
        
    def __enter__(self):
        self.pdf = pdfplumber.open(self.pdf_path)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pdf:
            self.pdf.close()
    
    def extract_all(self) -> Dict:
        """Extract all financial statements from PDF"""
        logger.info(f"Processing PDF: {self.pdf_path}")
        
        # Extract text and tables from all pages
        self._extract_content()
        
        # Detect document type and period
        doc_type = self._detect_document_type()
        periods = self._extract_periods()
        
        logger.info(f"Detected document type: {doc_type}")
        logger.info(f"Detected periods: {periods}")
        
        # Extract based on document type
        results = {
            'document_type': doc_type,
            'periods': [asdict(p) for p in periods],
            'extraction_timestamp': datetime.utcnow().isoformat(),
            'source_file': self.pdf_path,
            'income_statements': [],
            'balance_sheets': [],
            'cash_flows': []
        }
        
        # Extract each statement type
        if 'income' in doc_type.lower() or 'earnings' in doc_type.lower():
            results['income_statements'] = self._extract_income_statements(periods)
        
        if 'balance' in doc_type.lower():
            results['balance_sheets'] = self._extract_balance_sheets(periods)
            
        if 'cash flow' in doc_type.lower() or 'cash' in doc_type.lower():
            results['cash_flows'] = self._extract_cash_flows(periods)
        
        # If document contains multiple statements (annual report)
        if any(keyword in doc_type.lower() for keyword in ['annual', 'quarterly', 'earnings']):
            # Try to extract all three
            if not results['income_statements']:
                results['income_statements'] = self._extract_income_statements(periods)
            if not results['balance_sheets']:
                results['balance_sheets'] = self._extract_balance_sheets(periods)
            if not results['cash_flows']:
                results['cash_flows'] = self._extract_cash_flows(periods)
        
        return results
    
    def _extract_content(self):
        """Extract text and tables from all pages"""
        for page_num, page in enumerate(self.pdf.pages, 1):
            # Extract text
            text = page.extract_text()
            if text:
                self.text_content.append({
                    'page': page_num,
                    'text': text
                })
            
            # Extract tables
            tables = page.extract_tables()
            if tables:
                for table_num, table in enumerate(tables, 1):
                    self.tables.append({
                        'page': page_num,
                        'table_num': table_num,
                        'data': table
                    })
        
        logger.info(f"Extracted {len(self.text_content)} pages and {len(self.tables)} tables")
    
    def _detect_document_type(self) -> str:
        """Detect the type of financial document"""
        # Combine all text
        all_text = ' '.join([page['text'].lower() for page in self.text_content])
        
        # Count occurrences of key phrases
        scores = {
            'Income Statement': 0,
            'Balance Sheet': 0,
            'Cash Flow Statement': 0,
            'Annual Report': 0,
            'Quarterly Report': 0
        }
        
        # Income statement indicators
        income_keywords = ['income statement', 'statement of income', 'statement of operations',
                          'statement of earnings', 'profit and loss', 'p&l']
        scores['Income Statement'] = sum(all_text.count(kw) for kw in income_keywords)
        
        # Balance sheet indicators
        balance_keywords = ['balance sheet', 'statement of financial position',
                           'statement of financial condition']
        scores['Balance Sheet'] = sum(all_text.count(kw) for kw in balance_keywords)
        
        # Cash flow indicators
        cashflow_keywords = ['cash flow', 'statement of cash flows', 'cash flows']
        scores['Cash Flow Statement'] = sum(all_text.count(kw) for kw in cashflow_keywords)
        
        # Report type
        if 'annual report' in all_text or '10-k' in all_text:
            scores['Annual Report'] = 10
        if 'quarterly report' in all_text or '10-q' in all_text:
            scores['Quarterly Report'] = 10
        
        # Return the type with highest score
        doc_type = max(scores, key=scores.get)
        
        # If it's a full report, include all statement types
        if doc_type in ['Annual Report', 'Quarterly Report']:
            return doc_type
        
        return doc_type
    
    def _extract_periods(self) -> List[FinancialPeriod]:
        """Extract financial periods from the document"""
        periods = []
        
        # Combine all text
        all_text = ' '.join([page['text'] for page in self.text_content])
        
        # Common period patterns
        patterns = [
            # "Three Months Ended September 30, 2025"
            r'(?:three|nine|six|twelve)\s+months?\s+ended?\s+([a-z]+\s+\d{1,2},?\s+\d{4})',
            # "For the Year Ended December 31, 2024"
            r'for\s+the\s+year\s+ended?\s+([a-z]+\s+\d{1,2},?\s+\d{4})',
            # "Q3 2025", "3Q25"
            r'(?:q|quarter\s+)([1-4])\s*[,\s]*(\d{4}|\d{2})',
            # "FY 2024", "Fiscal Year 2024"
            r'(?:fy|fiscal\s+year)\s*(\d{4})',
            # "September 30, 2025"
            r'([a-z]+\s+\d{1,2},?\s+\d{4})',
            # "2025-09-30"
            r'(\d{4})-(\d{2})-(\d{2})'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, all_text.lower())
            for match in matches:
                try:
                    period = self._parse_period(match.group())
                    if period and period not in periods:
                        periods.append(period)
                except Exception as e:
                    logger.warning(f"Failed to parse period: {match.group()} - {e}")
        
        # Sort by date, most recent first
        periods.sort(key=lambda x: x.period_date, reverse=True)
        
        return periods[:8]  # Return up to 8 most recent periods
    
    def _parse_period(self, period_str: str) -> Optional[FinancialPeriod]:
        """Parse a period string into a FinancialPeriod object"""
        # This is a simplified parser - would need more robust date parsing
        # For now, return a placeholder
        try:
            # Try to extract year
            year_match = re.search(r'(\d{4})', period_str)
            if year_match:
                year = int(year_match.group(1))
                
                # Try to extract quarter
                quarter_match = re.search(r'q([1-4])', period_str.lower())
                quarter = int(quarter_match.group(1)) if quarter_match else None
                
                # Determine period type
                if 'three months' in period_str.lower() or quarter:
                    period_type = 'Quarterly'
                elif 'nine months' in period_str.lower():
                    period_type = 'Nine Months'
                elif 'year' in period_str.lower() or 'twelve months' in period_str.lower():
                    period_type = 'Annual'
                else:
                    period_type = 'Unknown'
                
                # Create period date (end of quarter/year)
                if quarter:
                    month = quarter * 3
                    period_date = f"{year}-{month:02d}-{self._get_last_day_of_month(year, month)}"
                else:
                    period_date = f"{year}-12-31"
                
                return FinancialPeriod(
                    period_date=period_date,
                    period_type=period_type,
                    fiscal_year=year,
                    fiscal_quarter=quarter
                )
        except Exception as e:
            logger.debug(f"Failed to parse period {period_str}: {e}")
        
        return None
    
    def _get_last_day_of_month(self, year: int, month: int) -> int:
        """Get the last day of a month"""
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # Check for leap year
        if month == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            return 29
        return days_in_month[month - 1]
    
    def _extract_income_statements(self, periods: List[FinancialPeriod]) -> List[Dict]:
        """Extract income statement data"""
        income_statements = []
        
        for table_info in self.tables:
            table = table_info['data']
            page = table_info['page']
            
            # Check if this table contains income statement data
            if self._is_income_statement_table(table):
                logger.info(f"Found income statement on page {page}")
                
                # Extract data from table
                extracted_data = self._parse_income_statement_table(table, page)
                
                # Match with periods
                for period in periods:
                    statement = IncomeStatementData(
                        period=period,
                        **extracted_data,
                        source_page=page
                    )
                    income_statements.append(asdict(statement))
        
        return income_statements
    
    def _is_income_statement_table(self, table: List[List]) -> bool:
        """Check if a table contains income statement data"""
        if not table or len(table) < 2:
            return False
        
        # Convert table to lowercase text
        table_text = ' '.join([
            ' '.join([str(cell).lower() if cell else '' for cell in row])
            for row in table
        ])
        
        # Check for income statement keywords
        income_keywords = ['revenue', 'sales', 'net income', 'operating income',
                          'gross profit', 'ebit', 'earnings']
        
        return sum(keyword in table_text for keyword in income_keywords) >= 3
    
    def _parse_income_statement_table(self, table: List[List], page: int) -> Dict:
        """Parse income statement table and extract values"""
        data = {}
        
        # Find header row (contains years/periods)
        header_row = table[0] if table else []
        
        # Iterate through rows to find and extract values
        for row in table[1:]:
            if not row or len(row) < 2:
                continue
            
            label = str(row[0]).lower().strip() if row[0] else ''
            values = [self._parse_number(cell) for cell in row[1:]]
            
            # Match label to field
            field = self._match_income_statement_field(label)
            if field and values and values[0] is not None:
                data[field] = values[0]  # Take first value (most recent period)
        
        # Calculate confidence score
        filled_fields = sum(1 for v in data.values() if v is not None)
        total_fields = 13  # Number of key income statement fields
        data['confidence_score'] = filled_fields / total_fields
        
        return data
    
    def _match_income_statement_field(self, label: str) -> Optional[str]:
        """Match a label to an income statement field"""
        keyword_map = {
            'revenue': FinancialKeywords.REVENUE,
            'cost_of_revenue': FinancialKeywords.COST_OF_REVENUE,
            'gross_profit': FinancialKeywords.GROSS_PROFIT,
            'operating_expenses': FinancialKeywords.OPERATING_EXPENSES,
            'ebitda': FinancialKeywords.EBITDA,
            'depreciation_amortization': FinancialKeywords.DEPRECIATION,
            'ebit': FinancialKeywords.EBIT,
            'interest_expense': FinancialKeywords.INTEREST_EXPENSE,
            'pretax_income': FinancialKeywords.PRETAX_INCOME,
            'income_tax': FinancialKeywords.TAX,
            'net_income': FinancialKeywords.NET_INCOME
        }
        
        for field, keywords in keyword_map.items():
            if any(keyword in label for keyword in keywords):
                return field
        
        return None
    
    def _extract_balance_sheets(self, periods: List[FinancialPeriod]) -> List[Dict]:
        """Extract balance sheet data"""
        # Similar structure to income statement extraction
        # Implementation would follow same pattern
        return []
    
    def _extract_cash_flows(self, periods: List[FinancialPeriod]) -> List[Dict]:
        """Extract cash flow statement data"""
        # Similar structure to income statement extraction
        # Implementation would follow same pattern
        return []
    
    def _parse_number(self, cell) -> Optional[Decimal]:
        """Parse a cell value to extract number"""
        if cell is None:
            return None
        
        try:
            # Convert to string and clean
            text = str(cell).strip()
            
            # Remove common formatting
            text = text.replace('$', '').replace(',', '').replace('(', '-').replace(')', '')
            text = text.replace('−', '-')  # Unicode minus
            
            # Handle percentages
            if '%' in text:
                text = text.replace('%', '')
                return Decimal(text) / 100
            
            # Try to convert to Decimal
            return Decimal(text)
        except:
            return None


def extract_financial_statements(pdf_path: str) -> Dict:
    """
    Main function to extract financial statements from a PDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing extracted financial data
    """
    with PDFFinancialExtractor(pdf_path) as extractor:
        return extractor.extract_all()


# Example usage
if __name__ == '__main__':
    # Test with the uploaded Meta earnings report
    pdf_path = '/mnt/user-data/uploads/Meta-Reports-Third-Quarter-2025-Results-2025.pdf'
    
    try:
        results = extract_financial_statements(pdf_path)
        print(json.dumps(results, indent=2, default=str))
    except Exception as e:
        logger.error(f"Failed to extract: {e}")
        raise
