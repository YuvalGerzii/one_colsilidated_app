"""
Economics API Data Parser

Parses different response formats from Sugra AI Economics API
and prepares them for database storage.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class EconomicsDataParser:
    """Parser for economics API responses"""

    @staticmethod
    def parse_numeric_value(value_str: str) -> Optional[float]:
        """
        Parse numeric value from string, handling various formats

        Examples:
            "25440" -> 25440.0
            "3.30" -> 3.30
            "-3.70" -> -3.70
            "1.37M" -> 1.37
            "13.09B" -> 13.09
        """
        if not value_str or value_str == "null":
            return None

        try:
            # Remove commas and spaces
            clean_str = str(value_str).replace(',', '').strip()

            # Handle M (million), B (billion), T (trillion) suffixes
            multipliers = {'M': 1, 'B': 1000, 'T': 1000000, 'K': 0.001}

            for suffix, multiplier in multipliers.items():
                if clean_str.endswith(suffix):
                    return float(clean_str[:-1]) * multiplier

            # Regular number
            return float(clean_str)
        except (ValueError, TypeError) as e:
            logger.warning(f"Could not parse numeric value '{value_str}': {str(e)}")
            return None

    @staticmethod
    def parse_date_reference(ref_str: str) -> Optional[datetime]:
        """
        Parse date reference string to datetime

        Examples:
            "Nov/25" -> datetime(2025, 11, 1)
            "2025-11" -> datetime(2025, 11, 1)
            "Q3/2025" -> datetime(2025, 7, 1)
        """
        if not ref_str:
            return None

        try:
            # Handle "Nov/25" format
            month_map = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
            }

            if '/' in ref_str:
                parts = ref_str.split('/')
                if len(parts) == 2:
                    month_str, year_str = parts

                    # Handle month abbreviation
                    if month_str in month_map:
                        month = month_map[month_str]
                    else:
                        month = int(month_str)

                    # Handle 2-digit year
                    year = int(year_str)
                    if year < 100:
                        year += 2000

                    return datetime(year, month, 1)

            # Handle "2025-11" format
            if '-' in ref_str:
                parts = ref_str.split('-')
                if len(parts) >= 2:
                    year = int(parts[0])
                    month = int(parts[1])
                    day = int(parts[2]) if len(parts) > 2 else 1
                    return datetime(year, month, day)

            # Handle "Q3/2025" format
            if ref_str.startswith('Q'):
                quarter_match = re.match(r'Q(\d)/(\d{4})', ref_str)
                if quarter_match:
                    quarter = int(quarter_match.group(1))
                    year = int(quarter_match.group(2))
                    month = (quarter - 1) * 3 + 1
                    return datetime(year, month, 1)

            return None
        except (ValueError, IndexError) as e:
            logger.warning(f"Could not parse date reference '{ref_str}': {str(e)}")
            return None

    def parse_countries_overview(self, data: List[Dict]) -> List[Dict]:
        """
        Parse countries overview response

        Input format:
        [
            {
                "Country": "United States",
                "GDP": "25440",
                "GDP Growth": "3.30",
                "Inflation Rate": "3.40",
                ...
            }
        ]

        Returns list of normalized country data dicts
        """
        parsed_data = []

        for country_data in data:
            try:
                parsed = {
                    'country_name': country_data.get('Country'),
                    'gdp': self.parse_numeric_value(country_data.get('GDP')),
                    'gdp_growth': self.parse_numeric_value(country_data.get('GDP Growth')),
                    'inflation_rate': self.parse_numeric_value(country_data.get('Inflation Rate')),
                    'interest_rate': self.parse_numeric_value(country_data.get('Interest Rate')),
                    'unemployment_rate': self.parse_numeric_value(country_data.get('Jobless Rate')),
                    'population': self.parse_numeric_value(country_data.get('Population')),
                    'current_account': self.parse_numeric_value(country_data.get('Current Account')),
                    'debt_to_gdp': self.parse_numeric_value(country_data.get('Debt/GDP')),
                    'government_budget': self.parse_numeric_value(country_data.get('Gov. Budget')),
                    'data_date': datetime.now(),
                    'data_source': 'economics-api',
                    'raw_data': country_data
                }
                parsed_data.append(parsed)
            except Exception as e:
                logger.error(f"Error parsing country data: {str(e)}")
                continue

        return parsed_data

    def parse_economic_indicators(
        self,
        data: List[Dict],
        country: str,
        category: str
    ) -> List[Dict]:
        """
        Parse economic indicators response

        Input format:
        [
            {
                "Related": "Consumer Confidence",
                "Last": "50.3",
                "Previous": "53.6",
                "Highest": "111",
                "Lowest": "50",
                "Reference": "Nov/25",
                "Unit": "points"
            }
        ]

        Returns list of normalized indicator dicts
        """
        parsed_data = []

        for indicator in data:
            try:
                indicator_name = indicator.get('Related', 'Unknown')
                last_value = indicator.get('Last')
                reference = indicator.get('Reference')

                parsed = {
                    'country_name': country,
                    'category': category,
                    'indicator_name': indicator_name,
                    'last_value': last_value,
                    'last_value_numeric': self.parse_numeric_value(last_value),
                    'previous_value': indicator.get('Previous'),
                    'previous_value_numeric': self.parse_numeric_value(indicator.get('Previous')),
                    'highest_value': indicator.get('Highest'),
                    'highest_value_numeric': self.parse_numeric_value(indicator.get('Highest')),
                    'lowest_value': indicator.get('Lowest'),
                    'lowest_value_numeric': self.parse_numeric_value(indicator.get('Lowest')),
                    'unit': indicator.get('Unit'),
                    'frequency': indicator.get('Frequency'),
                    'reference_period': reference,
                    'data_date': self.parse_date_reference(reference) or datetime.now(),
                    'source': indicator.get('Source'),
                    'raw_data': indicator,
                    'data_source_api': 'economics-api'
                }
                parsed_data.append(parsed)
            except Exception as e:
                logger.error(f"Error parsing indicator {indicator.get('Related')}: {str(e)}")
                continue

        return parsed_data

    def parse_indicator_for_history(
        self,
        indicator_data: Dict,
        country: str,
        category: str
    ) -> Optional[Dict]:
        """
        Parse a single indicator for time series history tracking
        """
        try:
            indicator_name = indicator_data.get('Related', 'Unknown')
            last_value = indicator_data.get('Last')
            reference = indicator_data.get('Reference')
            observation_date = self.parse_date_reference(reference) or datetime.now()

            # Calculate change from previous
            last_numeric = self.parse_numeric_value(last_value)
            prev_numeric = self.parse_numeric_value(indicator_data.get('Previous'))

            change_from_previous = None
            change_percent = None

            if last_numeric is not None and prev_numeric is not None and prev_numeric != 0:
                change_from_previous = last_numeric - prev_numeric
                change_percent = (change_from_previous / prev_numeric) * 100

            return {
                'country_name': country,
                'category': category,
                'indicator_name': indicator_name,
                'observation_date': observation_date,
                'value': last_value,
                'value_numeric': last_numeric,
                'unit': indicator_data.get('Unit'),
                'change_from_previous': change_from_previous,
                'change_percent': change_percent,
                'frequency': indicator_data.get('Frequency'),
                'source': indicator_data.get('Source'),
                'data_source_api': 'economics-api'
            }
        except Exception as e:
            logger.error(f"Error parsing indicator for history: {str(e)}")
            return None

    def calculate_change_metrics(
        self,
        current: float,
        previous: float
    ) -> Dict[str, Optional[float]]:
        """Calculate change metrics between two values"""
        if current is None or previous is None:
            return {
                'absolute_change': None,
                'percent_change': None
            }

        absolute_change = current - previous
        percent_change = None

        if previous != 0:
            percent_change = (absolute_change / previous) * 100

        return {
            'absolute_change': absolute_change,
            'percent_change': percent_change
        }

    def extract_country_code(self, country_name: str) -> Optional[str]:
        """Extract ISO country code from country name"""
        # Simple mapping for common countries
        country_codes = {
            'United States': 'US',
            'China': 'CN',
            'Japan': 'JP',
            'Germany': 'DE',
            'United Kingdom': 'GB',
            'France': 'FR',
            'India': 'IN',
            'Italy': 'IT',
            'Brazil': 'BR',
            'Canada': 'CA',
            'Russia': 'RU',
            'South Korea': 'KR',
            'Spain': 'ES',
            'Mexico': 'MX',
            'Indonesia': 'ID',
            'Netherlands': 'NL',
            'Saudi Arabia': 'SA',
            'Turkey': 'TR',
            'Switzerland': 'CH',
            'Poland': 'PL',
            'Belgium': 'BE',
            'Sweden': 'SE',
            'Israel': 'IL',
            'Australia': 'AU',
            'Euro Area': 'EU',
        }

        return country_codes.get(country_name)

    def validate_indicator_data(self, indicator: Dict) -> bool:
        """Validate that indicator data has minimum required fields"""
        required_fields = ['country_name', 'category', 'indicator_name']
        return all(indicator.get(field) for field in required_fields)
