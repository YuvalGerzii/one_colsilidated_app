#!/usr/bin/env python3
"""
Government Bulk Data Downloader
Downloads real estate data from government sources WITHOUT API keys
"""

import requests
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from zipfile import ZipFile
from io import BytesIO
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GovernmentBulkDownloader:
    """Download bulk real estate data from government sources"""

    def __init__(self, output_dir: str = "./data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_hud_fair_market_rents(self, year: int = 2024) -> str:
        """
        Download HUD Fair Market Rents
        No API key required
        """
        url = f"https://www.huduser.gov/portal/datasets/fmr/fmr{year}/FY{year % 100}_FMRs.zip"

        logger.info(f"Downloading HUD FMR data for FY{year}...")

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Extract ZIP
            with ZipFile(BytesIO(response.content)) as zip_file:
                # List contents
                logger.info(f"ZIP contains: {zip_file.namelist()}")

                # Extract all files
                extract_path = self.output_dir / f"hud_fmr_{year}"
                extract_path.mkdir(exist_ok=True)

                zip_file.extractall(extract_path)

                logger.info(f"✓ Extracted to {extract_path}")

                # Try to load DBF file if exists
                dbf_files = list(extract_path.glob("*.dbf"))
                if dbf_files:
                    logger.info(f"Found DBF file: {dbf_files[0]}")
                    logger.info("Note: Use dbfread or simpledbf to read DBF files")

                return str(extract_path)

        except Exception as e:
            logger.error(f"Error downloading HUD FMR: {e}")
            raise

    def download_census_acs_pums(self, year: int = 2023, period: str = "1-Year") -> str:
        """
        Download Census ACS PUMS housing data
        No API key required
        """
        base_url = "https://www2.census.gov/programs-surveys/acs/data/pums"
        url = f"{base_url}/{year}/{period}/csv_hus.zip"

        logger.info(f"Downloading Census ACS PUMS {period} data for {year}...")
        logger.info("⚠️  Warning: This is a LARGE file (500MB+)")

        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            # Save ZIP file
            zip_path = self.output_dir / f"census_acs_pums_{year}_{period.replace('-', '_')}.zip"

            # Download with progress
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            logger.info(f"Downloaded: {percent:.1f}%")

            logger.info(f"✓ Downloaded to {zip_path}")

            # Extract
            extract_path = self.output_dir / f"census_acs_pums_{year}"
            extract_path.mkdir(exist_ok=True)

            with ZipFile(zip_path, 'r') as zip_file:
                logger.info(f"Extracting {zip_file.namelist()[0]}...")
                zip_file.extractall(extract_path)

            logger.info(f"✓ Extracted to {extract_path}")

            # Load sample
            csv_files = list(extract_path.glob("*.csv"))
            if csv_files:
                logger.info("Loading sample data...")
                df = pd.read_csv(csv_files[0], nrows=5)
                logger.info(f"Columns: {df.columns.tolist()}")
                logger.info(f"\nSample:\n{df.head()}")

            return str(extract_path)

        except Exception as e:
            logger.error(f"Error downloading Census PUMS: {e}")
            raise

    def download_fhfa_house_price_index(self, geography: str = "state") -> str:
        """
        Download FHFA House Price Index
        No API key required

        Geography options: national, state, metro, 3zip, 5zip
        """
        base_url = "https://www.fhfa.gov/DataTools/Downloads/Documents/HPI"

        urls = {
            'national': f"{base_url}/HPI_AT_us.xlsx",
            'state': f"{base_url}/HPI_AT_state.xlsx",
            'metro': f"{base_url}/HPI_AT_metro.xlsx",
            '3zip': f"{base_url}/HPI_AT_3zip.xlsx",
            '5zip': f"{base_url}/HPI_AT_5zip.xlsx",
        }

        if geography not in urls:
            raise ValueError(f"Invalid geography. Choose from: {list(urls.keys())}")

        url = urls[geography]

        logger.info(f"Downloading FHFA HPI {geography} data...")

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Save Excel file
            file_path = self.output_dir / f"fhfa_hpi_{geography}.xlsx"

            with open(file_path, 'wb') as f:
                f.write(response.content)

            logger.info(f"✓ Downloaded to {file_path}")

            # Load sample with pandas
            logger.info("Loading sample data...")
            df = pd.read_excel(file_path, nrows=10)
            logger.info(f"Columns: {df.columns.tolist()}")
            logger.info(f"\nSample:\n{df.head()}")

            return str(file_path)

        except Exception as e:
            logger.error(f"Error downloading FHFA HPI: {e}")
            raise

    def download_sec_edgar_quarterly_data(self, year: int = 2024, quarter: int = 1) -> str:
        """
        Download SEC EDGAR quarterly financial data
        No API key required
        """
        url = f"https://www.sec.gov/files/dera/data/financial-statement-data-sets/{year}q{quarter}.zip"

        headers = {
            'User-Agent': 'Real Estate Dashboard research@example.com'
        }

        logger.info(f"Downloading SEC EDGAR {year}Q{quarter} data...")

        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()

            # Extract ZIP
            extract_path = self.output_dir / f"sec_edgar_{year}q{quarter}"
            extract_path.mkdir(exist_ok=True)

            with ZipFile(BytesIO(response.content)) as zip_file:
                logger.info(f"ZIP contains: {zip_file.namelist()}")
                zip_file.extractall(extract_path)

            logger.info(f"✓ Extracted to {extract_path}")

            # Load sample from num.txt
            num_file = extract_path / "num.txt"
            if num_file.exists():
                logger.info("Loading sample numeric data...")
                df = pd.read_csv(num_file, sep='\t', nrows=10)
                logger.info(f"Columns: {df.columns.tolist()}")

            return str(extract_path)

        except Exception as e:
            logger.error(f"Error downloading SEC EDGAR data: {e}")
            raise

    def download_datagov_real_estate_sales(self) -> str:
        """
        Download Connecticut Real Estate Sales from Data.gov
        No API key required
        Example dataset - other states may have similar data
        """
        url = "https://data.ct.gov/api/views/5mzw-sjtu/rows.csv?accessType=DOWNLOAD"

        logger.info("Downloading Connecticut Real Estate Sales...")

        try:
            df = pd.read_csv(url)

            # Save to CSV
            file_path = self.output_dir / "ct_real_estate_sales.csv"
            df.to_csv(file_path, index=False)

            logger.info(f"✓ Downloaded {len(df)} records to {file_path}")
            logger.info(f"Columns: {df.columns.tolist()}")
            logger.info(f"\nSample:\n{df.head()}")

            return str(file_path)

        except Exception as e:
            logger.error(f"Error downloading Data.gov dataset: {e}")
            raise

    def download_corgis_real_estate_dataset(self) -> str:
        """
        Download CORGIS Real Estate dataset
        No API key required
        """
        url = "https://corgis-edu.github.io/corgis/datasets/csv/real_estate/real_estate.csv"

        logger.info("Downloading CORGIS Real Estate dataset...")

        try:
            df = pd.read_csv(url)

            # Save to CSV
            file_path = self.output_dir / "corgis_real_estate.csv"
            df.to_csv(file_path, index=False)

            logger.info(f"✓ Downloaded {len(df)} records to {file_path}")
            logger.info(f"Columns: {df.columns.tolist()}")
            logger.info(f"\nSample:\n{df.head()}")

            return str(file_path)

        except Exception as e:
            logger.error(f"Error downloading CORGIS dataset: {e}")
            raise

    def download_all(self):
        """Download all available datasets"""
        logger.info("="*80)
        logger.info("DOWNLOADING ALL GOVERNMENT BULK DATA")
        logger.info("="*80)

        results = {}

        # HUD FMR
        try:
            results['hud_fmr'] = self.download_hud_fair_market_rents()
        except Exception as e:
            logger.error(f"Failed HUD FMR: {e}")
            results['hud_fmr'] = None

        # FHFA HPI - State level
        try:
            results['fhfa_hpi_state'] = self.download_fhfa_house_price_index('state')
        except Exception as e:
            logger.error(f"Failed FHFA HPI: {e}")
            results['fhfa_hpi_state'] = None

        # Data.gov CT Sales
        try:
            results['ct_sales'] = self.download_datagov_real_estate_sales()
        except Exception as e:
            logger.error(f"Failed Data.gov: {e}")
            results['ct_sales'] = None

        # CORGIS Dataset
        try:
            results['corgis'] = self.download_corgis_real_estate_dataset()
        except Exception as e:
            logger.error(f"Failed CORGIS: {e}")
            results['corgis'] = None

        # SEC EDGAR (skip by default - very large)
        # try:
        #     results['sec_edgar'] = self.download_sec_edgar_quarterly_data()
        # except Exception as e:
        #     logger.error(f"Failed SEC EDGAR: {e}")

        # Census PUMS (skip by default - VERY large)
        # try:
        #     results['census_pums'] = self.download_census_acs_pums()
        # except Exception as e:
        #     logger.error(f"Failed Census PUMS: {e}")

        logger.info("\n" + "="*80)
        logger.info("DOWNLOAD SUMMARY")
        logger.info("="*80)

        for name, path in results.items():
            status = "✓" if path else "✗"
            logger.info(f"{status} {name}: {path or 'FAILED'}")

        return results


def main():
    """Run bulk data downloader"""
    print(f"\n🏛️  Government Bulk Data Downloader")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    downloader = GovernmentBulkDownloader(output_dir="./government_data")

    print("\n📊 Available Datasets:")
    print("  1. HUD Fair Market Rents")
    print("  2. Census ACS PUMS (Housing)")
    print("  3. FHFA House Price Index")
    print("  4. SEC EDGAR Quarterly Data")
    print("  5. Data.gov Real Estate Sales")
    print("  6. CORGIS Real Estate Dataset")
    print("  7. Download ALL (quick datasets only)")
    print("  0. Exit")

    while True:
        choice = input("\n👉 Enter choice: ").strip()

        if choice == '0':
            break
        elif choice == '1':
            year = input("Year (default 2024): ").strip() or "2024"
            downloader.download_hud_fair_market_rents(int(year))
        elif choice == '2':
            year = input("Year (default 2023): ").strip() or "2023"
            period = input("Period (1-Year/5-Year, default 1-Year): ").strip() or "1-Year"
            confirm = input("⚠️  This is 500MB+. Continue? (y/n): ")
            if confirm.lower() == 'y':
                downloader.download_census_acs_pums(int(year), period)
        elif choice == '3':
            print("\nGeography options: national, state, metro, 3zip, 5zip")
            geo = input("Geography (default state): ").strip() or "state"
            downloader.download_fhfa_house_price_index(geo)
        elif choice == '4':
            year = input("Year (default 2024): ").strip() or "2024"
            quarter = input("Quarter (1-4, default 1): ").strip() or "1"
            downloader.download_sec_edgar_quarterly_data(int(year), int(quarter))
        elif choice == '5':
            downloader.download_datagov_real_estate_sales()
        elif choice == '6':
            downloader.download_corgis_real_estate_dataset()
        elif choice == '7':
            confirm = input("Download all quick datasets? (y/n): ")
            if confirm.lower() == 'y':
                downloader.download_all()
        else:
            print("❌ Invalid choice")

    print("\n✅ Done!\n")


if __name__ == "__main__":
    main()
