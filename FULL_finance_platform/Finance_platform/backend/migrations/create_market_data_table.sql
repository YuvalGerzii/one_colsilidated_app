-- Create market_data table
-- Run this with: psql -U portfolio_user -d portfolio_dashboard -f create_market_data_table.sql

CREATE TABLE IF NOT EXISTS market_data (
    -- Primary Key
    id SERIAL PRIMARY KEY,

    -- Location Information
    address VARCHAR(500) NOT NULL,
    city VARCHAR(200) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,

    -- Property Type
    property_type VARCHAR(100) NOT NULL,

    -- CoStar Data
    costar_cap_rate FLOAT,
    costar_avg_rent_psf FLOAT,
    costar_market_trend VARCHAR(50),
    costar_vacancy_rate FLOAT,
    costar_comparable_sales JSONB,
    costar_market_rating VARCHAR(20),

    -- Zillow/Redfin Data
    zillow_estimate FLOAT,
    zillow_rent_estimate FLOAT,
    zillow_price_sqft FLOAT,
    zillow_price_change_30d FLOAT,
    zillow_comparable_properties JSONB,
    redfin_hot_homes_rank INTEGER,
    redfin_days_on_market INTEGER,

    -- Census Data
    census_population INTEGER,
    census_median_income FLOAT,
    census_population_growth FLOAT,
    census_employment_rate FLOAT,
    census_age_median FLOAT,
    census_education_bachelor_plus FLOAT,
    census_demographics JSONB,

    -- Walk Score Data
    walk_score INTEGER,
    transit_score INTEGER,
    bike_score INTEGER,
    walk_score_description VARCHAR(100),
    nearby_amenities JSONB,

    -- Metadata
    data_sources JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Optional relationship to company
    company_id INTEGER,

    -- Foreign key constraint (if companies table exists)
    CONSTRAINT fk_company
        FOREIGN KEY (company_id)
        REFERENCES companies(id)
        ON DELETE CASCADE
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_market_data_location ON market_data(city, state, zip_code);
CREATE INDEX IF NOT EXISTS idx_market_data_property_type ON market_data(property_type);
CREATE INDEX IF NOT EXISTS idx_market_data_created_at ON market_data(created_at);
CREATE INDEX IF NOT EXISTS idx_market_data_company_id ON market_data(company_id);

-- Add comments to the table
COMMENT ON TABLE market_data IS 'Market data from external APIs (CoStar, Zillow, Census, Walk Score)';
COMMENT ON COLUMN market_data.address IS 'Property address';
COMMENT ON COLUMN market_data.property_type IS 'Property type (e.g., Multifamily, SFR, Office)';
COMMENT ON COLUMN market_data.costar_cap_rate IS 'Cap rate from CoStar';
COMMENT ON COLUMN market_data.zillow_estimate IS 'Zillow Zestimate property value';
COMMENT ON COLUMN market_data.census_population IS 'Census population data';
COMMENT ON COLUMN market_data.walk_score IS 'Walk Score (0-100)';

-- Display success message
\echo 'Successfully created market_data table and indexes!'

-- Show table structure
\d market_data
