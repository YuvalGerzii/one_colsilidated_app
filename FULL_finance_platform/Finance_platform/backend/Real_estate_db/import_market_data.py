#!/usr/bin/env python3
"""
Real Estate Market Data Import Script
Imports NYC and Miami market data into Portfolio Dashboard database

Usage:
    python import_market_data.py --db-name portfolio_dashboard --user postgres

Requirements:
    pip install psycopg2-binary pandas --break-system-packages
"""

import pandas as pd
import psycopg2
from psycopg2 import sql
import argparse
import sys
from datetime import datetime

def create_connection(db_name, user, password=None, host='localhost', port=5432):
    """Create PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print(f"✅ Connected to database: {db_name}")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        sys.exit(1)

def import_market_data(conn, csv_file='market_data.csv'):
    """Import market_data.csv into market_data table"""
    print(f"\n📊 Importing {csv_file}...")
    
    try:
        # Read CSV
        df = pd.read_csv(csv_file)
        print(f"   Found {len(df)} records in CSV")
        
        # Convert period to date format
        df['period'] = pd.to_datetime(df['period']).dt.date
        
        # Replace NaN with None (NULL in SQL)
        df = df.where(pd.notnull(df), None)
        
        # Insert data
        cursor = conn.cursor()
        inserted = 0
        skipped = 0
        
        for idx, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO market_data (
                        market_name, submarket_name, property_type, property_class,
                        metric_name, metric_value, metric_unit, period,
                        data_source, confidence_level, notes
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    row['market_name'], row['submarket_name'], row['property_type'],
                    row['property_class'], row['metric_name'], row['metric_value'],
                    row['metric_unit'], row['period'], row['data_source'],
                    row['confidence_level'], row['notes']
                ))
                if cursor.rowcount > 0:
                    inserted += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"   ⚠️  Error on row {idx}: {e}")
                skipped += 1
        
        conn.commit()
        cursor.close()
        print(f"   ✅ Inserted {inserted} records, skipped {skipped} duplicates")
        return True
        
    except Exception as e:
        print(f"   ❌ Error importing market_data: {e}")
        conn.rollback()
        return False

def import_comp_transactions(conn, csv_file='comp_transactions.csv'):
    """Import comp_transactions.csv into comp_transactions table"""
    print(f"\n🏢 Importing {csv_file}...")
    
    try:
        # Read CSV
        df = pd.read_csv(csv_file)
        print(f"   Found {len(df)} records in CSV")
        
        # Convert dates
        df['sale_date'] = pd.to_datetime(df['sale_date']).dt.date
        
        # Replace NaN with None
        df = df.where(pd.notnull(df), None)
        
        # Insert data
        cursor = conn.cursor()
        inserted = 0
        skipped = 0
        
        for idx, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO comp_transactions (
                        address, city, submarket, state, property_type, property_class,
                        sale_date, sale_price, price_per_unit, price_per_sf, cap_rate,
                        units, total_sf, year_built, buyer, seller,
                        financing_type, occupancy_at_sale, deal_type,
                        data_source, source_url, notes
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT DO NOTHING
                """, (
                    row['address'], row['city'], row['submarket'], row['state'],
                    row['property_type'], row['property_class'], row['sale_date'],
                    row['sale_price'], row['price_per_unit'], row['price_per_sf'],
                    row['cap_rate'], row['units'], row['total_sf'], row['year_built'],
                    row['buyer'], row['seller'], row['financing_type'],
                    row['occupancy_at_sale'], row['deal_type'], row['data_source'],
                    row['source_url'], row['notes']
                ))
                if cursor.rowcount > 0:
                    inserted += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"   ⚠️  Error on row {idx}: {e}")
                skipped += 1
        
        conn.commit()
        cursor.close()
        print(f"   ✅ Inserted {inserted} records, skipped {skipped} duplicates")
        return True
        
    except Exception as e:
        print(f"   ❌ Error importing comp_transactions: {e}")
        conn.rollback()
        return False

def import_economic_indicators(conn, csv_file='economic_indicators.csv'):
    """Import economic_indicators.csv into economic_indicators table"""
    print(f"\n📈 Importing {csv_file}...")
    
    try:
        # Read CSV
        df = pd.read_csv(csv_file)
        print(f"   Found {len(df)} records in CSV")
        
        # Convert dates
        df['period'] = pd.to_datetime(df['period']).dt.date
        
        # Replace NaN with None
        df = df.where(pd.notnull(df), None)
        
        # Insert data
        cursor = conn.cursor()
        inserted = 0
        skipped = 0
        
        for idx, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO economic_indicators (
                        geography, geography_type, indicator_name, indicator_value,
                        indicator_unit, period, period_type, data_source, notes
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    row['geography'], row['geography_type'], row['indicator_name'],
                    row['indicator_value'], row['indicator_unit'], row['period'],
                    row['period_type'], row['data_source'], row['notes']
                ))
                if cursor.rowcount > 0:
                    inserted += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"   ⚠️  Error on row {idx}: {e}")
                skipped += 1
        
        conn.commit()
        cursor.close()
        print(f"   ✅ Inserted {inserted} records, skipped {skipped} duplicates")
        return True
        
    except Exception as e:
        print(f"   ❌ Error importing economic_indicators: {e}")
        conn.rollback()
        return False

def verify_import(conn):
    """Verify data was imported successfully"""
    print("\n🔍 Verifying import...")
    
    cursor = conn.cursor()
    
    # Check market_data
    cursor.execute("SELECT COUNT(*) FROM market_data")
    market_count = cursor.fetchone()[0]
    print(f"   market_data: {market_count} records")
    
    # Check comp_transactions
    cursor.execute("SELECT COUNT(*) FROM comp_transactions")
    comp_count = cursor.fetchone()[0]
    print(f"   comp_transactions: {comp_count} records")
    
    # Check economic_indicators
    cursor.execute("SELECT COUNT(*) FROM economic_indicators")
    econ_count = cursor.fetchone()[0]
    print(f"   economic_indicators: {econ_count} records")
    
    cursor.close()
    
    print("\n📊 Sample Queries:")
    print("   - Latest NYC multifamily cap rates:")
    print("     SELECT * FROM v_latest_cap_rates WHERE market_name = 'NYC' AND property_type = 'multifamily';")
    print("\n   - Recent Manhattan transactions:")
    print("     SELECT * FROM v_recent_comp_transactions WHERE city = 'Manhattan' LIMIT 10;")
    print("\n   - Miami population and employment:")
    print("     SELECT * FROM v_latest_economic_indicators WHERE geography = 'Miami Metro';")

def main():
    parser = argparse.ArgumentParser(description='Import NYC/Miami market data into Portfolio Dashboard')
    parser.add_argument('--db-name', default='portfolio_dashboard', help='Database name')
    parser.add_argument('--user', default='postgres', help='Database user')
    parser.add_argument('--password', help='Database password (optional)')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', type=int, default=5432, help='Database port')
    parser.add_argument('--schema', default='real_estate_market_data_schema.sql', 
                       help='Schema file to apply first')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🏗️  REAL ESTATE MARKET DATA IMPORT")
    print("=" * 70)
    
    # Connect to database
    conn = create_connection(
        db_name=args.db_name,
        user=args.user,
        password=args.password,
        host=args.host,
        port=args.port
    )
    
    # Apply schema (optional - user may have already applied it)
    print(f"\n📋 Note: Ensure schema '{args.schema}' has been applied to database")
    print("   Run: psql -U postgres -d portfolio_dashboard -f real_estate_market_data_schema.sql")
    
    response = input("\nHave you applied the schema? (y/n): ")
    if response.lower() != 'y':
        print("\n⚠️  Please apply the schema first and re-run this script")
        sys.exit(1)
    
    # Import data
    success = True
    success = import_market_data(conn, 'market_data.csv') and success
    success = import_comp_transactions(conn, 'comp_transactions.csv') and success
    success = import_economic_indicators(conn, 'economic_indicators.csv') and success
    
    # Verify
    verify_import(conn)
    
    # Close connection
    conn.close()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ IMPORT COMPLETE!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Run sample queries to verify data")
        print("2. Create dashboards using the views (v_latest_cap_rates, etc.)")
        print("3. Integrate with your financial models")
        print("4. Set up automated updates for ongoing data collection")
    else:
        print("\n" + "=" * 70)
        print("⚠️  IMPORT COMPLETED WITH ERRORS")
        print("=" * 70)
        print("Some records may not have been imported. Check errors above.")

if __name__ == "__main__":
    main()
