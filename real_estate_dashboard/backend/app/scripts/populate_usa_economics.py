"""
USA Economics Data Population Script

Fetches real economic data from BLS and FRED APIs and populates
the economics_united_states database.

Data Sources:
- BLS (Bureau of Labor Statistics): Employment, wages, CPI
- FRED (Federal Reserve Economic Data): GDP, interest rates, money supply

Usage:
    python -m app.scripts.populate_usa_economics

API Keys (Optional but Recommended):
- BLS: No API key required (public access)
- FRED: Free API key from https://fred.stlouisfed.org/docs/api/api_key.html
  Set as environment variable: FRED_API_KEY
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import requests
from sqlalchemy.exc import IntegrityError

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database.country_database_manager import country_db_manager
from app.models.economics import EconomicIndicator, EconomicDataFetchLog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class USAEconomicsDataFetcher:
    """Fetches and stores USA economic data from multiple sources"""

    def __init__(self):
        self.country_slug = "united-states"
        self.country_name = "United States"

        # API configuration
        self.fred_api_key = os.environ.get("FRED_API_KEY")
        self.bls_api_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
        self.fred_api_url = "https://api.stlouisfed.org/fred/series"

        # Session for database
        self.db_session = None

    def initialize_database(self) -> bool:
        """Initialize the USA economics database if it doesn't exist"""
        try:
            logger.info("Initializing USA economics database...")
            success = country_db_manager.initialize_country_database(self.country_slug)
            if success:
                logger.info("✓ Database initialized successfully")
                return True
            else:
                logger.error("✗ Failed to initialize database")
                return False
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            return False

    def get_session(self):
        """Get database session for USA economics database"""
        if self.db_session is None:
            self.db_session = country_db_manager.get_session(self.country_slug)
        return self.db_session

    def close_session(self):
        """Close database session"""
        if self.db_session:
            self.db_session.close()
            self.db_session = None

    # ===== BLS API Methods =====

    def fetch_bls_data(self, series_ids: List[str], start_year: int = None, end_year: int = None) -> Optional[Dict]:
        """
        Fetch data from BLS API

        Args:
            series_ids: List of BLS series IDs
            start_year: Start year for data (default: 5 years ago)
            end_year: End year for data (default: current year)

        Returns:
            API response data or None on error
        """
        if start_year is None:
            start_year = datetime.now().year - 5
        if end_year is None:
            end_year = datetime.now().year

        payload = {
            "seriesid": series_ids,
            "startyear": str(start_year),
            "endyear": str(end_year),
        }

        try:
            response = requests.post(self.bls_api_url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching BLS data: {e}")
            return None

    def parse_bls_series(self, series_data: Dict, category: str, indicator_name: str, unit: str = "") -> List[EconomicIndicator]:
        """Parse BLS series data into EconomicIndicator objects"""
        indicators = []

        if "data" not in series_data or not series_data["data"]:
            return indicators

        # Sort by period descending to get latest first
        data_points = sorted(series_data["data"], key=lambda x: (x["year"], x["period"]), reverse=True)

        if len(data_points) == 0:
            return indicators

        # Get latest and previous values
        latest = data_points[0] if len(data_points) > 0 else None
        previous = data_points[1] if len(data_points) > 1 else None

        # Find highest and lowest
        all_values = [float(d["value"]) for d in data_points if d.get("value")]
        highest_val = max(all_values) if all_values else None
        lowest_val = min(all_values) if all_values else None

        if latest:
            # Parse date
            year = int(latest["year"])
            period = latest["period"]  # M01-M12 for monthly
            month = int(period.replace("M", "")) if "M" in period else 1
            data_date = datetime(year, month, 1)

            indicator = EconomicIndicator(
                country_name=self.country_name,
                category=category,
                indicator_name=indicator_name,
                last_value=latest["value"],
                last_value_numeric=float(latest["value"]) if latest.get("value") else None,
                previous_value=previous["value"] if previous else None,
                previous_value_numeric=float(previous["value"]) if previous and previous.get("value") else None,
                highest_value=str(highest_val) if highest_val is not None else None,
                highest_value_numeric=highest_val,
                lowest_value=str(lowest_val) if lowest_val is not None else None,
                lowest_value_numeric=lowest_val,
                unit=unit,
                frequency="Monthly",
                reference_period=f"{latest['periodName']} {latest['year']}",
                data_date=data_date,
                source="U.S. Bureau of Labor Statistics",
                data_source_api="bls-api",
            )
            indicators.append(indicator)

        return indicators

    def fetch_bls_indicators(self) -> int:
        """
        Fetch key BLS indicators

        Returns:
            Number of indicators successfully stored
        """
        logger.info("Fetching BLS indicators...")

        # Key BLS series IDs and their metadata
        bls_series = {
            # Labor Force Statistics (CPS)
            "LNS14000000": ("labour", "Unemployment Rate", "%"),
            "LNS11300000": ("labour", "Labor Force Participation Rate", "%"),
            "LNS12300000": ("labour", "Employment-Population Ratio", "%"),

            # Employment (CES - Non-farm payrolls)
            "CES0000000001": ("labour", "Total Nonfarm Employment", "Thousands"),
            "CES0500000003": ("labour", "Average Weekly Hours - All Employees", "Hours"),
            "CES0500000011": ("labour", "Average Hourly Earnings - All Employees", "$/Hour"),

            # Consumer Price Index (CPI)
            "CUUR0000SA0": ("prices", "Consumer Price Index (All Items)", "Index"),
            "CUUR0000SA0L1E": ("prices", "CPI - All Items Less Food & Energy", "Index"),
            "CUUR0000SAF1": ("prices", "CPI - Food", "Index"),
            "CUUR0000SAH": ("prices", "CPI - Housing", "Index"),
            "CUUR0000SETB01": ("prices", "CPI - Gasoline (All Types)", "Index"),

            # Producer Price Index (PPI)
            "WPUFD49207": ("prices", "Producer Price Index - Final Demand", "Index"),
        }

        count = 0
        session = self.get_session()

        # Fetch in batches (BLS allows up to 50 series per request)
        series_ids = list(bls_series.keys())
        batch_size = 25

        for i in range(0, len(series_ids), batch_size):
            batch = series_ids[i:i + batch_size]
            logger.info(f"Fetching BLS batch {i // batch_size + 1}...")

            data = self.fetch_bls_data(batch)
            if not data or data.get("status") != "REQUEST_SUCCEEDED":
                logger.warning(f"BLS batch {i // batch_size + 1} failed or returned no data")
                continue

            for series in data.get("Results", {}).get("series", []):
                series_id = series["seriesID"]
                if series_id in bls_series:
                    category, name, unit = bls_series[series_id]
                    indicators = self.parse_bls_series(series, category, name, unit)

                    for indicator in indicators:
                        try:
                            session.add(indicator)
                            session.commit()
                            count += 1
                            logger.info(f"✓ Stored: {name}")
                        except IntegrityError:
                            session.rollback()
                            # Update existing record
                            existing = session.query(EconomicIndicator).filter_by(
                                country_name=self.country_name,
                                category=category,
                                indicator_name=name
                            ).first()
                            if existing:
                                existing.last_value = indicator.last_value
                                existing.last_value_numeric = indicator.last_value_numeric
                                existing.previous_value = indicator.previous_value
                                existing.previous_value_numeric = indicator.previous_value_numeric
                                existing.data_date = indicator.data_date
                                session.commit()
                                logger.info(f"↻ Updated: {name}")
                        except Exception as e:
                            session.rollback()
                            logger.error(f"Error storing {name}: {e}")

        logger.info(f"BLS indicators processed: {count}")
        return count

    # ===== FRED API Methods =====

    def fetch_fred_series(self, series_id: str) -> Optional[Dict]:
        """
        Fetch series observations from FRED API

        Args:
            series_id: FRED series ID

        Returns:
            API response data or None on error
        """
        if not self.fred_api_key:
            logger.warning("FRED_API_KEY not set. Skipping FRED data. Get free key at: https://fred.stlouisfed.org/docs/api/api_key.html")
            return None

        url = f"{self.fred_api_url}/observations"
        params = {
            "series_id": series_id,
            "api_key": self.fred_api_key,
            "file_type": "json",
            "sort_order": "desc",  # Most recent first
            "limit": 10,  # Get last 10 observations
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching FRED series {series_id}: {e}")
            return None

    def parse_fred_series(self, series_data: Dict, category: str, indicator_name: str, unit: str = "") -> List[EconomicIndicator]:
        """Parse FRED series data into EconomicIndicator objects"""
        indicators = []

        if "observations" not in series_data or not series_data["observations"]:
            return indicators

        observations = series_data["observations"]

        # Find valid observations (exclude "." values)
        valid_obs = [obs for obs in observations if obs["value"] != "."]

        if len(valid_obs) == 0:
            return indicators

        # Latest and previous
        latest = valid_obs[0]
        previous = valid_obs[1] if len(valid_obs) > 1 else None

        # Highest and lowest
        values = [float(obs["value"]) for obs in valid_obs]
        highest_val = max(values) if values else None
        lowest_val = min(values) if values else None

        # Parse date
        data_date = datetime.strptime(latest["date"], "%Y-%m-%d")

        indicator = EconomicIndicator(
            country_name=self.country_name,
            category=category,
            indicator_name=indicator_name,
            last_value=latest["value"],
            last_value_numeric=float(latest["value"]),
            previous_value=previous["value"] if previous else None,
            previous_value_numeric=float(previous["value"]) if previous else None,
            highest_value=str(highest_val) if highest_val is not None else None,
            highest_value_numeric=highest_val,
            lowest_value=str(lowest_val) if lowest_val is not None else None,
            lowest_value_numeric=lowest_val,
            unit=unit,
            frequency="Quarterly" if "GDP" in indicator_name else "Monthly",
            reference_period=latest["date"],
            data_date=data_date,
            source="Federal Reserve Economic Data (FRED)",
            data_source_api="fred-api",
        )
        indicators.append(indicator)

        return indicators

    def fetch_fred_indicators(self) -> int:
        """
        Fetch key FRED indicators

        Returns:
            Number of indicators successfully stored
        """
        if not self.fred_api_key:
            logger.warning("Skipping FRED indicators (no API key)")
            return 0

        logger.info("Fetching FRED indicators...")

        # Key FRED series IDs and their metadata
        fred_series = {
            # GDP
            "GDP": ("gdp", "Gross Domestic Product", "Billions $"),
            "GDPC1": ("gdp", "Real Gross Domestic Product", "Billions Chained 2017 $"),
            "A191RL1Q225SBEA": ("gdp", "GDP Growth Rate", "%"),

            # Interest Rates
            "FEDFUNDS": ("money", "Federal Funds Effective Rate", "%"),
            "DFF": ("money", "Federal Funds Rate (Daily)", "%"),
            "DGS10": ("money", "10-Year Treasury Constant Maturity Rate", "%"),
            "DGS2": ("money", "2-Year Treasury Constant Maturity Rate", "%"),
            "MORTGAGE30US": ("housing", "30-Year Fixed Rate Mortgage Average", "%"),

            # Money Supply
            "M2SL": ("money", "M2 Money Supply", "Billions $"),
            "M1SL": ("money", "M1 Money Supply", "Billions $"),

            # Housing
            "CSUSHPISA": ("housing", "S&P/Case-Shiller U.S. National Home Price Index", "Index"),
            "HOUST": ("housing", "Housing Starts", "Thousands"),
            "PERMIT": ("housing", "New Private Housing Units Authorized", "Thousands"),

            # Trade
            "BOPGSTB": ("trade", "Trade Balance: Goods and Services", "Millions $"),
            "IMPGS": ("trade", "Imports of Goods and Services", "Millions $"),
            "EXPGS": ("trade", "Exports of Goods and Services", "Millions $"),

            # Government
            "GFDEBTN": ("government", "Federal Debt: Total Public Debt", "Millions $"),
            "FYFSD": ("government", "Federal Surplus or Deficit", "Millions $"),

            # Business
            "INDPRO": ("business", "Industrial Production Index", "Index"),
            "UMCSENT": ("business", "University of Michigan Consumer Sentiment", "Index"),
            "RSXFS": ("business", "Retail Sales", "Millions $"),
        }

        count = 0
        session = self.get_session()

        for series_id, (category, name, unit) in fred_series.items():
            logger.info(f"Fetching FRED: {name}...")

            data = self.fetch_fred_series(series_id)
            if not data:
                continue

            indicators = self.parse_fred_series(data, category, name, unit)

            for indicator in indicators:
                try:
                    session.add(indicator)
                    session.commit()
                    count += 1
                    logger.info(f"✓ Stored: {name}")
                except IntegrityError:
                    session.rollback()
                    # Update existing record
                    existing = session.query(EconomicIndicator).filter_by(
                        country_name=self.country_name,
                        category=category,
                        indicator_name=name
                    ).first()
                    if existing:
                        existing.last_value = indicator.last_value
                        existing.last_value_numeric = indicator.last_value_numeric
                        existing.previous_value = indicator.previous_value
                        existing.previous_value_numeric = indicator.previous_value_numeric
                        existing.data_date = indicator.data_date
                        session.commit()
                        logger.info(f"↻ Updated: {name}")
                except Exception as e:
                    session.rollback()
                    logger.error(f"Error storing {name}: {e}")

        logger.info(f"FRED indicators processed: {count}")
        return count

    def log_fetch_result(self, endpoint: str, category: str, status: str, records_fetched: int, records_stored: int, error_msg: str = None):
        """Log fetch operation to database"""
        try:
            session = self.get_session()
            log_entry = EconomicDataFetchLog(
                endpoint=endpoint,
                country=self.country_name,
                category=category,
                status=status,
                records_fetched=records_fetched,
                records_stored=records_stored,
                error_message=error_msg,
                triggered_by="manual-script",
            )
            session.add(log_entry)
            session.commit()
        except Exception as e:
            logger.error(f"Error logging fetch result: {e}")

    def populate_all_data(self) -> Dict[str, int]:
        """
        Populate all USA economics data

        Returns:
            Dictionary with counts per source
        """
        results = {
            "bls": 0,
            "fred": 0,
            "total": 0,
        }

        print("\n" + "=" * 80)
        print("USA ECONOMICS DATA POPULATION")
        print("=" * 80)
        print(f"\nCountry: {self.country_name}")
        print(f"Database: {country_db_manager.get_country_db_name(self.country_slug)}")
        print()

        # Initialize database
        if not self.initialize_database():
            logger.error("Failed to initialize database. Exiting.")
            return results

        try:
            # Fetch BLS data
            print("\n📊 BUREAU OF LABOR STATISTICS (BLS)")
            print("-" * 80)
            bls_count = self.fetch_bls_indicators()
            results["bls"] = bls_count
            self.log_fetch_result("bls-api", "all", "success" if bls_count > 0 else "failed", bls_count, bls_count)

            # Fetch FRED data
            print("\n📈 FEDERAL RESERVE ECONOMIC DATA (FRED)")
            print("-" * 80)
            fred_count = self.fetch_fred_indicators()
            results["fred"] = fred_count
            self.log_fetch_result("fred-api", "all", "success" if fred_count > 0 else "failed", fred_count, fred_count)

            results["total"] = bls_count + fred_count

            print("\n" + "=" * 80)
            print("SUMMARY")
            print("=" * 80)
            print(f"BLS indicators:  {bls_count}")
            print(f"FRED indicators: {fred_count}")
            print(f"TOTAL:           {results['total']}")
            print("=" * 80 + "\n")

            if results["total"] > 0:
                print("✅ USA economics data populated successfully!")
                print("\nYou can now view the data at:")
                print("  Frontend: United States Economic Indicators dashboard")
                print("  API: http://localhost:8001/api/v1/market-intelligence/data/usa-economics")
            else:
                print("⚠️  No data was populated. Check the logs above for errors.")

        finally:
            self.close_session()

        return results


def main():
    """Main execution function"""
    fetcher = USAEconomicsDataFetcher()

    try:
        results = fetcher.populate_all_data()

        # Exit with success if we got any data
        sys.exit(0 if results["total"] > 0 else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
