"""
File Parser Service for CSV and Excel Files

Handles parsing of uploaded CSV and Excel files for market intelligence data.
"""

import pandas as pd
import io
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import UploadFile, HTTPException

logger = logging.getLogger(__name__)


class FileParserService:
    """Service for parsing CSV and Excel files into market intelligence data"""

    SUPPORTED_FORMATS = ['.csv', '.xlsx', '.xls']

    # Expected column mappings (flexible - we'll try to detect)
    COLUMN_MAPPINGS = {
        'indicator': ['indicator', 'indicator_name', 'name', 'metric', 'variable'],
        'category': ['category', 'type', 'group', 'sector'],
        'value': ['value', 'last_value', 'current', 'amount', 'number'],
        'previous': ['previous', 'previous_value', 'prior', 'last'],
        'unit': ['unit', 'units', 'measurement'],
        'date': ['date', 'period', 'timestamp', 'reference'],
    }

    @staticmethod
    def parse_file(file: UploadFile) -> List[Dict[str, Any]]:
        """
        Parse uploaded file into structured data

        Args:
            file: Uploaded file object

        Returns:
            List of dictionaries containing parsed indicator data

        Raises:
            HTTPException: If file format is not supported or parsing fails
        """
        # Validate file extension
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in FileParserService.SUPPORTED_FORMATS):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported formats: {', '.join(FileParserService.SUPPORTED_FORMATS)}"
            )

        try:
            # Read file content
            content = file.file.read()

            # Parse based on file type
            if filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(content))
            else:  # Excel
                df = pd.read_excel(io.BytesIO(content))

            # Validate dataframe
            if df.empty:
                raise HTTPException(status_code=400, detail="File contains no data")

            # Detect columns
            column_map = FileParserService._detect_columns(df)

            # Parse rows
            indicators = FileParserService._parse_dataframe(df, column_map)

            logger.info(f"Successfully parsed {len(indicators)} indicators from {filename}")
            return indicators

        except pd.errors.EmptyDataError:
            raise HTTPException(status_code=400, detail="File is empty")
        except pd.errors.ParserError as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing file: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Internal error parsing file: {str(e)}")

    @staticmethod
    def _detect_columns(df: pd.DataFrame) -> Dict[str, str]:
        """
        Detect column mappings from dataframe

        Args:
            df: Pandas dataframe

        Returns:
            Dictionary mapping standard fields to actual column names
        """
        column_map = {}
        df_columns_lower = {col: col.lower() for col in df.columns}

        for field, possible_names in FileParserService.COLUMN_MAPPINGS.items():
            for possible_name in possible_names:
                # Check if any column matches (case-insensitive)
                for actual_col, lower_col in df_columns_lower.items():
                    if possible_name in lower_col or lower_col in possible_name:
                        column_map[field] = actual_col
                        break
                if field in column_map:
                    break

        # Ensure we have at least indicator and value columns
        if 'indicator' not in column_map:
            # Try to use first column as indicator
            column_map['indicator'] = df.columns[0]
            logger.warning(f"No indicator column found, using first column: {df.columns[0]}")

        if 'value' not in column_map:
            # Try to find any numeric column
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                column_map['value'] = numeric_cols[0]
                logger.warning(f"No value column found, using first numeric column: {numeric_cols[0]}")
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Could not detect value column. Please ensure file has numeric data."
                )

        logger.info(f"Detected columns: {column_map}")
        return column_map

    @staticmethod
    def _parse_dataframe(df: pd.DataFrame, column_map: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Parse dataframe into list of indicator dictionaries

        Args:
            df: Pandas dataframe
            column_map: Mapping of standard fields to actual column names

        Returns:
            List of indicator dictionaries
        """
        indicators = []

        for idx, row in df.iterrows():
            try:
                # Extract values using column map
                indicator_name = str(row[column_map['indicator']]).strip()

                # Skip empty rows
                if not indicator_name or indicator_name.lower() in ['nan', 'none', '']:
                    continue

                # Get value
                value_raw = row[column_map['value']]
                if pd.isna(value_raw):
                    continue

                # Convert value to float if possible
                try:
                    value_numeric = float(value_raw)
                    value_str = str(value_raw)
                except (ValueError, TypeError):
                    value_str = str(value_raw)
                    value_numeric = None

                # Build indicator dictionary
                indicator = {
                    'indicator_name': indicator_name,
                    'last_value': value_str,
                    'last_value_numeric': value_numeric,
                }

                # Add optional fields
                if 'category' in column_map and column_map['category'] in row.index:
                    category = row[column_map['category']]
                    if not pd.isna(category):
                        indicator['category'] = str(category).strip()

                if 'previous' in column_map and column_map['previous'] in row.index:
                    previous = row[column_map['previous']]
                    if not pd.isna(previous):
                        try:
                            indicator['previous_value'] = str(previous)
                            indicator['previous_value_numeric'] = float(previous)
                        except (ValueError, TypeError):
                            indicator['previous_value'] = str(previous)

                if 'unit' in column_map and column_map['unit'] in row.index:
                    unit = row[column_map['unit']]
                    if not pd.isna(unit):
                        indicator['unit'] = str(unit).strip()

                if 'date' in column_map and column_map['date'] in row.index:
                    date_val = row[column_map['date']]
                    if not pd.isna(date_val):
                        indicator['reference_period'] = str(date_val).strip()
                        # Try to parse as datetime
                        try:
                            dt = pd.to_datetime(date_val)
                            indicator['data_date'] = dt.isoformat()
                        except:
                            pass

                # Calculate change if we have previous value
                if 'previous_value_numeric' in indicator and indicator['previous_value_numeric'] and value_numeric:
                    change = value_numeric - indicator['previous_value_numeric']
                    if indicator['previous_value_numeric'] != 0:
                        change_pct = (change / abs(indicator['previous_value_numeric'])) * 100
                        indicator['change_percent'] = round(change_pct, 2)
                        indicator['change_absolute'] = round(change, 2)

                indicators.append(indicator)

            except Exception as e:
                logger.warning(f"Error parsing row {idx}: {str(e)}")
                continue

        return indicators

    @staticmethod
    def validate_indicators(indicators: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate parsed indicators and return summary

        Args:
            indicators: List of parsed indicator dictionaries

        Returns:
            Validation summary dictionary
        """
        total = len(indicators)

        # Count indicators by category
        categories = {}
        has_numeric = 0
        has_previous = 0
        has_category = 0

        for ind in indicators:
            # Count numeric values
            if ind.get('last_value_numeric') is not None:
                has_numeric += 1

            # Count previous values
            if ind.get('previous_value_numeric') is not None:
                has_previous += 1

            # Count categories
            if ind.get('category'):
                has_category += 1
                cat = ind['category']
                categories[cat] = categories.get(cat, 0) + 1

        return {
            'total_indicators': total,
            'numeric_values': has_numeric,
            'with_previous': has_previous,
            'with_category': has_category,
            'categories': categories,
            'numeric_percentage': round((has_numeric / total * 100) if total > 0 else 0, 1),
        }


    @staticmethod
    def export_template(format: str = 'csv') -> bytes:
        """
        Generate a template file for data import

        Args:
            format: File format ('csv' or 'excel')

        Returns:
            File content as bytes
        """
        # Create template dataframe
        template_data = {
            'Indicator Name': [
                'GDP Growth Rate',
                'Unemployment Rate',
                'Inflation Rate',
                'Consumer Confidence Index',
                'Housing Price Index',
            ],
            'Category': [
                'GDP',
                'Labour',
                'Prices',
                'Business',
                'Housing',
            ],
            'Current Value': [3.5, 4.2, 2.8, 105.2, 285.4],
            'Previous Value': [3.2, 4.3, 3.1, 102.1, 280.5],
            'Unit': ['%', '%', '%', 'Index', 'Index'],
            'Date': ['2025-Q3', '2025-10', '2025-10', '2025-10', '2025-Q3'],
        }

        df = pd.DataFrame(template_data)

        # Export to requested format
        if format.lower() == 'csv':
            return df.to_csv(index=False).encode('utf-8')
        else:  # Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Economic Indicators')
            output.seek(0)
            return output.read()
