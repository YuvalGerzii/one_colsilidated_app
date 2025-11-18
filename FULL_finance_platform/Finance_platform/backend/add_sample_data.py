"""
Script to add sample data for testing the Portfolio Dashboard application.
"""

import asyncio
from datetime import date, timedelta
from decimal import Decimal
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.fund import Fund
from app.models.company import PortfolioCompany
from app.config import settings


def add_sample_data():
    """Add sample funds and companies to the database."""

    # Create database connection
    engine = create_engine(str(settings.DATABASE_URL))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_funds = db.query(Fund).count()
        if existing_funds > 0:
            print(f"✓ Database already has {existing_funds} funds. Skipping sample data creation.")
            return

        print("Creating sample funds and companies...")

        # Create Fund I
        fund1 = Fund(
            fund_name="Growth Fund I",
            fund_number=1,
            vintage_year=2020,
            fund_size=Decimal("500000000"),  # $500M
            committed_capital=Decimal("500000000"),
            drawn_capital=Decimal("300000000"),  # $300M drawn
            distributed_capital=Decimal("50000000"),  # $50M distributed
            target_irr=Decimal("0.25"),  # 25% target IRR
            fund_strategy="Buyout",
            sector_focus=["Technology", "Healthcare", "Financial Services"],
            geographic_focus=["North America", "Europe"],
            fund_status="Active",
            inception_date=date(2020, 1, 15),
            close_date=date(2020, 6, 30),
            final_close_date=date(2020, 12, 31)
        )
        db.add(fund1)
        db.flush()  # Get the fund ID

        # Create Fund II
        fund2 = Fund(
            fund_name="Growth Fund II",
            fund_number=2,
            vintage_year=2022,
            fund_size=Decimal("750000000"),  # $750M
            committed_capital=Decimal("750000000"),
            drawn_capital=Decimal("200000000"),  # $200M drawn
            distributed_capital=Decimal("0"),
            target_irr=Decimal("0.30"),  # 30% target IRR
            fund_strategy="Growth Equity",
            sector_focus=["Technology", "Consumer"],
            geographic_focus=["North America"],
            fund_status="Active",
            inception_date=date(2022, 3, 1),
            close_date=date(2022, 9, 15),
            final_close_date=date(2023, 3, 31)
        )
        db.add(fund2)
        db.flush()

        print(f"✓ Created 2 funds")

        # Create sample companies for Fund I
        companies_fund1 = [
            {
                "company_name": "TechCorp Solutions",
                "company_legal_name": "TechCorp Solutions, Inc.",
                "website": "https://techcorp.example.com",
                "investment_date": date(2020, 7, 15),
                "deal_type": "LBO",
                "sector": "Technology",
                "industry": "SaaS",
                "sub_sector": "Enterprise Software",
                "business_description": "Leading provider of cloud-based enterprise resource planning software for mid-market companies.",
                "headquarters_city": "San Francisco",
                "headquarters_state": "California",
                "headquarters_country": "United States",
                "entry_revenue": Decimal("50000000"),  # $50M
                "entry_ebitda": Decimal("12000000"),  # $12M
                "entry_multiple": Decimal("8.33"),  # 8.33x EBITDA
                "purchase_price": Decimal("100000000"),  # $100M
                "equity_invested": Decimal("40000000"),  # $40M equity
                "debt_raised": Decimal("60000000"),  # $60M debt
                "ownership_percentage": Decimal("0.75"),  # 75%
                "company_status": "Active",
                "risk_rating": "Medium",
                "internal_rating": "B+",
                "ceo_name": "Sarah Johnson",
                "cfo_name": "Michael Chen",
                "board_members": ["Sarah Johnson", "Michael Chen", "Partner 1", "Partner 2"]
            },
            {
                "company_name": "HealthTech Innovations",
                "company_legal_name": "HealthTech Innovations LLC",
                "website": "https://healthtech.example.com",
                "investment_date": date(2021, 3, 1),
                "deal_type": "Growth Equity",
                "sector": "Healthcare",
                "industry": "Digital Health",
                "sub_sector": "Telemedicine",
                "business_description": "Digital healthcare platform connecting patients with healthcare providers via video consultations.",
                "headquarters_city": "Boston",
                "headquarters_state": "Massachusetts",
                "headquarters_country": "United States",
                "entry_revenue": Decimal("30000000"),  # $30M
                "entry_ebitda": Decimal("6000000"),  # $6M
                "entry_multiple": Decimal("10.0"),  # 10x EBITDA
                "purchase_price": Decimal("60000000"),  # $60M
                "equity_invested": Decimal("25000000"),  # $25M equity
                "debt_raised": Decimal("35000000"),  # $35M debt
                "ownership_percentage": Decimal("0.60"),  # 60%
                "company_status": "Active",
                "risk_rating": "Low",
                "internal_rating": "A",
                "ceo_name": "Dr. Emily Rodriguez",
                "cfo_name": "David Park"
            },
            {
                "company_name": "FinServe Group",
                "company_legal_name": "FinServe Group Corporation",
                "website": "https://finserve.example.com",
                "investment_date": date(2020, 11, 15),
                "deal_type": "LBO",
                "sector": "Financial Services",
                "industry": "Wealth Management",
                "sub_sector": "RIA",
                "business_description": "Registered investment advisor firm providing wealth management services to high-net-worth individuals.",
                "headquarters_city": "New York",
                "headquarters_state": "New York",
                "headquarters_country": "United States",
                "entry_revenue": Decimal("25000000"),  # $25M
                "entry_ebitda": Decimal("8000000"),  # $8M
                "entry_multiple": Decimal("6.25"),  # 6.25x EBITDA
                "purchase_price": Decimal("50000000"),  # $50M
                "equity_invested": Decimal("20000000"),  # $20M equity
                "debt_raised": Decimal("30000000"),  # $30M debt
                "ownership_percentage": Decimal("0.80"),  # 80%
                "company_status": "Exited",
                "exit_date": date(2023, 6, 30),
                "exit_type": "Strategic Sale",
                "exit_proceeds": Decimal("90000000"),  # $90M exit
                "realized_moic": Decimal("4.5"),  # 4.5x MOIC
                "realized_irr": Decimal("0.48"),  # 48% IRR
                "risk_rating": "Low",
                "internal_rating": "A+",
                "ceo_name": "Robert Williams",
                "cfo_name": "Jennifer Martinez"
            }
        ]

        for company_data in companies_fund1:
            company = PortfolioCompany(
                fund_id=fund1.id,
                **company_data
            )
            db.add(company)

        # Create sample companies for Fund II
        companies_fund2 = [
            {
                "company_name": "CloudScale Systems",
                "company_legal_name": "CloudScale Systems Inc.",
                "website": "https://cloudscale.example.com",
                "investment_date": date(2022, 10, 1),
                "deal_type": "Growth Equity",
                "sector": "Technology",
                "industry": "Cloud Infrastructure",
                "sub_sector": "DevOps",
                "business_description": "Platform for automating cloud infrastructure deployment and management across multiple cloud providers.",
                "headquarters_city": "Seattle",
                "headquarters_state": "Washington",
                "headquarters_country": "United States",
                "entry_revenue": Decimal("40000000"),  # $40M
                "entry_ebitda": Decimal("10000000"),  # $10M
                "entry_multiple": Decimal("12.0"),  # 12x EBITDA
                "purchase_price": Decimal("120000000"),  # $120M
                "equity_invested": Decimal("50000000"),  # $50M equity
                "debt_raised": Decimal("70000000"),  # $70M debt
                "ownership_percentage": Decimal("0.55"),  # 55%
                "company_status": "Active",
                "risk_rating": "Medium",
                "internal_rating": "B",
                "ceo_name": "Alex Kumar",
                "cfo_name": "Lisa Thompson"
            },
            {
                "company_name": "EcommerceNow",
                "company_legal_name": "EcommerceNow LLC",
                "website": "https://ecommercenow.example.com",
                "investment_date": date(2023, 2, 15),
                "deal_type": "Growth Equity",
                "sector": "Consumer",
                "industry": "E-commerce",
                "sub_sector": "Direct-to-Consumer",
                "business_description": "D2C e-commerce platform for sustainable home goods and furniture.",
                "headquarters_city": "Austin",
                "headquarters_state": "Texas",
                "headquarters_country": "United States",
                "entry_revenue": Decimal("35000000"),  # $35M
                "entry_ebitda": Decimal("5000000"),  # $5M
                "entry_multiple": Decimal("15.0"),  # 15x EBITDA
                "purchase_price": Decimal("75000000"),  # $75M
                "equity_invested": Decimal("30000000"),  # $30M equity
                "debt_raised": Decimal("45000000"),  # $45M debt
                "ownership_percentage": Decimal("0.50"),  # 50%
                "company_status": "Active",
                "risk_rating": "High",
                "internal_rating": "B-",
                "ceo_name": "Maria Garcia",
                "cfo_name": "James Anderson"
            }
        ]

        for company_data in companies_fund2:
            company = PortfolioCompany(
                fund_id=fund2.id,
                **company_data
            )
            db.add(company)

        # Commit all changes
        db.commit()

        print(f"✓ Created 5 portfolio companies")
        print("\n✅ Sample data successfully added!")
        print("\nSummary:")
        print(f"  - Funds: 2 (Growth Fund I, Growth Fund II)")
        print(f"  - Companies: 5 (3 in Fund I, 2 in Fund II)")
        print(f"  - 1 exited company (FinServe Group)")
        print(f"  - Total capital invested: ${Decimal('165000000'):,.0f}")
        print("\nYou can now view the data in the Portfolio Dashboard at http://localhost:3000")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error adding sample data: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_sample_data()
