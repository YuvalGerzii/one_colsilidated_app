"""
Walk Score API Integration Service

Provides transit, amenities, and neighborhood walkability scores.
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
import httpx


class WalkScoreService:
    """
    Walk Score API Integration

    Fetches neighborhood data including:
    - Walk Score (0-100)
    - Transit Score (0-100)
    - Bike Score (0-100)
    - Nearby amenities
    """

    def __init__(self):
        self.api_key = os.getenv("WALKSCORE_API_KEY", "")
        self.base_url = "https://api.walkscore.com"
        self.timeout = 30.0

    async def get_scores(
        self,
        address: str,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Fetch Walk Score, Transit Score, and Bike Score.

        Args:
            address: Full property address
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Dictionary containing walkability scores
        """
        # NOTE: This is a mock implementation. Replace with actual Walk Score API calls.
        # Walk Score API documentation: https://www.walkscore.com/professional/api.php
        # You need to sign up for an API key at: https://www.walkscore.com/professional/walk-score-apis.php

        if not self.api_key:
            return self._get_mock_data(address, latitude, longitude)

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Walk Score API call
                response = await client.get(
                    f"{self.base_url}/score",
                    params={
                        "format": "json",
                        "address": address,
                        "lat": latitude,
                        "lon": longitude,
                        "transit": 1,
                        "bike": 1,
                        "wsapikey": self.api_key,
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Walk Score API error: {str(e)}")
            return self._get_mock_data(address, latitude, longitude)

    def _get_mock_data(self, address: str, latitude: float, longitude: float) -> Dict:
        """Generate mock Walk Score data for development/testing."""
        import random

        walk_score = random.randint(20, 100)
        transit_score = random.randint(10, 100)
        bike_score = random.randint(15, 100)

        # Walk Score descriptions based on score ranges
        def get_walk_description(score: int) -> str:
            if score >= 90:
                return "Walker's Paradise"
            elif score >= 70:
                return "Very Walkable"
            elif score >= 50:
                return "Somewhat Walkable"
            elif score >= 25:
                return "Car-Dependent"
            else:
                return "Very Car-Dependent"

        # Generate nearby amenities based on walk score
        amenity_types = [
            "Grocery Stores", "Restaurants", "Coffee Shops", "Parks",
            "Schools", "Banks", "Pharmacies", "Libraries", "Gyms",
            "Shopping", "Entertainment"
        ]

        num_amenities = int(walk_score / 10)  # Higher score = more amenities
        nearby_amenities = []

        for i in range(min(num_amenities, len(amenity_types))):
            amenity_type = amenity_types[i]
            count = random.randint(1, 5)
            avg_distance = round(random.uniform(0.1, 1.0), 2)

            nearby_amenities.append({
                "type": amenity_type,
                "count": count,
                "avg_distance_miles": avg_distance,
                "closest": f"{random.choice(['Whole Foods', 'Starbucks', 'Target', 'CVS', '24 Hour Fitness', 'Chase Bank'])}",
                "closest_distance": round(avg_distance * 0.7, 2),
            })

        return {
            "walk_score": walk_score,
            "transit_score": transit_score,
            "bike_score": bike_score,
            "walk_score_description": get_walk_description(walk_score),
            "transit_description": get_walk_description(transit_score),
            "bike_description": get_walk_description(bike_score),
            "nearby_amenities": nearby_amenities,
            "transit_options": {
                "bus_stops": random.randint(0, 10),
                "train_stations": random.randint(0, 3),
                "closest_transit": f"{round(random.uniform(0.1, 1.5), 2)} miles",
            },
            "source": "Walk Score (Mock Data)",
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def get_nearby_amenities(
        self,
        address: str,
        latitude: float,
        longitude: float,
        category: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch nearby amenities.

        Args:
            address: Full property address
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            category: Optional category filter (e.g., "restaurants", "schools")

        Returns:
            List of nearby amenities
        """
        scores = await self.get_scores(address, latitude, longitude)
        amenities = scores.get("nearby_amenities", [])

        if category:
            amenities = [a for a in amenities if category.lower() in a["type"].lower()]

        return amenities

    async def get_transit_options(
        self,
        address: str,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Fetch transit options near the property.

        Args:
            address: Full property address
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Transit options data
        """
        scores = await self.get_scores(address, latitude, longitude)
        return {
            "transit_score": scores.get("transit_score"),
            "transit_options": scores.get("transit_options", {}),
            "description": scores.get("transit_description"),
        }

    def interpret_walk_score(self, score: int) -> str:
        """
        Interpret walk score and return description.

        Args:
            score: Walk score (0-100)

        Returns:
            Description of walkability
        """
        if score >= 90:
            return "Walker's Paradise: Daily errands do not require a car"
        elif score >= 70:
            return "Very Walkable: Most errands can be accomplished on foot"
        elif score >= 50:
            return "Somewhat Walkable: Some errands can be accomplished on foot"
        elif score >= 25:
            return "Car-Dependent: Most errands require a car"
        else:
            return "Very Car-Dependent: Almost all errands require a car"
