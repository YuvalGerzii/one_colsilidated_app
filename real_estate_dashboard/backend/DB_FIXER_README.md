# Database Validation and Fixer Utility

Comprehensive database schema validator and auto-repair tool with fallback mechanisms and error handling.

## Features

- **Database Connection Validation** - Verifies database connectivity before running checks
- **Schema Validation** - Validates all tables, columns, foreign keys, and indexes
- **Missing Table Detection** - Identifies tables that should exist but don't
- **Auto-Repair** - Automatically creates missing tables and fixes schema issues
- **Fallback Mechanisms** - Graceful error handling for common database issues
- **Detailed Reporting** - Comprehensive JSON reports of all issues and fixes
- **Zero Downtime** - Safe to run on production databases (validation mode)

## Usage

### Validation Only (Safe Mode)

Check database health without making any changes:

```bash
cd backend
python db_fixer.py --validate-only
```

This will:
- Verify database connection
- List all expected tables (84 tables)
- Compare with existing tables in database
- Validate columns, foreign keys, and indexes
- Report any mismatches or issues
- Exit with status 0 if healthy, 1 if errors found

### Auto-Fix Mode

Automatically repair detected issues:

```bash
python db_fixer.py --auto-fix
```

This will:
- Run full validation
- Automatically create missing tables
- Fix schema mismatches where possible
- Re-validate after fixes
- Report success/failure of each fix

### Create All Tables

Force create all tables from SQLAlchemy metadata:

```bash
python db_fixer.py --create-all
```

**Warning:** Use with caution - this will attempt to create all tables even if they exist.

### Generate JSON Report

Save detailed validation report to file:

```bash
python db_fixer.py --validate-only --report db_health_report.json
```

The report includes:
- Timestamp and environment
- Summary statistics
- All issues found (with severity levels)
- All fixes applied (with success status)
- Error details

## Understanding the Output

### Database Status

```
✅ DATABASE IS HEALTHY - No critical errors found
❌ DATABASE HAS ISSUES - Critical errors detected
```

### Issue Severity Levels

- **ERROR** - Critical issues that prevent functionality (missing tables, type mismatches)
- **WARNING** - Non-critical issues (missing columns, extra columns)
- **INFO** - Informational messages (extra columns from old schema)

### Validation Summary

```
Total issues: 36
  • Errors: 0
  • Warnings: 36
  • Missing tables: 0
```

- **Errors: 0** means database is healthy
- Warnings are typically from schema evolution (old columns)
- Missing tables will be auto-created in fix mode

## Tested Features

### Legal Services Tables (All Validated ✅)

- `legal_documents` - Legal document management
- `compliance_items` - Compliance tracking
- `legal_deadlines` - Legal calendar and deadlines
- `risk_assessments` - Property risk assessments
- `contract_reviews` - Contract review tracking

### Accounting Tables (All Validated ✅)

- `accounting_profiles` - Accounting entity profiles
- `chart_of_accounts` - Account hierarchies
- `accounting_transactions` - Transaction records
- `transaction_lines` - Transaction line items
- `tax_benefits` - Tax benefit tracking
- `integration_configs` - Third-party integrations

## API Endpoint Verification

All endpoints tested and working:

```bash
# Legal Services Dashboard
curl "http://localhost:8001/api/v1/legal-services/dashboard-summary?company_id=<UUID>"

# Legal Documents List
curl "http://localhost:8001/api/v1/legal-services/documents?company_id=<UUID>"

# Accounting Profiles
curl "http://localhost:8001/api/v1/accounting/profiles"

# Chart of Accounts
curl "http://localhost:8001/api/v1/accounting/chart-of-accounts?accounting_profile_id=<ID>"
```

## Common Issues and Solutions

### Issue: "Total expected tables: 0"

**Cause:** Models not imported, Base.metadata is empty

**Solution:** Already fixed - `db_fixer.py` now imports all models automatically

### Issue: Foreign key constraint errors

**Cause:** Data type mismatch (e.g., UUID vs Integer)

**Solution:** Already fixed - all legal services tables use UUID for company_id

### Issue: Module import errors

**Cause:** Conflicting module names (config.py vs config/ directory)

**Solution:** Already fixed - renamed config.py to settings.py

### Issue: Schema mismatches in older tables

**Cause:** Database schema evolved, old columns remain

**Solution:** Non-critical warnings - old columns don't affect functionality

## Integration with CI/CD

Add to your deployment pipeline:

```bash
# Pre-deployment validation
python db_fixer.py --validate-only --report pre_deploy_report.json

# Post-deployment auto-fix
python db_fixer.py --auto-fix --report post_deploy_report.json
```

## Architecture

The fixer uses:
- **SQLAlchemy Inspector** for schema introspection
- **Base.metadata** for expected schema definition
- **Automatic model discovery** via `app.models` import
- **Graceful error handling** with fallback mechanisms
- **Detailed logging** with severity levels

## Fallback Mechanisms

1. **Connection Failures** - Exits gracefully with error message
2. **Missing Tables** - Creates tables using SQLAlchemy metadata
3. **Schema Mismatches** - Reports but doesn't fail validation
4. **Foreign Key Errors** - Logs warning but continues validation
5. **Index Validation Errors** - Non-blocking, continues with other checks

## Best Practices

1. **Always validate first** - Run `--validate-only` before `--auto-fix`
2. **Save reports** - Use `--report` flag for audit trail
3. **Check exit code** - Exit 0 = healthy, Exit 1 = issues found
4. **Review warnings** - Even if healthy, check warnings for schema drift
5. **Regular checks** - Run validation after deployments and migrations

## Exit Codes

- `0` - Database is healthy (errors = 0)
- `1` - Database has issues (errors > 0)

## Support

The database fixer validates all 84 tables including:
- Property Management (11 tables)
- Real Estate Models (11 tables)
- CRM & Deal Pipeline (10 tables)
- Fund Management (8 tables)
- Financial Models (3 tables)
- Debt Management (4 tables)
- Legal Services (5 tables) ✅
- Accounting (6 tables) ✅
- Reports & Projects (8 tables)
- Market Data (18 tables)

All features fully tested and operational.
