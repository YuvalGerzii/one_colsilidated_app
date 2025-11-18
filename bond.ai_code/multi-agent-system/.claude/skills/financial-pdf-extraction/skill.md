---
name: Financial PDF Extraction
description: Extracts financial statements (P&L, Balance Sheet, Cash Flow) from PDFs with OCR, validation, and automatic database upload
---

# Financial PDF Extraction Skill

This skill provides comprehensive PDF extraction capabilities for financial statements, including P&L (Profit & Loss), Balance Sheets, and Cash Flow Statements. Supports both text-based and scanned (OCR) PDFs with automatic validation and database integration.

## When to Use This Skill

Invoke when:
- Extracting financial data from PDF documents
- Processing scanned financial statements (OCR required)
- Validating extracted financial data for accuracy
- Mapping PDF data to database models
- Handling malformed or inconsistent PDF formats
- Automating financial data entry (70% time savings)

## Technology Stack

### Core Libraries

**PDF Processing:**
```python
# pdfplumber - Best for table extraction from text-based PDFs
pip install pdfplumber

# PyPDF2 - Alternative for simple text extraction
pip install PyPDF2

# camelot-py - Excellent for complex table structures
pip install camelot-py[cv]

# tabula-py - Java-based table extraction (requires Java)
pip install tabula-py
```

**OCR (Optical Character Recognition):**
```python
# pytesseract - Open source OCR engine
pip install pytesseract
# Requires: brew install tesseract (macOS) or apt-get install tesseract-ocr (Linux)

# pdf2image - Convert PDF pages to images for OCR
pip install pdf2image
# Requires: brew install poppler (macOS)

# Pillow - Image processing
pip install Pillow
```

**Data Processing:**
```python
# pandas - Data manipulation and cleaning
pip install pandas

# openpyxl - Excel file handling (for export)
pip install openpyxl

# python-dateutil - Date parsing
pip install python-dateutil
```

## Financial Statement Types

### 1. Profit & Loss Statement (P&L / Income Statement)

**Standard Structure:**
```
INCOME STATEMENT
Period: [Start Date] to [End Date]

REVENUE
  Rental Income                    $XXX,XXX
  Other Income                     $XXX
  ─────────────────────────────────────────
  Total Revenue                    $XXX,XXX

OPERATING EXPENSES
  Property Management              $XX,XXX
  Repairs & Maintenance            $XX,XXX
  Property Taxes                   $XX,XXX
  Insurance                        $XX,XXX
  Utilities                        $XX,XXX
  HOA Fees                         $XX,XXX
  Marketing                        $X,XXX
  Legal & Professional             $X,XXX
  ─────────────────────────────────────────
  Total Operating Expenses         $XXX,XXX

NET OPERATING INCOME (NOI)         $XXX,XXX

OTHER EXPENSES
  Debt Service (P&I)               $XX,XXX
  Depreciation                     $XX,XXX
  ─────────────────────────────────────────
  Total Other Expenses             $XXX,XXX

NET INCOME                         $XXX,XXX
```

**Extraction Pattern:**
```python
import pdfplumber
import pandas as pd
from typing import Dict, Optional
import re

def extract_pl_statement(pdf_path: str) -> Dict:
    """Extract P&L statement from PDF."""

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        tables = []

        for page in pdf.pages:
            # Extract text
            text += page.extract_text() or ""

            # Extract tables
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)

        # Parse period
        period = extract_period(text)

        # Extract line items
        revenue = extract_revenue_section(tables, text)
        expenses = extract_expense_section(tables, text)

        # Calculate totals
        total_revenue = sum(revenue.values())
        total_expenses = sum(expenses.values())
        noi = total_revenue - total_expenses

        return {
            "statement_type": "P&L",
            "period_start": period["start"],
            "period_end": period["end"],
            "revenue": revenue,
            "total_revenue": total_revenue,
            "expenses": expenses,
            "total_expenses": total_expenses,
            "noi": noi,
            "net_income": calculate_net_income(revenue, expenses, text),
        }

def extract_period(text: str) -> Dict:
    """Extract period from text like 'January 1, 2024 - December 31, 2024'."""
    from dateutil import parser

    # Pattern: "Period: MM/DD/YYYY to MM/DD/YYYY"
    period_pattern = r"(?:Period|Date Range|For the (?:Year|Month|Quarter)).*?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}).*?(?:to|through|-|–).*?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"

    match = re.search(period_pattern, text, re.IGNORECASE)
    if match:
        start_date = parser.parse(match.group(1))
        end_date = parser.parse(match.group(2))
        return {"start": start_date, "end": end_date}

    # Fallback: Try to find year
    year_match = re.search(r"20\d{2}", text)
    if year_match:
        year = int(year_match.group(0))
        return {
            "start": f"{year}-01-01",
            "end": f"{year}-12-31"
        }

    return {"start": None, "end": None}

def extract_revenue_section(tables: list, text: str) -> Dict:
    """Extract revenue line items."""
    revenue = {}

    # Common revenue keywords
    revenue_keywords = [
        "rental income", "rent revenue", "rental revenue",
        "other income", "laundry income", "parking income",
        "pet fees", "late fees", "application fees",
        "total revenue", "gross income", "total income"
    ]

    for table in tables:
        for row in table:
            if not row or len(row) < 2:
                continue

            item_name = str(row[0]).lower().strip()

            # Check if this is a revenue item
            for keyword in revenue_keywords:
                if keyword in item_name:
                    # Extract amount from last column
                    amount = extract_amount(row[-1])
                    if amount is not None:
                        revenue[row[0].strip()] = amount
                    break

    return revenue

def extract_amount(value: str) -> Optional[float]:
    """Extract numeric amount from string like '$12,345.67' or '(1,234)'."""
    if not value:
        return None

    # Remove whitespace
    value = str(value).strip()

    # Check for parentheses (negative)
    is_negative = value.startswith('(') and value.endswith(')')

    # Remove currency symbols, commas, parentheses
    cleaned = re.sub(r'[$,\(\)]', '', value)

    # Try to convert to float
    try:
        amount = float(cleaned)
        return -amount if is_negative else amount
    except ValueError:
        return None
```

### 2. Balance Sheet

**Standard Structure:**
```
BALANCE SHEET
As of [Date]

ASSETS
  Current Assets
    Cash & Cash Equivalents         $XXX,XXX
    Accounts Receivable             $XX,XXX
    Prepaid Expenses               $X,XXX
    ───────────────────────────────────────
    Total Current Assets            $XXX,XXX

  Fixed Assets
    Land                            $XXX,XXX
    Building                        $X,XXX,XXX
    Less: Accumulated Depreciation  ($XXX,XXX)
    Furniture & Equipment           $XX,XXX
    ───────────────────────────────────────
    Total Fixed Assets              $X,XXX,XXX

  TOTAL ASSETS                      $X,XXX,XXX

LIABILITIES
  Current Liabilities
    Accounts Payable                $XX,XXX
    Security Deposits               $XX,XXX
    Current Portion of Mortgage     $XX,XXX
    ───────────────────────────────────────
    Total Current Liabilities       $XXX,XXX

  Long-Term Liabilities
    Mortgage Payable                $X,XXX,XXX
    ───────────────────────────────────────
    Total Long-Term Liabilities     $X,XXX,XXX

  TOTAL LIABILITIES                 $X,XXX,XXX

EQUITY
  Owner's Capital                   $XXX,XXX
  Retained Earnings                 $XXX,XXX
  ───────────────────────────────────────
  TOTAL EQUITY                      $XXX,XXX

TOTAL LIABILITIES & EQUITY          $X,XXX,XXX
```

**Validation Rules:**
```python
def validate_balance_sheet(data: Dict) -> Dict:
    """Validate balance sheet accounting equation."""

    total_assets = data.get("total_assets", 0)
    total_liabilities = data.get("total_liabilities", 0)
    total_equity = data.get("total_equity", 0)

    # Fundamental Accounting Equation
    # Assets = Liabilities + Equity

    liabilities_plus_equity = total_liabilities + total_equity
    difference = abs(total_assets - liabilities_plus_equity)
    tolerance = 1.0  # $1 tolerance for rounding

    is_balanced = difference <= tolerance

    return {
        "is_valid": is_balanced,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "liabilities_plus_equity": liabilities_plus_equity,
        "difference": difference,
        "error_message": None if is_balanced else f"Balance sheet doesn't balance! Difference: ${difference:,.2f}"
    }
```

### 3. Cash Flow Statement

**Standard Structure:**
```
CASH FLOW STATEMENT
Period: [Start Date] to [End Date]

OPERATING ACTIVITIES
  Net Income                        $XXX,XXX
  Adjustments:
    Depreciation                    $XX,XXX
    Changes in Accounts Receivable  ($X,XXX)
    Changes in Accounts Payable     $X,XXX
    ───────────────────────────────────────
  Net Cash from Operations          $XXX,XXX

INVESTING ACTIVITIES
  Purchase of Equipment             ($XX,XXX)
  Capital Improvements              ($XX,XXX)
    ───────────────────────────────────────
  Net Cash from Investing           ($XXX,XXX)

FINANCING ACTIVITIES
  Mortgage Proceeds                 $XXX,XXX
  Mortgage Principal Payments       ($XX,XXX)
  Owner Contributions               $XX,XXX
  Owner Distributions               ($XX,XXX)
    ───────────────────────────────────────
  Net Cash from Financing           $XXX,XXX

NET CHANGE IN CASH                  $XXX,XXX
Beginning Cash Balance              $XXX,XXX
Ending Cash Balance                 $XXX,XXX
```

## OCR for Scanned PDFs

### Setup and Configuration

```python
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

def extract_from_scanned_pdf(pdf_path: str) -> str:
    """Extract text from scanned PDF using OCR."""

    # Convert PDF to images
    images = convert_from_path(
        pdf_path,
        dpi=300,  # Higher DPI = better quality
        fmt='png'
    )

    full_text = ""

    for i, image in enumerate(images):
        print(f"Processing page {i+1}/{len(images)}...")

        # Preprocess image for better OCR
        processed_image = preprocess_image_for_ocr(image)

        # Extract text with Tesseract
        page_text = pytesseract.image_to_string(
            processed_image,
            config='--psm 6'  # Assume uniform block of text
        )

        full_text += page_text + "\n\n"

    return full_text

def preprocess_image_for_ocr(image: Image) -> Image:
    """Improve image quality for OCR."""
    from PIL import ImageEnhance, ImageFilter

    # Convert to grayscale
    image = image.convert('L')

    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Sharpen
    image = image.filter(ImageFilter.SHARPEN)

    # Threshold to binary (black & white)
    threshold = 128
    image = image.point(lambda p: p > threshold and 255)

    return image

def is_scanned_pdf(pdf_path: str) -> bool:
    """Detect if PDF is scanned (image-based) or text-based."""
    import pdfplumber

    with pdfplumber.open(pdf_path) as pdf:
        # Check first page
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        # If very little text extracted, likely scanned
        return len(text or "") < 50
```

### OCR Best Practices

1. **High DPI:** Use 300 DPI minimum for conversion
2. **Preprocessing:** Enhance contrast, convert to grayscale, threshold
3. **Language:** Specify language if non-English: `lang='eng'`
4. **PSM Mode:** Choose appropriate page segmentation mode:
   - `--psm 3`: Fully automatic (default)
   - `--psm 6`: Assume uniform block of text
   - `--psm 4`: Assume single column of text
5. **Confidence:** Check OCR confidence scores to identify errors

```python
def extract_with_confidence(image: Image) -> Dict:
    """Extract text with confidence scores."""

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT,
        config='--psm 6'
    )

    # Filter low-confidence results
    min_confidence = 60

    filtered_text = []
    for i, conf in enumerate(data['conf']):
        if int(conf) > min_confidence:
            filtered_text.append(data['text'][i])

    return {
        "text": " ".join(filtered_text),
        "avg_confidence": sum(int(c) for c in data['conf'] if int(c) > 0) / len([c for c in data['conf'] if int(c) > 0]),
        "low_confidence_count": sum(1 for c in data['conf'] if 0 < int(c) < min_confidence)
    }
```

## Database Integration

### FastAPI Endpoint Pattern

```python
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict
import tempfile
import os

router = APIRouter(prefix="/financial-statements", tags=["Financial Statements"])

@router.post("/upload-pdf", response_model=FinancialStatementResponse)
async def upload_financial_statement_pdf(
    file: UploadFile = File(...),
    company_id: str = Query(...),
    statement_type: str = Query(..., regex="^(pl|balance_sheet|cash_flow)$"),
    db: Session = Depends(get_db)
):
    """
    Upload and extract financial statement from PDF.

    Args:
        file: PDF file (text-based or scanned)
        company_id: Company UUID
        statement_type: Type of statement (pl, balance_sheet, cash_flow)

    Returns:
        Extracted financial data with validation results
    """

    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Detect if scanned
        is_scanned = is_scanned_pdf(tmp_path)

        # Extract data
        if is_scanned:
            text = extract_from_scanned_pdf(tmp_path)
            # Parse extracted text
            data = parse_financial_statement(text, statement_type)
        else:
            if statement_type == "pl":
                data = extract_pl_statement(tmp_path)
            elif statement_type == "balance_sheet":
                data = extract_balance_sheet(tmp_path)
            elif statement_type == "cash_flow":
                data = extract_cash_flow_statement(tmp_path)

        # Validate
        if statement_type == "balance_sheet":
            validation = validate_balance_sheet(data)
            if not validation["is_valid"]:
                raise HTTPException(
                    status_code=422,
                    detail=validation["error_message"]
                )

        # Save to database
        statement = save_financial_statement(db, company_id, data)

        return {
            "success": True,
            "statement_id": statement.id,
            "statement_type": statement_type,
            "is_scanned": is_scanned,
            "data": data,
            "message": "Financial statement extracted and saved successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )

    finally:
        # Cleanup temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def save_financial_statement(
    db: Session,
    company_id: str,
    data: Dict
) -> FinancialStatement:
    """Save extracted financial data to database."""

    statement = FinancialStatement(
        company_id=company_id,
        statement_type=data["statement_type"],
        period_start=data.get("period_start"),
        period_end=data.get("period_end"),
        total_revenue=data.get("total_revenue"),
        total_expenses=data.get("total_expenses"),
        noi=data.get("noi"),
        net_income=data.get("net_income"),
        total_assets=data.get("total_assets"),
        total_liabilities=data.get("total_liabilities"),
        total_equity=data.get("total_equity"),
        raw_data=data  # Store full extracted data as JSON
    )

    db.add(statement)
    db.commit()
    db.refresh(statement)

    return statement
```

### Database Model

```python
from sqlalchemy import Column, String, Float, Date, JSON, ForeignKey
from app.models.base import Base, UUIDMixin, TimestampMixin

class FinancialStatement(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "financial_statements"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    statement_type = Column(String, nullable=False)  # pl, balance_sheet, cash_flow
    period_start = Column(Date)
    period_end = Column(Date)

    # P&L fields
    total_revenue = Column(Float)
    total_expenses = Column(Float)
    noi = Column(Float)
    net_income = Column(Float)

    # Balance Sheet fields
    total_assets = Column(Float)
    total_liabilities = Column(Float)
    total_equity = Column(Float)

    # Cash Flow fields
    operating_cash_flow = Column(Float)
    investing_cash_flow = Column(Float)
    financing_cash_flow = Column(Float)
    net_cash_change = Column(Float)

    # Store full extracted data
    raw_data = Column(JSON)

    # Metadata
    is_ocr = Column(Boolean, default=False)
    ocr_confidence = Column(Float)
```

## Error Handling & Validation

### Common PDF Issues

```python
class PDFExtractionError(Exception):
    """Base exception for PDF extraction errors."""
    pass

class MalformedPDFError(PDFExtractionError):
    """PDF structure is invalid or corrupted."""
    pass

class ValidationError(PDFExtractionError):
    """Extracted data failed validation."""
    pass

def safe_extract_pdf(pdf_path: str) -> Dict:
    """Extract PDF with comprehensive error handling."""

    try:
        # Check file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Check file size (max 50MB)
        file_size = os.path.getsize(pdf_path)
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            raise PDFExtractionError(f"PDF too large: {file_size / 1024 / 1024:.1f}MB (max 50MB)")

        # Try extraction
        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) == 0:
                raise MalformedPDFError("PDF has no pages")

            # Extract
            data = extract_financial_data(pdf)

            # Validate
            if not data or len(data) == 0:
                raise ValidationError("No financial data extracted from PDF")

            return data

    except pdfplumber.pdfminer.pdfparser.PDFSyntaxError:
        raise MalformedPDFError("PDF is corrupted or has invalid syntax")

    except Exception as e:
        raise PDFExtractionError(f"Unexpected error: {str(e)}")
```

### Data Validation

```python
def validate_pl_statement(data: Dict) -> Dict:
    """Validate P&L statement data."""

    errors = []
    warnings = []

    # Required fields
    required = ["total_revenue", "total_expenses", "noi"]
    for field in required:
        if field not in data or data[field] is None:
            errors.append(f"Missing required field: {field}")

    # Revenue should be positive
    if data.get("total_revenue", 0) < 0:
        warnings.append("Total revenue is negative")

    # Expenses typically positive (but can be shown as negative in some formats)
    total_expenses = data.get("total_expenses", 0)
    if total_expenses > 0:
        warnings.append("Expenses shown as positive (typically negative in accounting)")

    # NOI calculation check
    calculated_noi = data.get("total_revenue", 0) - abs(data.get("total_expenses", 0))
    extracted_noi = data.get("noi", 0)

    if abs(calculated_noi - extracted_noi) > 1:
        warnings.append(f"NOI mismatch: Calculated ${calculated_noi:,.2f} vs Extracted ${extracted_noi:,.2f}")

    # Period validation
    if data.get("period_start") and data.get("period_end"):
        from datetime import datetime
        start = data["period_start"] if isinstance(data["period_start"], datetime) else datetime.fromisoformat(str(data["period_start"]))
        end = data["period_end"] if isinstance(data["period_end"], datetime) else datetime.fromisoformat(str(data["period_end"]))

        if start > end:
            errors.append("Period start date is after end date")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
```

## Best Practices

### 1. Always Try Text Extraction First
```python
# Text extraction is 100x faster than OCR
if not is_scanned_pdf(pdf_path):
    data = extract_pl_statement(pdf_path)  # Fast
else:
    data = extract_from_scanned_pdf(pdf_path)  # Slower (OCR)
```

### 2. Store Raw Extracted Data
```python
# Always store the raw extracted data for debugging
statement.raw_data = {
    "extracted_text": full_text,
    "tables": tables,
    "line_items": line_items,
    "extraction_method": "pdfplumber" or "ocr",
    "confidence": ocr_confidence if ocr else 100
}
```

### 3. Provide Manual Review Option
```python
@router.post("/review/{statement_id}")
async def flag_for_manual_review(
    statement_id: str,
    reason: str,
    db: Session = Depends(get_db)
):
    """Flag statement for manual review if extraction confidence is low."""

    statement = db.query(FinancialStatement).filter(
        FinancialStatement.id == statement_id
    ).first()

    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")

    statement.needs_review = True
    statement.review_reason = reason
    db.commit()

    return {"message": "Flagged for manual review"}
```

### 4. Batch Processing
```python
async def process_multiple_pdfs(
    pdf_paths: List[str],
    company_id: str,
    db: Session
) -> Dict:
    """Process multiple PDFs in batch."""

    results = {
        "successful": 0,
        "failed": 0,
        "warnings": 0,
        "details": []
    }

    for pdf_path in pdf_paths:
        try:
            data = safe_extract_pdf(pdf_path)
            validation = validate_pl_statement(data)

            if validation["is_valid"]:
                statement = save_financial_statement(db, company_id, data)
                results["successful"] += 1
                results["details"].append({
                    "file": os.path.basename(pdf_path),
                    "status": "success",
                    "statement_id": statement.id
                })
            else:
                results["warnings"] += 1
                results["details"].append({
                    "file": os.path.basename(pdf_path),
                    "status": "warning",
                    "errors": validation["errors"]
                })

        except Exception as e:
            results["failed"] += 1
            results["details"].append({
                "file": os.path.basename(pdf_path),
                "status": "failed",
                "error": str(e)
            })

    return results
```

## Common Pitfalls & Solutions

### ❌ Pitfall 1: Not Handling Different PDF Formats
Financial statements come in many layouts. Don't assume a single format.

**Solution:**
```python
# Use multiple extraction strategies
strategies = [
    extract_with_pdfplumber,
    extract_with_camelot,
    extract_with_tabula,
    extract_with_ocr  # Fallback
]

for strategy in strategies:
    try:
        data = strategy(pdf_path)
        if validate_extracted_data(data):
            return data
    except Exception:
        continue

raise PDFExtractionError("All extraction strategies failed")
```

### ❌ Pitfall 2: Assuming All PDFs Are Text-Based
Many older financial statements are scanned images.

**Solution:** Always check and use OCR when needed (shown above)

### ❌ Pitfall 3: Not Validating Accounting Equations
Extracted data may have errors.

**Solution:** Always validate:
- Assets = Liabilities + Equity (Balance Sheet)
- Revenue - Expenses = Net Income (P&L)
- Sum of line items = Total

### ❌ Pitfall 4: Ignoring Negative Signs
Financial statements use different conventions for negatives.

**Solution:**
```python
def normalize_sign_convention(value: float, line_item: str) -> float:
    """Normalize accounting sign conventions."""

    # Expenses should be negative
    expense_keywords = ["expense", "cost", "depreciation"]
    if any(kw in line_item.lower() for kw in expense_keywords):
        return -abs(value)

    # Revenue should be positive
    revenue_keywords = ["revenue", "income", "sales"]
    if any(kw in line_item.lower() for kw in revenue_keywords):
        return abs(value)

    return value
```

### ❌ Pitfall 5: Not Handling Multi-Page Statements
Statements often span multiple pages.

**Solution:**
```python
def extract_multi_page_statement(pdf_path: str) -> Dict:
    """Handle statements spanning multiple pages."""

    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        full_text = ""

        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                all_tables.extend(page_tables)

            full_text += page.extract_text() or ""

        # Merge tables from all pages
        merged_data = merge_financial_tables(all_tables)

        return merged_data
```

## Testing Patterns

```python
import pytest
from fastapi.testclient import TestClient

def test_extract_text_based_pdf():
    """Test extraction from text-based PDF."""

    pdf_path = "tests/fixtures/sample_pl.pdf"
    data = extract_pl_statement(pdf_path)

    assert data["statement_type"] == "P&L"
    assert data["total_revenue"] > 0
    assert data["total_expenses"] < 0
    assert data["noi"] == data["total_revenue"] + data["total_expenses"]

def test_extract_scanned_pdf():
    """Test OCR extraction from scanned PDF."""

    pdf_path = "tests/fixtures/scanned_balance_sheet.pdf"
    text = extract_from_scanned_pdf(pdf_path)

    assert len(text) > 100
    assert "assets" in text.lower()
    assert "liabilities" in text.lower()

def test_balance_sheet_validation():
    """Test balance sheet validation."""

    data = {
        "total_assets": 1000000,
        "total_liabilities": 600000,
        "total_equity": 400000
    }

    validation = validate_balance_sheet(data)
    assert validation["is_valid"] is True

def test_malformed_pdf():
    """Test handling of corrupted PDF."""

    with pytest.raises(MalformedPDFError):
        extract_pl_statement("tests/fixtures/corrupted.pdf")

def test_upload_pdf_endpoint(client: TestClient):
    """Test PDF upload endpoint."""

    with open("tests/fixtures/sample_pl.pdf", "rb") as f:
        response = client.post(
            "/financial-statements/upload-pdf",
            files={"file": ("pl.pdf", f, "application/pdf")},
            params={
                "company_id": "test-company-id",
                "statement_type": "pl"
            }
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "statement_id" in data
```

## ROI Calculation

**Manual Data Entry:**
- Time per P&L: 30-45 minutes
- Time per Balance Sheet: 45-60 minutes
- Monthly financials (both): ~1.5 hours
- Annual cost (12 months): ~18 hours

**With PDF Extraction:**
- Upload time: 2 minutes
- Review time: 5-10 minutes
- Monthly financials (both): ~15 minutes
- Annual cost (12 months): ~3 hours

**Time Saved:** 15 hours/year per property = ~83% reduction

For a portfolio of 10 properties:
- Manual: 180 hours/year
- Automated: 30 hours/year
- **Savings: 150 hours/year (70%+ reduction)**

## Checklist for Implementation

- [ ] Install required Python packages (pdfplumber, pytesseract, pdf2image)
- [ ] Install system dependencies (Tesseract, Poppler)
- [ ] Create FinancialStatement database model
- [ ] Implement text-based PDF extraction
- [ ] Implement OCR for scanned PDFs
- [ ] Add validation logic (accounting equations)
- [ ] Create FastAPI upload endpoint
- [ ] Build frontend upload component
- [ ] Add manual review workflow
- [ ] Write comprehensive tests
- [ ] Document common PDF formats in your domain
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Create user guide with examples

## Summary

**Key Capabilities:**
✅ Extract P&L, Balance Sheet, Cash Flow from PDFs
✅ OCR support for scanned documents
✅ Automatic validation (Assets = Liabilities + Equity)
✅ Database integration with FastAPI
✅ Error handling for malformed PDFs
✅ 70%+ time savings on data entry

**Best Use Cases:**
- Monthly/quarterly financial statement processing
- Due diligence document review
- Historical data digitization
- Portfolio reporting automation

**When NOT to Use:**
- Non-standard financial document formats
- Handwritten statements (OCR unreliable)
- Extremely complex multi-entity consolidations
- Real-time data entry (manual faster for single entry)
