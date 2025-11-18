-- ============================================================================
-- Lease Abstraction & Rent Roll Database Schema
-- ============================================================================
-- 
-- Stores extracted lease data, rent rolls, and analysis results for
-- commercial real estate portfolio management
--
-- Tables:
--   1. properties - Master property list
--   2. leases - Individual lease abstractions
--   3. rent_roll - Current tenant roster
--   4. rent_roll_analysis - Historical analysis snapshots
--   5. lease_documents - Document tracking
-- ============================================================================

-- Properties table (links to existing portfolio_companies if needed)
CREATE TABLE IF NOT EXISTS properties (
    property_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES portfolio_companies(company_id),
    property_name VARCHAR(255) NOT NULL,
    property_type VARCHAR(50), -- 'Office', 'Retail', 'Industrial', 'Multifamily', 'Mixed-Use'
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    country VARCHAR(50) DEFAULT 'USA',
    
    -- Building details
    total_square_feet INTEGER,
    number_of_units INTEGER,
    year_built INTEGER,
    year_renovated INTEGER,
    
    -- Acquisition info
    acquisition_date DATE,
    acquisition_price DECIMAL(15,2),
    current_valuation DECIMAL(15,2),
    
    -- Status
    status VARCHAR(50) DEFAULT 'Active', -- 'Active', 'Under Contract', 'Sold', 'Disposed'
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    
    UNIQUE(property_name, company_id)
);

-- Lease abstractions table
CREATE TABLE IF NOT EXISTS leases (
    lease_id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(property_id) ON DELETE CASCADE,
    
    -- Tenant information
    tenant_name VARCHAR(255) NOT NULL,
    tenant_legal_name VARCHAR(255),
    tenant_credit_rating VARCHAR(10), -- 'AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'Unrated'
    
    -- Premises
    unit_number VARCHAR(50),
    premises_description TEXT,
    square_feet INTEGER NOT NULL,
    
    -- Lease dates
    lease_start_date DATE NOT NULL,
    lease_end_date DATE NOT NULL,
    lease_term_months INTEGER,
    notice_date DATE, -- Date tenant gave notice
    
    -- Financial terms
    base_rent_monthly DECIMAL(12,2),
    base_rent_annual DECIMAL(12,2),
    rent_per_sf_annual DECIMAL(10,2),
    security_deposit DECIMAL(12,2),
    
    -- Lease structure
    lease_type VARCHAR(50), -- 'Gross', 'Modified Gross', 'Net', 'Triple-Net'
    percentage_rent TEXT,
    operating_expense_structure TEXT,
    cap_on_operating_expenses TEXT,
    
    -- Renewal & termination
    renewal_options TEXT[], -- Array of renewal descriptions
    renewal_probability DECIMAL(3,2) DEFAULT 0.50, -- 0.00 to 1.00
    termination_rights TEXT,
    
    -- Escalations
    rent_escalations JSONB, -- Array of {year, type, amount_or_percentage}
    
    -- Additional costs
    tenant_improvements DECIMAL(12,2),
    leasing_commissions DECIMAL(12,2),
    parking_spaces INTEGER,
    
    -- Special clauses
    exclusive_use_clause TEXT,
    co_tenancy_clause TEXT,
    use_clause TEXT,
    assignment_subletting TEXT,
    
    -- Critical dates
    critical_dates JSONB, -- Array of {date, description}
    
    -- Document tracking
    lease_document_id INTEGER REFERENCES lease_documents(document_id),
    extraction_confidence DECIMAL(3,2), -- 0.00 to 1.00
    manually_verified BOOLEAN DEFAULT FALSE,
    verified_by VARCHAR(100),
    verified_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_leases_property (property_id),
    INDEX idx_leases_tenant (tenant_name),
    INDEX idx_leases_expiration (lease_end_date),
    INDEX idx_leases_credit (tenant_credit_rating)
);

-- Current rent roll (snapshot of active tenants)
CREATE TABLE IF NOT EXISTS rent_roll (
    rent_roll_id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(property_id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- Unit information
    unit_number VARCHAR(50) NOT NULL,
    tenant_name VARCHAR(255),
    tenant_status VARCHAR(20) NOT NULL, -- 'Occupied', 'Vacant', 'Notice'
    
    -- Size
    square_feet INTEGER NOT NULL,
    
    -- Lease dates
    lease_start_date DATE,
    lease_end_date DATE,
    months_remaining INTEGER,
    
    -- Rent
    monthly_rent DECIMAL(12,2),
    annual_rent DECIMAL(12,2),
    rent_per_sf DECIMAL(10,2),
    market_rent_per_sf DECIMAL(10,2),
    loss_to_lease_annual DECIMAL(12,2), -- Calculated: (market - actual) * SF
    
    -- Additional info
    security_deposit DECIMAL(12,2),
    lease_type VARCHAR(50),
    credit_rating VARCHAR(10),
    renewal_probability DECIMAL(3,2),
    expiration_risk VARCHAR(20), -- 'CRITICAL', 'HIGH', 'MODERATE', 'LOW', 'N/A'
    
    -- Link to lease abstract
    lease_id INTEGER REFERENCES leases(lease_id),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(property_id, snapshot_date, unit_number),
    INDEX idx_rent_roll_property (property_id),
    INDEX idx_rent_roll_date (snapshot_date),
    INDEX idx_rent_roll_status (tenant_status),
    INDEX idx_rent_roll_expiration (lease_end_date)
);

-- Rent roll analysis (historical snapshots)
CREATE TABLE IF NOT EXISTS rent_roll_analysis (
    analysis_id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(property_id) ON DELETE CASCADE,
    analysis_date DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- Property metrics
    total_square_feet INTEGER,
    occupied_square_feet INTEGER,
    vacant_square_feet INTEGER,
    
    -- Occupancy rates
    physical_occupancy_rate DECIMAL(5,2), -- Percentage
    economic_occupancy_rate DECIMAL(5,2),
    
    -- Rent metrics
    total_annual_rent DECIMAL(15,2),
    total_market_rent DECIMAL(15,2),
    weighted_avg_rent_psf DECIMAL(10,2),
    weighted_avg_market_rent_psf DECIMAL(10,2),
    
    -- Mark-to-market
    total_loss_to_lease DECIMAL(15,2),
    loss_to_lease_percentage DECIMAL(5,2),
    
    -- Lease metrics
    weighted_avg_lease_term_months DECIMAL(6,2), -- WALT
    number_of_tenants INTEGER,
    
    -- Rollover risk
    leases_expiring_12m INTEGER,
    leases_expiring_12m_sf INTEGER,
    leases_expiring_12m_rent DECIMAL(15,2),
    rollover_risk_percentage DECIMAL(5,2),
    
    -- Credit quality
    credit_weighted_avg DECIMAL(5,2), -- 1-7 scale
    
    -- Tenant concentration
    top_5_tenant_concentration DECIMAL(5,2),
    largest_tenant_name VARCHAR(255),
    largest_tenant_percentage DECIMAL(5,2),
    
    -- Full analysis JSON
    analysis_data JSONB, -- Complete report data
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    
    UNIQUE(property_id, analysis_date),
    INDEX idx_analysis_property (property_id),
    INDEX idx_analysis_date (analysis_date)
);

-- Document tracking
CREATE TABLE IF NOT EXISTS lease_documents (
    document_id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(property_id) ON DELETE CASCADE,
    
    -- Document info
    document_type VARCHAR(50) NOT NULL, -- 'Lease', 'Rent Roll', 'Amendment', 'Letter of Intent'
    document_name VARCHAR(255) NOT NULL,
    file_path TEXT,
    file_size_bytes BIGINT,
    file_hash VARCHAR(64), -- SHA-256 hash for duplicate detection
    
    -- Processing status
    processing_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'error'
    extraction_confidence DECIMAL(3,2),
    error_message TEXT,
    
    -- OCR info (if scanned)
    is_scanned BOOLEAN DEFAULT FALSE,
    ocr_confidence DECIMAL(3,2),
    
    -- Links
    lease_id INTEGER REFERENCES leases(lease_id),
    
    -- Metadata
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uploaded_by VARCHAR(100),
    processed_at TIMESTAMP,
    
    INDEX idx_documents_property (property_id),
    INDEX idx_documents_type (document_type),
    INDEX idx_documents_status (processing_status)
);

-- ============================================================================
-- Views for common queries
-- ============================================================================

-- Current rent roll view (latest snapshot per property)
CREATE OR REPLACE VIEW v_current_rent_roll AS
SELECT 
    rr.*,
    p.property_name,
    p.property_type,
    p.total_square_feet as building_total_sf
FROM rent_roll rr
INNER JOIN properties p ON rr.property_id = p.property_id
INNER JOIN (
    SELECT property_id, MAX(snapshot_date) as latest_date
    FROM rent_roll
    GROUP BY property_id
) latest ON rr.property_id = latest.property_id 
    AND rr.snapshot_date = latest.latest_date;

-- Lease expiration summary
CREATE OR REPLACE VIEW v_lease_expirations AS
SELECT 
    p.property_id,
    p.property_name,
    l.lease_id,
    l.tenant_name,
    l.unit_number,
    l.square_feet,
    l.lease_end_date,
    l.base_rent_annual,
    EXTRACT(YEAR FROM l.lease_end_date) as expiration_year,
    EXTRACT(MONTH FROM l.lease_end_date) as expiration_month,
    (DATE_PART('year', l.lease_end_date) - DATE_PART('year', CURRENT_DATE)) * 12 +
    (DATE_PART('month', l.lease_end_date) - DATE_PART('month', CURRENT_DATE)) as months_to_expiration,
    CASE 
        WHEN (DATE_PART('year', l.lease_end_date) - DATE_PART('year', CURRENT_DATE)) * 12 +
             (DATE_PART('month', l.lease_end_date) - DATE_PART('month', CURRENT_DATE)) < 6 THEN 'CRITICAL'
        WHEN (DATE_PART('year', l.lease_end_date) - DATE_PART('year', CURRENT_DATE)) * 12 +
             (DATE_PART('month', l.lease_end_date) - DATE_PART('month', CURRENT_DATE)) < 12 THEN 'HIGH'
        WHEN (DATE_PART('year', l.lease_end_date) - DATE_PART('year', CURRENT_DATE)) * 12 +
             (DATE_PART('month', l.lease_end_date) - DATE_PART('month', CURRENT_DATE)) < 24 THEN 'MODERATE'
        ELSE 'LOW'
    END as risk_level
FROM leases l
INNER JOIN properties p ON l.property_id = p.property_id
WHERE l.lease_end_date >= CURRENT_DATE
ORDER BY l.lease_end_date;

-- Portfolio-level metrics
CREATE OR REPLACE VIEW v_portfolio_metrics AS
SELECT 
    COUNT(DISTINCT p.property_id) as total_properties,
    SUM(p.total_square_feet) as total_sf,
    COUNT(DISTINCT l.lease_id) as total_leases,
    SUM(l.base_rent_annual) as total_annual_rent,
    AVG(rra.economic_occupancy_rate) as avg_occupancy,
    AVG(rra.weighted_avg_rent_psf) as avg_rent_psf,
    SUM(rra.total_loss_to_lease) as total_loss_to_lease,
    AVG(rra.weighted_avg_lease_term_months) as avg_walt
FROM properties p
LEFT JOIN leases l ON p.property_id = l.property_id AND l.lease_end_date >= CURRENT_DATE
LEFT JOIN rent_roll_analysis rra ON p.property_id = rra.property_id
WHERE p.status = 'Active';

-- ============================================================================
-- Sample queries
-- ============================================================================

-- Find leases expiring in next 12 months
/*
SELECT * FROM v_lease_expirations
WHERE months_to_expiration <= 12
ORDER BY months_to_expiration;
*/

-- Top 10 tenants by rent
/*
SELECT tenant_name, COUNT(*) as units, SUM(square_feet) as total_sf, SUM(base_rent_annual) as total_rent
FROM leases
WHERE lease_end_date >= CURRENT_DATE
GROUP BY tenant_name
ORDER BY total_rent DESC
LIMIT 10;
*/

-- Properties with highest loss-to-lease
/*
SELECT p.property_name, rra.total_loss_to_lease, rra.loss_to_lease_percentage
FROM rent_roll_analysis rra
INNER JOIN properties p ON rra.property_id = p.property_id
ORDER BY rra.total_loss_to_lease DESC
LIMIT 10;
*/

-- Tenant concentration by property
/*
SELECT 
    p.property_name,
    rra.largest_tenant_name,
    rra.largest_tenant_percentage,
    rra.top_5_tenant_concentration
FROM rent_roll_analysis rra
INNER JOIN properties p ON rra.property_id = p.property_id
ORDER BY rra.largest_tenant_percentage DESC;
*/
