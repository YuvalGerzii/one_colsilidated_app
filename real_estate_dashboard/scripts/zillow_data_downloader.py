#!/usr/bin/env python3
"""
Zillow Research Data Downloader

Downloads Zillow research data CSV files to local storage.
Can be scheduled monthly via cron for automated updates.

Usage:
    python zillow_data_downloader.py

Cron example (1st of each month at 2 AM):
    0 2 1 * * /usr/bin/python3 /path/to/zillow_data_downloader.py
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
BASE_URL = "https://files.zillowstatic.com/research/public_csvs"
LEGACY_BASE_URL = "http://files.zillowstatic.com/research/public"

# Default storage path
DEFAULT_STORAGE_PATH = Path(__file__).parent.parent / "storage" / "zillow"

# Zillow dataset definitions
DATASETS = {
    # ZHVI (Zillow Home Value Index) - Home Values
    "zhvi": {
        "measures": [
            "Zhvi_AllHomes",
            "Zhvi_SingleFamilyResidence",
            "Zhvi_CondoCoop",
            "Zhvi_1Bedroom",
            "Zhvi_2Bedroom",
            "Zhvi_3Bedroom",
            "Zhvi_4Bedroom",
            "Zhvi_5BedroomOrMore",
            "MedianValuePerSqft_AllHomes",
            "Zhvi_TopTier",
            "Zhvi_BottomTier"
        ],
        "geographies": ["Metro", "State", "City", "Zip", "County", "Neighborhood"]
    },
    # ZORI (Zillow Observed Rent Index) - Rental Prices
    "zori": {
        "measures": [
            "Zori_AllHomesPlusMultifamily",
            "Zori_Sfr",
            "MedianRentalPrice_AllHomes",
            "MedianRentalPrice_Sfr",
            "MedianRentalPrice_CondoCoop",
            "MedianRentalPricePerSqft_AllHomes",
            "MedianRentalPricePerSqft_Sfr"
        ],
        "geographies": ["Metro", "State", "City", "Zip", "County"]
    },
    # For Sale Inventory
    "inventory": {
        "measures": [
            "ForSaleInventory_AllHomes",
            "ForSaleInventory_Sfr",
            "ForSaleInventory_CondoCoop",
            "DaysOnMarket_AllHomes",
            "NewListings_AllHomes",
            "PriceReduction_AllHomes"
        ],
        "geographies": ["Metro", "State", "City", "Zip", "County"]
    },
    # Sales Data
    "sales": {
        "measures": [
            "SoldCount_AllHomes",
            "NewMonthlyListings_AllHomes",
            "SaleToListRatio_AllHomes"
        ],
        "geographies": ["Metro", "State", "City", "Zip", "County"]
    }
}

# Additional standalone files
STANDALONE_FILES = [
    "MortgageRateConventionalFixed.csv",
    "CountyCrossWalk_Zillow.csv"
]


class ZillowDataDownloader:
    """Downloads and manages Zillow research data files."""

    def __init__(self, storage_path: Optional[Path] = None, max_workers: int = 5):
        self.storage_path = Path(storage_path) if storage_path else DEFAULT_STORAGE_PATH
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Setup logging
        self._setup_logging()

        # Ensure storage directory exists
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Track download statistics
        self.stats = {
            "downloaded": 0,
            "failed": 0,
            "skipped": 0,
            "total_size": 0
        }

    def _setup_logging(self):
        """Configure logging."""
        log_file = self.storage_path / "download.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _build_download_urls(self) -> List[Dict[str, str]]:
        """Build list of all download URLs."""
        urls = []

        # Build dataset URLs
        for category, config in DATASETS.items():
            for measure in config["measures"]:
                for geo in config["geographies"]:
                    filename = f"{geo}_{measure}.csv"
                    url = f"{BASE_URL}/{geo}/{filename}"
                    urls.append({
                        "url": url,
                        "filename": filename,
                        "category": category,
                        "geography": geo,
                        "measure": measure
                    })

        # Add standalone files
        for filename in STANDALONE_FILES:
            urls.append({
                "url": f"{BASE_URL}/{filename}",
                "filename": filename,
                "category": "standalone",
                "geography": "national",
                "measure": filename.replace(".csv", "")
            })

        return urls

    def _download_file(self, file_info: Dict[str, str]) -> Dict:
        """Download a single file."""
        url = file_info["url"]
        filename = file_info["filename"]
        category = file_info["category"]

        # Create category subdirectory
        category_path = self.storage_path / category
        category_path.mkdir(exist_ok=True)

        file_path = category_path / filename

        try:
            # Try primary URL
            response = self.session.get(url, timeout=60, stream=True)

            # If 404, try legacy URL pattern
            if response.status_code == 404:
                legacy_url = f"{LEGACY_BASE_URL}/{file_info['geography']}/{filename}"
                response = self.session.get(legacy_url, timeout=60, stream=True)

            if response.status_code == 200:
                # Write file
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                file_size = file_path.stat().st_size
                self.logger.info(f"Downloaded: {filename} ({file_size:,} bytes)")

                return {
                    "status": "success",
                    "filename": filename,
                    "size": file_size,
                    "path": str(file_path)
                }
            else:
                self.logger.warning(f"Failed to download {filename}: HTTP {response.status_code}")
                return {
                    "status": "failed",
                    "filename": filename,
                    "error": f"HTTP {response.status_code}"
                }

        except Exception as e:
            self.logger.error(f"Error downloading {filename}: {str(e)}")
            return {
                "status": "failed",
                "filename": filename,
                "error": str(e)
            }

    def download_all(self, categories: Optional[List[str]] = None) -> Dict:
        """
        Download all Zillow data files.

        Args:
            categories: Optional list of categories to download.
                       If None, downloads all categories.

        Returns:
            Dictionary with download statistics and results.
        """
        self.logger.info("Starting Zillow data download...")
        start_time = datetime.now()

        # Build URL list
        all_urls = self._build_download_urls()

        # Filter by categories if specified
        if categories:
            all_urls = [u for u in all_urls if u["category"] in categories]

        self.logger.info(f"Found {len(all_urls)} files to download")

        results = []

        # Download files with thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._download_file, url_info): url_info
                for url_info in all_urls
            }

            for future in as_completed(futures):
                result = future.result()
                results.append(result)

                if result["status"] == "success":
                    self.stats["downloaded"] += 1
                    self.stats["total_size"] += result.get("size", 0)
                else:
                    self.stats["failed"] += 1

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Save download manifest
        manifest = {
            "timestamp": end_time.isoformat(),
            "duration_seconds": duration,
            "statistics": self.stats,
            "results": results
        }

        manifest_path = self.storage_path / "download_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        self.logger.info(f"Download complete in {duration:.1f}s")
        self.logger.info(f"Downloaded: {self.stats['downloaded']}, Failed: {self.stats['failed']}")
        self.logger.info(f"Total size: {self.stats['total_size']:,} bytes")

        return manifest

    def download_priority_datasets(self) -> Dict:
        """Download only the most commonly used datasets."""
        priority_files = [
            # Core home values
            {"url": f"{BASE_URL}/Metro/Metro_Zhvi_AllHomes.csv", "filename": "Metro_Zhvi_AllHomes.csv", "category": "zhvi", "geography": "Metro", "measure": "Zhvi_AllHomes"},
            {"url": f"{BASE_URL}/State/State_Zhvi_AllHomes.csv", "filename": "State_Zhvi_AllHomes.csv", "category": "zhvi", "geography": "State", "measure": "Zhvi_AllHomes"},
            {"url": f"{BASE_URL}/Zip/Zip_Zhvi_AllHomes.csv", "filename": "Zip_Zhvi_AllHomes.csv", "category": "zhvi", "geography": "Zip", "measure": "Zhvi_AllHomes"},
            {"url": f"{BASE_URL}/City/City_Zhvi_AllHomes.csv", "filename": "City_Zhvi_AllHomes.csv", "category": "zhvi", "geography": "City", "measure": "Zhvi_AllHomes"},
            # Core rental data
            {"url": f"{BASE_URL}/Metro/Metro_Zori_AllHomesPlusMultifamily.csv", "filename": "Metro_Zori_AllHomesPlusMultifamily.csv", "category": "zori", "geography": "Metro", "measure": "Zori_AllHomesPlusMultifamily"},
            {"url": f"{BASE_URL}/State/State_Zori_AllHomesPlusMultifamily.csv", "filename": "State_Zori_AllHomesPlusMultifamily.csv", "category": "zori", "geography": "State", "measure": "Zori_AllHomesPlusMultifamily"},
            {"url": f"{BASE_URL}/Zip/Zip_Zori_AllHomesPlusMultifamily.csv", "filename": "Zip_Zori_AllHomesPlusMultifamily.csv", "category": "zori", "geography": "Zip", "measure": "Zori_AllHomesPlusMultifamily"},
            # Inventory
            {"url": f"{BASE_URL}/Metro/Metro_ForSaleInventory_AllHomes.csv", "filename": "Metro_ForSaleInventory_AllHomes.csv", "category": "inventory", "geography": "Metro", "measure": "ForSaleInventory_AllHomes"},
            {"url": f"{BASE_URL}/Metro/Metro_DaysOnMarket_AllHomes.csv", "filename": "Metro_DaysOnMarket_AllHomes.csv", "category": "inventory", "geography": "Metro", "measure": "DaysOnMarket_AllHomes"},
        ]

        self.logger.info("Downloading priority datasets only...")

        results = []
        for file_info in priority_files:
            result = self._download_file(file_info)
            results.append(result)

            if result["status"] == "success":
                self.stats["downloaded"] += 1
                self.stats["total_size"] += result.get("size", 0)
            else:
                self.stats["failed"] += 1

        return {
            "statistics": self.stats,
            "results": results
        }


def setup_cron_job():
    """Print instructions for setting up monthly cron job."""
    script_path = Path(__file__).absolute()

    print("\n" + "="*60)
    print("CRON JOB SETUP INSTRUCTIONS")
    print("="*60)
    print("\nTo schedule monthly downloads, add this line to your crontab:")
    print("\n  crontab -e\n")
    print("Then add this line (runs at 2 AM on the 1st of each month):\n")
    print(f"  0 2 1 * * /usr/bin/python3 {script_path}")
    print("\nAlternatively, for systemd timer, create these files:")
    print("\n  /etc/systemd/system/zillow-download.service")
    print("  /etc/systemd/system/zillow-download.timer")
    print("="*60 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download Zillow research data")
    parser.add_argument(
        "--storage",
        type=str,
        help="Storage directory path",
        default=str(DEFAULT_STORAGE_PATH)
    )
    parser.add_argument(
        "--priority-only",
        action="store_true",
        help="Download only priority datasets"
    )
    parser.add_argument(
        "--categories",
        type=str,
        nargs="+",
        choices=["zhvi", "zori", "inventory", "sales", "standalone"],
        help="Specific categories to download"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="Number of concurrent download workers"
    )
    parser.add_argument(
        "--setup-cron",
        action="store_true",
        help="Show cron setup instructions"
    )

    args = parser.parse_args()

    if args.setup_cron:
        setup_cron_job()
        sys.exit(0)

    # Initialize downloader
    downloader = ZillowDataDownloader(
        storage_path=Path(args.storage),
        max_workers=args.workers
    )

    # Run download
    if args.priority_only:
        results = downloader.download_priority_datasets()
    else:
        results = downloader.download_all(categories=args.categories)

    # Print summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"Downloaded: {results['statistics']['downloaded']} files")
    print(f"Failed: {results['statistics']['failed']} files")
    print(f"Total size: {results['statistics']['total_size']:,} bytes")
    print(f"Storage path: {downloader.storage_path}")
    print("="*60 + "\n")
