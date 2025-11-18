# Professional Report Generation System

## Overview

The Real Estate Dashboard now includes a comprehensive professional report generation system that automatically creates investment-grade documents from your deal data, portfolio metrics, and market analysis.

## Features

### Report Types

1. **Investment Committee Memos**
   - Automatically generated from deal data
   - Includes executive summary, investment overview, financial analysis
   - Market analysis with comparable transactions
   - Risk assessment and recommendations
   - Professional formatting with charts

2. **Quarterly Portfolio Reports**
   - Fund performance summaries
   - Portfolio investment tracking
   - Unrealized gains/losses
   - Investment breakdowns
   - Performance charts

3. **Market Research Reports**
   - Market statistics and trends
   - Comparable transaction analysis
   - Property type breakdowns
   - Average cap rates and pricing
   - Market summary insights

4. **Due Diligence Summary Reports**
   - Property overview
   - DD timeline tracking
   - Key findings by category
   - Action items and recommendations
   - Status tracking

### Export Formats

All reports can be exported in multiple formats:
- **PDF** - Professional documents with embedded charts
- **PowerPoint (PPTX)** - Presentation-ready slides
- **Word (DOCX)** - Editable documents (coming soon)
- **Excel (XLSX)** - Data-focused exports (coming soon)

## Usage

### Backend API

#### Generate Investment Committee Memo

```python
POST /api/v1/reports/generate
{
  "report_type": "investment_committee_memo",
  "report_name": "123 Main St - IC Memo",
  "deal_id": "uuid-of-deal",
  "include_charts": true
}
```

#### Generate Quarterly Portfolio Report

```python
POST /api/v1/reports/generate
{
  "report_type": "quarterly_portfolio",
  "report_name": "Q1 2024 Portfolio Performance",
  "fund_id": "uuid-of-fund",  # Optional, omit for all funds
  "quarter": 1,
  "year": 2024,
  "include_charts": true
}
```

#### Generate Market Research Report

```python
POST /api/v1/reports/generate
{
  "report_type": "market_research",
  "report_name": "Austin Multifamily Market Analysis",
  "market": "Austin, TX",
  "property_type": "Multifamily",  # Optional
  "include_charts": true
}
```

#### Export Report to PDF

```python
POST /api/v1/reports/{report_id}/export/pdf
```

Response: PDF file download

#### Export Report to PowerPoint

```python
POST /api/v1/reports/{report_id}/export/powerpoint
```

Response: PPTX file download

#### Quick Generate (Direct Export)

For immediate exports without database storage:

```python
POST /api/v1/reports/quick/investment-memo/{deal_id}?export_format=pdf
```

### Frontend UI

Navigate to `/reports` in the dashboard to access the Report Generator interface.

#### Steps:

1. **Select Report Type**
   - Choose from Investment Memo, Portfolio Report, Market Research, or Due Diligence

2. **Fill in Details**
   - Report name
   - Select relevant deal/fund (if applicable)
   - Specify market/period (if applicable)

3. **Generate Report**
   - Click "Generate Report"
   - Report data is compiled from your CRM, fund management, and financial models

4. **Export**
   - Once generated, export to PDF or PowerPoint
   - Download directly to your device

## Technical Architecture

### Backend Components

```
backend/app/
├── models/
│   └── reports.py                    # Report data models
├── services/
│   └── report_generator_service.py   # Report generation logic
├── core/
│   └── document_generator.py         # PDF/PowerPoint generators
└── api/v1/endpoints/
    └── reports.py                    # API endpoints
```

### Key Services

#### ReportGeneratorService

Main service for generating report data:
- Aggregates data from deals, funds, comparables
- Calculates financial metrics
- Generates charts
- Formats data for export

#### PDFGenerator

Utility for creating professional PDFs:
- Custom styled sections
- Embedded charts
- Tables with formatting
- Multi-page layouts

#### PowerPointGenerator

Utility for creating presentations:
- Title and content slides
- Data tables
- Chart embedding
- Professional themes

#### ChartGenerator

Creates charts for embedding:
- Bar charts
- Line charts
- Pie charts
- Returns PNG bytes for embedding

### Database Models

#### GeneratedReport

Stores generated reports:
- `report_type` - Type of report
- `report_name` - Custom name
- `status` - Generation status
- `report_data` - JSON data
- `deal_id` / `fund_id` - Source references
- `export_formats` - Available formats

#### ReportTemplate

Custom report templates (future feature):
- Custom HTML/CSS templates
- Section configuration
- Reusable formats

## Data Sources

Reports pull data from:

1. **CRM Module**
   - Deal pipeline data
   - Property information
   - Broker relationships
   - Comparable transactions

2. **Fund Management**
   - Fund performance
   - Portfolio investments
   - LP commitments
   - Capital calls and distributions

3. **Financial Models**
   - DCF valuations
   - LBO returns analysis
   - Sensitivity analyses

4. **ML Analytics**
   - Deal scoring
   - Market predictions
   - Anomaly detection

## Report Components

### Investment Committee Memo Sections

1. **Executive Summary**
   - Property overview
   - Key metrics (cap rate, IRR, NOI)
   - Investment thesis

2. **Investment Overview**
   - Property details
   - Pricing analysis
   - Timeline

3. **Financial Analysis**
   - Revenue projections
   - Operating metrics
   - Returns analysis

4. **Market Analysis**
   - Market overview
   - Comparable transactions
   - Market positioning

5. **Risk Analysis**
   - Risk categories
   - Risk ratings
   - Mitigation strategies

6. **Recommendation**
   - Investment decision
   - Confidence level
   - Next steps

### Charts Included

- Cap rate comparison
- Fund performance
- Market trends
- Returns waterfall
- Portfolio allocation

## Dependencies

### Python Packages

```
reportlab==4.0.7         # PDF generation
python-pptx==0.6.23      # PowerPoint generation
jinja2==3.1.2            # Template rendering
pillow==10.1.0           # Image processing
matplotlib==3.8.2        # Chart generation
weasyprint==60.1         # Alternative PDF engine
```

Install with:
```bash
cd backend
pip install -r requirements.txt
```

## Configuration

### Environment Variables

```env
# Report Generation Settings
REPORTS_STORAGE_PATH=/path/to/reports  # Optional: for file storage
ENABLE_WATERMARKS=true                 # Add watermarks to PDFs
DEFAULT_CHART_DPI=300                  # Chart resolution
```

### Company Context

Reports are automatically filtered by company:
- Uses `X-Company-ID` header or JWT token
- Ensures data isolation
- Multi-tenant support

## Best Practices

1. **Naming Conventions**
   - Use descriptive report names
   - Include date/quarter in name
   - Example: "Sunset Apartments - IC Memo - Q1 2024"

2. **Data Quality**
   - Ensure deal data is complete
   - Update cap rates and pricing
   - Add comprehensive notes

3. **Chart Inclusion**
   - Enable charts for presentations
   - Disable for text-heavy reports
   - Charts increase file size

4. **Export Format Selection**
   - PDF for final distribution
   - PowerPoint for presentations
   - Word for collaborative editing

## API Response Examples

### Generate Report Response

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "report_type": "investment_committee_memo",
  "report_name": "123 Main St IC Memo",
  "status": "completed",
  "data": {
    "report_type": "Investment Committee Memo",
    "deal_name": "123 Main Street Apartments",
    "executive_summary": { ... },
    "investment_overview": { ... },
    "financial_analysis": { ... }
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### List Reports Response

```json
{
  "success": true,
  "data": [
    {
      "id": "...",
      "report_type": "investment_committee_memo",
      "report_name": "123 Main St IC Memo",
      "status": "completed",
      "generated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **Report Generation Fails**
   - Check that deal/fund data exists
   - Verify company_id is set
   - Check logs for specific errors

2. **Charts Not Appearing**
   - Ensure matplotlib is installed
   - Check chart data is not empty
   - Verify `include_charts=true`

3. **PDF Export Fails**
   - Install reportlab: `pip install reportlab`
   - Check file permissions
   - Verify sufficient disk space

4. **Missing Data in Report**
   - Ensure deal has required fields
   - Check database relationships
   - Verify comparables exist for market analysis

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- [ ] Custom report templates
- [ ] Scheduled report generation
- [ ] Email delivery
- [ ] Batch report generation
- [ ] Excel exports with formulas
- [ ] Interactive web previews
- [ ] Report versioning
- [ ] Template marketplace
- [ ] Multi-language support
- [ ] Advanced charting options

## Support

For issues or feature requests:
- Create an issue in the repository
- Contact development team
- Review API documentation at `/docs`

## License

Part of the Real Estate Dashboard application.
