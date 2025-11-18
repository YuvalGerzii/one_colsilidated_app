"""
Market Intelligence Data Importer Service

This service fetches data from various sources and populates the database.
Includes comprehensive error handling and fallback mechanisms.
"""

import logging
from datetime import datetime, date, timezone
from typing import Dict, List, Optional
import requests
from sqlalchemy.orm import Session

from app.models import (
    CensusData,
    FREDIndicator,
    HUDFairMarketRent,
    PropertyListing,
    MarketDataImport,
)

logger = logging.getLogger(__name__)


class MarketDataImporter:
    """Service for importing market intelligence data from various sources."""

    def __init__(self, db: Session):
        self.db = db

    def create_import_job(self, data_source: str, import_type: str = "manual") -> MarketDataImport:
        """Create a new import job record."""
        job = MarketDataImport(
            data_source=data_source,
            import_type=import_type,
            status="running",
            started_at=datetime.now(timezone.utc),
            records_processed=0,
            records_inserted=0,
            records_updated=0,
            records_failed=0,
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def complete_import_job(
        self,
        job: MarketDataImport,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        """Mark an import job as completed."""
        job.status = "completed" if success else "failed"
        job.completed_at = datetime.now(timezone.utc)
        if job.started_at:
            duration = (job.completed_at - job.started_at).total_seconds()
            job.duration_seconds = int(duration)
        if error_message:
            job.error_message = error_message
        self.db.commit()

    def import_sample_census_data(self) -> Dict:
        """
        Import sample Census data (demonstration purposes).

        In production, this would call the Census API with proper API keys.
        """
        job = self.create_import_job("census", "manual")

        try:
            # Sample data for demonstration
            sample_data = [
                {
                    "geo_level": "county",
                    "geo_id": "06075",
                    "geo_name": "San Francisco County, California",
                    "state_code": "CA",
                    "county_code": "06075",
                    "year": 2023,
                    "dataset": "acs5",
                    "total_housing_units": 394310,
                    "occupied_units": 359393,
                    "vacant_units": 34917,
                    "owner_occupied": 141088,
                    "renter_occupied": 218305,
                    "median_home_value": 1200000,
                    "median_gross_rent": 2100,
                    "median_year_built": 1968,
                    "total_population": 873965,
                    "median_age": 38.5,
                    "median_household_income": 119136,
                    "per_capita_income": 81294,
                    "poverty_rate": 10.3,
                    "unemployment_rate": 3.8,
                    "bachelors_degree_pct": 58.2,
                    "data_date": date(2023, 1, 1),
                },
                {
                    "geo_level": "county",
                    "geo_id": "06037",
                    "geo_name": "Los Angeles County, California",
                    "state_code": "CA",
                    "county_code": "06037",
                    "year": 2023,
                    "dataset": "acs5",
                    "total_housing_units": 3591981,
                    "occupied_units": 3346537,
                    "vacant_units": 245444,
                    "owner_occupied": 1662386,
                    "renter_occupied": 1684151,
                    "median_home_value": 750000,
                    "median_gross_rent": 1800,
                    "median_year_built": 1972,
                    "total_population": 9829544,
                    "median_age": 36.8,
                    "median_household_income": 76244,
                    "per_capita_income": 39271,
                    "poverty_rate": 13.9,
                    "unemployment_rate": 4.5,
                    "bachelors_degree_pct": 33.7,
                    "data_date": date(2023, 1, 1),
                },
            ]

            for data in sample_data:
                # Check if record exists
                existing = self.db.query(CensusData).filter(
                    CensusData.geo_id == data["geo_id"],
                    CensusData.year == data["year"]
                ).first()

                if existing:
                    # Update existing record
                    for key, value in data.items():
                        setattr(existing, key, value)
                    job.records_updated += 1
                else:
                    # Insert new record
                    record = CensusData(**data)
                    self.db.add(record)
                    job.records_inserted += 1

                job.records_processed += 1

            self.db.commit()
            self.complete_import_job(job, success=True)

            return {
                "success": True,
                "job_id": job.id,
                "records_processed": job.records_processed,
                "records_inserted": job.records_inserted,
                "records_updated": job.records_updated,
            }

        except Exception as e:
            logger.error(f"Error importing census data: {e}")
            job.records_failed = job.records_processed
            self.complete_import_job(job, success=False, error_message=str(e))
            self.db.rollback()
            return {
                "success": False,
                "error": str(e),
                "job_id": job.id,
            }

    def import_sample_fred_data(self) -> Dict:
        """
        Import sample FRED economic indicators.

        In production, this would call the FRED API with proper API keys.
        """
        job = self.create_import_job("fred", "manual")

        try:
            # Sample FRED data
            sample_data = [
                {
                    "series_id": "MORTGAGE30US",
                    "series_name": "30-Year Fixed Rate Mortgage Average",
                    "category": "interest_rates",
                    "observation_date": date(2024, 11, 1),
                    "value": 6.87,
                    "frequency": "weekly",
                    "units": "Percent",
                    "seasonal_adjustment": "Not Seasonally Adjusted",
                },
                {
                    "series_id": "HOUST",
                    "series_name": "Housing Starts: Total: New Privately Owned",
                    "category": "housing",
                    "observation_date": date(2024, 10, 1),
                    "value": 1360.0,
                    "frequency": "monthly",
                    "units": "Thousands of Units",
                    "seasonal_adjustment": "Seasonally Adjusted Annual Rate",
                },
                {
                    "series_id": "CSUSHPINSA",
                    "series_name": "S&P/Case-Shiller U.S. National Home Price Index",
                    "category": "housing",
                    "observation_date": date(2024, 9, 1),
                    "value": 315.42,
                    "frequency": "monthly",
                    "units": "Index Jan 2000=100",
                    "seasonal_adjustment": "Not Seasonally Adjusted",
                },
            ]

            for data in sample_data:
                # Check if record exists
                existing = self.db.query(FREDIndicator).filter(
                    FREDIndicator.series_id == data["series_id"],
                    FREDIndicator.observation_date == data["observation_date"]
                ).first()

                if existing:
                    for key, value in data.items():
                        setattr(existing, key, value)
                    job.records_updated += 1
                else:
                    record = FREDIndicator(**data)
                    self.db.add(record)
                    job.records_inserted += 1

                job.records_processed += 1

            self.db.commit()
            self.complete_import_job(job, success=True)

            return {
                "success": True,
                "job_id": job.id,
                "records_processed": job.records_processed,
                "records_inserted": job.records_inserted,
                "records_updated": job.records_updated,
            }

        except Exception as e:
            logger.error(f"Error importing FRED data: {e}")
            job.records_failed = job.records_processed
            self.complete_import_job(job, success=False, error_message=str(e))
            self.db.rollback()
            return {
                "success": False,
                "error": str(e),
                "job_id": job.id,
            }

    def import_sample_hud_data(self) -> Dict:
        """
        Import sample HUD Fair Market Rent data.

        In production, this would download HUD data files.
        """
        job = self.create_import_job("hud", "manual")

        try:
            # Sample HUD FMR data for California counties
            sample_data = [
                {
                    "fips_code": "06075",
                    "county_name": "San Francisco County",
                    "state_code": "CA",
                    "metro_code": "41860",
                    "metro_name": "San Francisco-Oakland-Hayward, CA HUD Metro FMR Area",
                    "fiscal_year": 2024,
                    "fmr_0br": 2190,
                    "fmr_1br": 2790,
                    "fmr_2br": 3620,
                    "fmr_3br": 5010,
                    "fmr_4br": 6180,
                    "median_family_income": 154500,
                    "very_low_income_limit": 77250,
                    "extremely_low_income_limit": 46350,
                    "low_income_limit": 123600,
                    "fmr_type": "Metro FMR",
                },
                {
                    "fips_code": "06037",
                    "county_name": "Los Angeles County",
                    "state_code": "CA",
                    "metro_code": "31080",
                    "metro_name": "Los Angeles-Long Beach-Anaheim, CA HUD Metro FMR Area",
                    "fiscal_year": 2024,
                    "fmr_0br": 1676,
                    "fmr_1br": 1943,
                    "fmr_2br": 2449,
                    "fmr_3br": 3272,
                    "fmr_4br": 4048,
                    "median_family_income": 98100,
                    "very_low_income_limit": 49050,
                    "extremely_low_income_limit": 29430,
                    "low_income_limit": 78480,
                    "fmr_type": "Metro FMR",
                },
            ]

            for data in sample_data:
                existing = self.db.query(HUDFairMarketRent).filter(
                    HUDFairMarketRent.fips_code == data["fips_code"],
                    HUDFairMarketRent.fiscal_year == data["fiscal_year"]
                ).first()

                if existing:
                    for key, value in data.items():
                        setattr(existing, key, value)
                    job.records_updated += 1
                else:
                    record = HUDFairMarketRent(**data)
                    self.db.add(record)
                    job.records_inserted += 1

                job.records_processed += 1

            self.db.commit()
            self.complete_import_job(job, success=True)

            return {
                "success": True,
                "job_id": job.id,
                "records_processed": job.records_processed,
                "records_inserted": job.records_inserted,
                "records_updated": job.records_updated,
            }

        except Exception as e:
            logger.error(f"Error importing HUD data: {e}")
            job.records_failed = job.records_processed
            self.complete_import_job(job, success=False, error_message=str(e))
            self.db.rollback()
            return {
                "success": False,
                "error": str(e),
                "job_id": job.id,
            }

    def import_sample_property_listings(self) -> Dict:
        """
        Import sample property listings.

        In production, this would use the HomeHarvest scraper.
        """
        job = self.create_import_job("property_listings", "manual")

        try:
            # Sample property listings
            sample_data = [
                {
                    "source": "zillow",
                    "source_id": "zpid_12345",
                    "source_url": "https://zillow.com/property/12345",
                    "address": "1234 Market Street",
                    "city": "San Francisco",
                    "state_code": "CA",
                    "zip_code": "94102",
                    "county": "San Francisco County",
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "property_type": "single_family",
                    "listing_type": "for_sale",
                    "status": "active",
                    "price": 1450000,
                    "price_per_sqft": 805.56,
                    "bedrooms": 3,
                    "bathrooms": 2.0,
                    "square_footage": 1800,
                    "lot_size": 2400.00,
                    "year_built": 1925,
                    "listing_date": date(2024, 10, 15),
                    "days_on_market": 25,
                    "description": "Beautiful Victorian home in prime SF location",
                },
                {
                    "source": "redfin",
                    "source_id": "redfin_67890",
                    "source_url": "https://redfin.com/property/67890",
                    "address": "567 Valencia Street",
                    "city": "San Francisco",
                    "state_code": "CA",
                    "zip_code": "94110",
                    "county": "San Francisco County",
                    "latitude": 37.7599,
                    "longitude": -122.4209,
                    "property_type": "condo",
                    "listing_type": "for_sale",
                    "status": "active",
                    "price": 895000,
                    "price_per_sqft": 746.67,
                    "bedrooms": 2,
                    "bathrooms": 2.0,
                    "square_footage": 1200,
                    "year_built": 2015,
                    "listing_date": date(2024, 11, 1),
                    "days_on_market": 8,
                    "description": "Modern condo in vibrant Mission District",
                },
            ]

            for data in sample_data:
                existing = self.db.query(PropertyListing).filter(
                    PropertyListing.source == data["source"],
                    PropertyListing.source_id == data["source_id"]
                ).first()

                if existing:
                    for key, value in data.items():
                        setattr(existing, key, value)
                    job.records_updated += 1
                else:
                    record = PropertyListing(**data)
                    self.db.add(record)
                    job.records_inserted += 1

                job.records_processed += 1

            self.db.commit()
            self.complete_import_job(job, success=True)

            return {
                "success": True,
                "job_id": job.id,
                "records_processed": job.records_processed,
                "records_inserted": job.records_inserted,
                "records_updated": job.records_updated,
            }

        except Exception as e:
            logger.error(f"Error importing property listings: {e}")
            job.records_failed = job.records_processed
            self.complete_import_job(job, success=False, error_message=str(e))
            self.db.rollback()
            return {
                "success": False,
                "error": str(e),
                "job_id": job.id,
            }

    def import_all_sample_data(self) -> Dict:
        """Import sample data from all sources."""
        results = {
            "census": self.import_sample_census_data(),
            "fred": self.import_sample_fred_data(),
            "hud": self.import_sample_hud_data(),
            "property_listings": self.import_sample_property_listings(),
        }

        # Calculate totals
        total_inserted = sum(r.get("records_inserted", 0) for r in results.values())
        total_updated = sum(r.get("records_updated", 0) for r in results.values())
        all_success = all(r.get("success", False) for r in results.values())

        return {
            "success": all_success,
            "total_inserted": total_inserted,
            "total_updated": total_updated,
            "details": results,
        }
