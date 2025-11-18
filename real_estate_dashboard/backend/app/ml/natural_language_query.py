"""
Natural Language Query Engine

Enables natural language queries like:
- "Show me multifamily deals in Miami under $5M"
- "What's the average ROI for properties in ZIP 90210?"
- "Find all single family homes with NOI over $50k"
"""

import logging
import re
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class NaturalLanguageQueryEngine:
    """
    Natural language query engine for real estate data.

    Uses sentence transformers for semantic understanding and
    pattern matching for query parsing.
    """

    def __init__(self, use_embeddings: bool = False):
        """
        Initialize the NL query engine.

        Args:
            use_embeddings: Whether to use sentence embeddings (requires model download)
        """
        self.use_embeddings = use_embeddings
        self.embedding_model = None

        if use_embeddings:
            try:
                logger.info("Loading sentence transformer model...")
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Sentence transformer loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load embedding model: {e}. Using pattern matching only.")
                self.use_embeddings = False

        # Define query patterns
        self.patterns = self._initialize_patterns()

    def _initialize_patterns(self) -> Dict[str, Any]:
        """Initialize regex patterns for query parsing."""
        return {
            'property_types': {
                'multifamily': r'\b(multifamily|multi-family|apartment|apartments)\b',
                'single_family': r'\b(single family|single-family|sfr|house|houses|home|homes)\b',
                'commercial': r'\b(commercial|retail|office|industrial)\b',
                'condo': r'\b(condo|condominium|condos)\b',
                'townhouse': r'\b(townhouse|townhomes)\b',
                'land': r'\b(land|lot|lots|acreage)\b',
            },
            'metrics': {
                'price': r'\$([\d,]+[KkMmBb]?)',
                'roi': r'\b(\d+)%?\s*roi\b',
                'cap_rate': r'\b(\d+\.?\d*)%?\s*(cap\s*rate|cap)\b',
                'noi': r'\b(noi|net operating income)\s*(?:over|above|greater than)?\s*\$?([\d,]+[KkMm]?)',
                'cash_flow': r'\b(cash\s*flow)\s*(?:over|above|greater than)?\s*\$?([\d,]+[KkMm]?)',
            },
            'locations': {
                'city': r'\b(?:in|at|near)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b',
                'state': r'\b([A-Z]{2})\b',
                'zip': r'\b(\d{5})\b',
            },
            'comparisons': {
                'less_than': r'\b(under|below|less than|<)\b',
                'greater_than': r'\b(over|above|greater than|more than|>)\b',
                'equal': r'\b(equal to|equals|=)\b',
                'between': r'\b(between)\s+(\S+)\s+and\s+(\S+)\b',
            },
            'commands': {
                'show': r'\b(show|display|list|find|get)\b',
                'count': r'\b(count|how many)\b',
                'average': r'\b(average|avg|mean)\b',
                'sum': r'\b(sum|total)\b',
                'max': r'\b(max|maximum|highest)\b',
                'min': r'\b(min|minimum|lowest)\b',
            }
        }

    def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language query into structured format.

        Args:
            query: Natural language query string

        Returns:
            Dictionary with parsed query components
        """
        logger.info(f"Parsing query: {query}")

        query_lower = query.lower()
        parsed = {
            'original_query': query,
            'property_types': [],
            'filters': {},
            'location': {},
            'aggregation': None,
            'sort': None,
            'limit': None
        }

        # 1. Extract property types
        for prop_type, pattern in self.patterns['property_types'].items():
            if re.search(pattern, query_lower):
                parsed['property_types'].append(prop_type)

        # 2. Extract locations
        city_match = re.search(self.patterns['locations']['city'], query)
        if city_match:
            parsed['location']['city'] = city_match.group(1)

        state_match = re.search(self.patterns['locations']['state'], query)
        if state_match:
            parsed['location']['state'] = state_match.group(1)

        zip_match = re.search(self.patterns['locations']['zip'], query_lower)
        if zip_match:
            parsed['location']['zip_code'] = zip_match.group(1)

        # 3. Extract price filters
        price_match = re.search(self.patterns['metrics']['price'], query_lower)
        if price_match:
            price_str = price_match.group(1)
            price = self._parse_number(price_str)

            # Determine comparison operator
            if re.search(self.patterns['comparisons']['less_than'], query_lower):
                parsed['filters']['price'] = {'operator': '<', 'value': price}
            elif re.search(self.patterns['comparisons']['greater_than'], query_lower):
                parsed['filters']['price'] = {'operator': '>', 'value': price}
            else:
                parsed['filters']['price'] = {'operator': '=', 'value': price}

        # 4. Extract ROI filters
        roi_match = re.search(self.patterns['metrics']['roi'], query_lower)
        if roi_match:
            roi = float(roi_match.group(1))
            if re.search(self.patterns['comparisons']['greater_than'], query_lower):
                parsed['filters']['roi'] = {'operator': '>', 'value': roi}
            else:
                parsed['filters']['roi'] = {'operator': '=', 'value': roi}

        # 5. Extract cap rate filters
        cap_match = re.search(self.patterns['metrics']['cap_rate'], query_lower)
        if cap_match:
            cap_rate = float(cap_match.group(1))
            if re.search(self.patterns['comparisons']['greater_than'], query_lower):
                parsed['filters']['cap_rate'] = {'operator': '>', 'value': cap_rate}
            else:
                parsed['filters']['cap_rate'] = {'operator': '=', 'value': cap_rate}

        # 6. Extract NOI filters
        noi_match = re.search(self.patterns['metrics']['noi'], query_lower)
        if noi_match:
            noi_str = noi_match.group(2) if len(noi_match.groups()) > 1 else noi_match.group(1)
            noi = self._parse_number(noi_str)
            parsed['filters']['noi'] = {'operator': '>', 'value': noi}

        # 7. Extract aggregation commands
        for agg_type, pattern in self.patterns['commands'].items():
            if re.search(pattern, query_lower):
                if agg_type in ['count', 'average', 'sum', 'max', 'min']:
                    parsed['aggregation'] = agg_type
                break

        # 8. Extract limit
        limit_match = re.search(r'\b(top|first|limit)\s+(\d+)\b', query_lower)
        if limit_match:
            parsed['limit'] = int(limit_match.group(2))

        return parsed

    def _parse_number(self, num_str: str) -> float:
        """
        Parse number string with K, M, B suffixes.

        Args:
            num_str: Number string (e.g., "5M", "500K")

        Returns:
            Float value
        """
        num_str = num_str.replace(',', '').strip()

        multipliers = {
            'k': 1_000,
            'm': 1_000_000,
            'b': 1_000_000_000
        }

        for suffix, multiplier in multipliers.items():
            if num_str.lower().endswith(suffix):
                return float(num_str[:-1]) * multiplier

        return float(num_str)

    def execute_query(
        self,
        query: str,
        data: List[Dict[str, Any]],
        return_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Execute natural language query on data.

        Args:
            query: Natural language query
            data: List of data dictionaries to query
            return_metadata: Whether to return query metadata

        Returns:
            Dictionary with results and metadata
        """
        # Parse query
        parsed_query = self.parse_query(query)

        # Apply filters
        filtered_data = self._apply_filters(data, parsed_query)

        # Apply aggregation
        result = {
            'query': query,
            'results': []
        }

        if parsed_query['aggregation']:
            result['aggregation'] = self._apply_aggregation(
                filtered_data,
                parsed_query['aggregation']
            )
        else:
            # Return filtered results
            limit = parsed_query['limit'] or len(filtered_data)
            result['results'] = filtered_data[:limit]

        result['count'] = len(filtered_data)

        if return_metadata:
            result['parsed_query'] = parsed_query

        return result

    def _apply_filters(
        self,
        data: List[Dict[str, Any]],
        parsed_query: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Apply filters to data based on parsed query.

        Args:
            data: Data to filter
            parsed_query: Parsed query structure

        Returns:
            Filtered data
        """
        filtered = data.copy()

        # Property type filter
        if parsed_query['property_types']:
            filtered = [
                item for item in filtered
                if item.get('property_type') in parsed_query['property_types']
            ]

        # Location filters
        location = parsed_query['location']
        if location.get('city'):
            filtered = [
                item for item in filtered
                if item.get('city', '').lower() == location['city'].lower()
            ]

        if location.get('state'):
            filtered = [
                item for item in filtered
                if item.get('state', '').upper() == location['state'].upper()
            ]

        if location.get('zip_code'):
            filtered = [
                item for item in filtered
                if str(item.get('zip_code', '')) == location['zip_code']
            ]

        # Metric filters
        for metric, condition in parsed_query['filters'].items():
            operator = condition['operator']
            value = condition['value']

            filtered = [
                item for item in filtered
                if self._compare(item.get(metric, 0), operator, value)
            ]

        return filtered

    def _compare(self, actual: float, operator: str, expected: float) -> bool:
        """Compare values based on operator."""
        if operator == '<':
            return actual < expected
        elif operator == '>':
            return actual > expected
        elif operator == '=':
            return abs(actual - expected) < 0.01  # Fuzzy equality
        elif operator == '<=':
            return actual <= expected
        elif operator == '>=':
            return actual >= expected
        return False

    def _apply_aggregation(
        self,
        data: List[Dict[str, Any]],
        agg_type: str
    ) -> Dict[str, Any]:
        """
        Apply aggregation to data.

        Args:
            data: Data to aggregate
            agg_type: Type of aggregation (count, average, sum, max, min)

        Returns:
            Aggregation results
        """
        result = {'type': agg_type}

        if agg_type == 'count':
            result['value'] = len(data)

        elif agg_type in ['average', 'sum', 'max', 'min']:
            # Try to find numeric fields to aggregate
            if data:
                numeric_fields = []
                for key, value in data[0].items():
                    if isinstance(value, (int, float)):
                        numeric_fields.append(key)

                result['fields'] = {}
                for field in numeric_fields:
                    values = [item.get(field, 0) for item in data if field in item]

                    if agg_type == 'average':
                        result['fields'][field] = float(np.mean(values))
                    elif agg_type == 'sum':
                        result['fields'][field] = float(np.sum(values))
                    elif agg_type == 'max':
                        result['fields'][field] = float(np.max(values))
                    elif agg_type == 'min':
                        result['fields'][field] = float(np.min(values))

        return result

    def suggest_queries(self, partial_query: str) -> List[str]:
        """
        Suggest query completions based on partial input.

        Args:
            partial_query: Partial query string

        Returns:
            List of suggested complete queries
        """
        suggestions = [
            "Show me multifamily deals in Miami under $5M",
            "What's the average ROI for properties in ZIP 90210?",
            "Find all single family homes with NOI over $50k",
            "List commercial properties with cap rate above 7%",
            "Show top 10 properties by price in California",
            "Count properties in New York with cash flow over $10k",
            "Find condos under $500k in Florida",
            "What's the total value of all properties?",
            "Show properties between $1M and $3M",
            "Find deals with ROI greater than 15%"
        ]

        # Simple substring matching
        if partial_query:
            suggestions = [
                s for s in suggestions
                if partial_query.lower() in s.lower()
            ]

        return suggestions[:5]


def generate_sample_property_data(n_properties: int = 100) -> List[Dict[str, Any]]:
    """
    Generate sample property data for NL query testing.

    Args:
        n_properties: Number of properties to generate

    Returns:
        List of property dictionaries
    """
    np.random.seed(42)

    cities = [
        ('Miami', 'FL', '33139'),
        ('Los Angeles', 'CA', '90210'),
        ('New York', 'NY', '10001'),
        ('Chicago', 'IL', '60601'),
        ('Dallas', 'TX', '75201')
    ]

    property_types = ['single_family', 'multifamily', 'commercial', 'condo']

    properties = []

    for i in range(n_properties):
        city, state, zip_code = cities[i % len(cities)]
        prop_type = np.random.choice(property_types)

        # Generate realistic metrics
        price = np.random.randint(200_000, 5_000_000)
        noi = price * np.random.uniform(0.03, 0.08)
        cap_rate = (noi / price) * 100
        roi = np.random.uniform(5, 25)
        cash_flow = noi * 0.7

        properties.append({
            'id': f'PROP_{i:04d}',
            'property_type': prop_type,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'price': price,
            'noi': noi,
            'cap_rate': cap_rate,
            'roi': roi,
            'cash_flow': cash_flow,
            'bedrooms': np.random.randint(1, 6) if prop_type in ['single_family', 'condo'] else None,
            'bathrooms': np.random.randint(1, 4) if prop_type in ['single_family', 'condo'] else None,
            'square_feet': np.random.randint(800, 4000)
        })

    return properties
