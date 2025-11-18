"""
Example Usage of Excel Model Generation System
Demonstrates various ways to generate financial models from the database
"""

import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import generators
from excel_model_generator import (
    DCFModelGenerator,
    LBOModelGenerator,
    MergerModelGenerator,
    BatchModelGenerator,
    PortfolioCompany,
    FinancialMetric
)


# ============================================================================
# SETUP DATABASE CONNECTION
# ============================================================================

def setup_database():
    """Setup database connection"""
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql://portfolio_user:password@localhost/portfolio_db'
    )
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return SessionLocal()


# ============================================================================
# EXAMPLE 1: Generate Single DCF Model
# ============================================================================

def example_1_dcf_model():
    """Generate a DCF model for a specific company"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Generate DCF Model")
    print("="*60)
    
    db = setup_database()
    
    # Get a company (replace with actual UUID)
    company_id = '123e4567-e89b-12d3-a456-426614174000'
    
    try:
        # Create generator
        dcf_gen = DCFModelGenerator(db, company_id)
        
        # Generate model
        output_path = '/home/claude/generated_models/Example_DCF.xlsx'
        dcf_gen.generate(output_path)
        
        print(f"✓ DCF model generated successfully!")
        print(f"  File: {output_path}")
        print(f"  Company: {dcf_gen.company.company_name}")
        print(f"  Financial periods: {len(dcf_gen.financials)}")
    
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    finally:
        db.close()


# ============================================================================
# EXAMPLE 2: Generate LBO Model
# ============================================================================

def example_2_lbo_model():
    """Generate an LBO model"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Generate LBO Model")
    print("="*60)
    
    db = setup_database()
    company_id = '123e4567-e89b-12d3-a456-426614174000'
    
    try:
        lbo_gen = LBOModelGenerator(db, company_id)
        output_path = '/home/claude/generated_models/Example_LBO.xlsx'
        lbo_gen.generate(output_path)
        
        print(f"✓ LBO model generated!")
        print(f"  File: {output_path}")
        print(f"  Purchase Price: ${lbo_gen.company.purchase_price:,.0f}")
        print(f"  Entry Multiple: {lbo_gen.company.entry_multiple:.1f}x")
    
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    finally:
        db.close()


# ============================================================================
# EXAMPLE 3: Generate Merger Model (2 Companies)
# ============================================================================

def example_3_merger_model():
    """Generate a Merger & Acquisition model"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Generate Merger Model")
    print("="*60)
    
    db = setup_database()
    
    acquirer_id = '123e4567-e89b-12d3-a456-426614174000'
    target_id = '987fcdeb-51a2-43f1-9876-543210fedcba'
    
    try:
        merger_gen = MergerModelGenerator(db, acquirer_id, target_id)
        output_path = '/home/claude/generated_models/Example_Merger.xlsx'
        merger_gen.generate(output_path)
        
        print(f"✓ Merger model generated!")
        print(f"  File: {output_path}")
        print(f"  Acquirer: {merger_gen.acquirer.company_name}")
        print(f"  Target: {merger_gen.target.company_name}")
    
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    finally:
        db.close()


# ============================================================================
# EXAMPLE 4: Batch Generation (All Models)
# ============================================================================

def example_4_batch_generation():
    """Generate all models for a company"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Batch Generation (All Models)")
    print("="*60)
    
    db = setup_database()
    company_id = '123e4567-e89b-12d3-a456-426614174000'
    
    try:
        batch_gen = BatchModelGenerator(db)
        results = batch_gen.generate_all_models(
            company_id,
            output_dir='/home/claude/generated_models'
        )
        
        print(f"\n✓ Batch generation complete!")
        print(f"  Total models attempted: {len(results)}")
        
        for model_type, file_path in results.items():
            if file_path:
                print(f"  ✓ {model_type}: {os.path.basename(file_path)}")
            else:
                print(f"  ✗ {model_type}: Failed")
    
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    finally:
        db.close()


# ============================================================================
# EXAMPLE 5: Generate Models for All Companies in a Fund
# ============================================================================

def example_5_fund_batch_generation():
    """Generate DCF models for all companies in a fund"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Fund-Wide Generation")
    print("="*60)
    
    db = setup_database()
    fund_id = '456e7890-f12b-34c5-d678-901234567890'
    
    try:
        # Get all active companies in the fund
        companies = db.query(PortfolioCompany).filter(
            PortfolioCompany.fund_id == fund_id,
            PortfolioCompany.company_status == 'Active'
        ).all()
        
        print(f"Found {len(companies)} active companies in fund")
        
        for company in companies:
            try:
                dcf_gen = DCFModelGenerator(db, str(company.company_id))
                
                output_dir = '/home/claude/generated_models/fund_models'
                os.makedirs(output_dir, exist_ok=True)
                
                company_slug = company.company_name.replace(' ', '_')
                output_path = f'{output_dir}/{company_slug}_DCF.xlsx'
                
                dcf_gen.generate(output_path)
                print(f"  ✓ {company.company_name}")
            
            except Exception as e:
                print(f"  ✗ {company.company_name}: {e}")
    
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    finally:
        db.close()


# ============================================================================
# EXAMPLE 6: Generate with Custom Scenarios
# ============================================================================

def example_6_scenario_generation():
    """Generate multiple scenarios for the same company"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Scenario Generation")
    print("="*60)
    
    db = setup_database()
    company_id = '123e4567-e89b-12d3-a456-426614174000'
    
    scenarios = [
        ('Base_Case', {'revenue_growth': 0.10, 'margin': 0.20}),
        ('Upside', {'revenue_growth': 0.15, 'margin': 0.25}),
        ('Downside', {'revenue_growth': 0.05, 'margin': 0.15})
    ]
    
    try:
        for scenario_name, assumptions in scenarios:
            dcf_gen = DCFModelGenerator(db, company_id)
            
            output_path = f'/home/claude/generated_models/DCF_{scenario_name}.xlsx'
            dcf_gen.generate(output_path)
            
            print(f"  ✓ {scenario_name}: {output_path}")
    
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    finally:
        db.close()


# ============================================================================
# EXAMPLE 7: Check What Models Exist for a Company
# ============================================================================

def example_7_list_existing_models():
    """List all generated models for a company"""
    print("\n" + "="*60)
    print("EXAMPLE 7: List Existing Models")
    print("="*60)
    
    db = setup_database()
    company_id = '123e4567-e89b-12d3-a456-426614174000'
    
    try:
        company = db.query(PortfolioCompany).filter(
            PortfolioCompany.company_id == company_id
        ).first()
        
        if not company:
            print("Company not found")
            return
        
        company_slug = company.company_name.replace(' ', '_')
        output_dir = '/home/claude/generated_models'
        
        if os.path.exists(output_dir):
            files = [
                f for f in os.listdir(output_dir)
                if f.startswith(company_slug) and f.endswith('.xlsx')
            ]
            
            print(f"\nFound {len(files)} models for {company.company_name}:")
            for file in sorted(files):
                file_path = os.path.join(output_dir, file)
                stat = os.stat(file_path)
                size_mb = stat.st_size / 1024 / 1024
                created = datetime.fromtimestamp(stat.st_ctime)
                
                print(f"  • {file}")
                print(f"    Size: {size_mb:.2f} MB")
                print(f"    Created: {created.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("No models directory found")
    
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    finally:
        db.close()


# ============================================================================
# EXAMPLE 8: Using the API (HTTP Requests)
# ============================================================================

def example_8_api_usage():
    """Example of using the REST API"""
    print("\n" + "="*60)
    print("EXAMPLE 8: API Usage (with requests library)")
    print("="*60)
    
    try:
        import requests
        
        # Make sure API server is running: python api_model_generator.py
        base_url = 'http://localhost:8000'
        
        # Generate a DCF model
        response = requests.post(
            f'{base_url}/api/v1/models/generate',
            json={
                'company_id': '123e4567-e89b-12d3-a456-426614174000',
                'model_type': 'DCF',
                'scenario_name': 'Base Case'
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Model generated via API!")
            print(f"  File: {result['file_path']}")
            print(f"  Company: {result['company_name']}")
            print(f"  Generated at: {result['generated_at']}")
        else:
            print(f"✗ API request failed: {response.status_code}")
            print(f"  {response.text}")
    
    except ImportError:
        print("Install requests library: pip install requests")
    except Exception as e:
        print(f"✗ Failed: {e}")


# ============================================================================
# EXAMPLE 9: Validate Generated Model
# ============================================================================

def example_9_validate_model():
    """Validate that a generated model has correct data"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Validate Generated Model")
    print("="*60)
    
    from openpyxl import load_workbook
    
    db = setup_database()
    company_id = '123e4567-e89b-12d3-a456-426614174000'
    
    try:
        # Get company data
        company = db.query(PortfolioCompany).filter(
            PortfolioCompany.company_id == company_id
        ).first()
        
        if not company:
            print("Company not found")
            return
        
        # Generate model
        dcf_gen = DCFModelGenerator(db, company_id)
        output_path = '/home/claude/generated_models/Validation_Test.xlsx'
        dcf_gen.generate(output_path)
        
        # Load and validate
        wb = load_workbook(output_path)
        sheet = wb['DCF']
        
        print("\nValidation Checks:")
        
        # Check 1: Company name
        excel_name = sheet['B2'].value
        db_name = company.company_name
        if excel_name == db_name:
            print(f"  ✓ Company name matches: {excel_name}")
        else:
            print(f"  ✗ Name mismatch: Excel='{excel_name}' vs DB='{db_name}'")
        
        # Check 2: Formulas exist
        formula_cells = ['D8', 'D9', 'C22']  # Example formula cells
        formulas_ok = True
        for cell_ref in formula_cells:
            cell = sheet[cell_ref]
            if cell.value and str(cell.value).startswith('='):
                print(f"  ✓ Formula preserved in {cell_ref}")
            else:
                print(f"  ✗ Formula missing in {cell_ref}")
                formulas_ok = False
        
        if formulas_ok:
            print("\n✓ Model validation passed!")
        else:
            print("\n⚠ Some validation checks failed")
    
    except Exception as e:
        print(f"✗ Validation failed: {e}")
    
    finally:
        db.close()


# ============================================================================
# EXAMPLE 10: Performance Test
# ============================================================================

def example_10_performance_test():
    """Test generation performance"""
    print("\n" + "="*60)
    print("EXAMPLE 10: Performance Test")
    print("="*60)
    
    import time
    
    db = setup_database()
    company_id = '123e4567-e89b-12d3-a456-426614174000'
    
    try:
        # Time DCF generation
        start = time.time()
        dcf_gen = DCFModelGenerator(db, company_id)
        dcf_gen.generate('/home/claude/generated_models/Perf_Test_DCF.xlsx')
        dcf_time = time.time() - start
        
        # Time LBO generation
        start = time.time()
        lbo_gen = LBOModelGenerator(db, company_id)
        lbo_gen.generate('/home/claude/generated_models/Perf_Test_LBO.xlsx')
        lbo_time = time.time() - start
        
        # Time batch generation
        start = time.time()
        batch_gen = BatchModelGenerator(db)
        batch_gen.generate_all_models(company_id)
        batch_time = time.time() - start
        
        print(f"\nPerformance Results:")
        print(f"  DCF model:   {dcf_time:.2f} seconds")
        print(f"  LBO model:   {lbo_time:.2f} seconds")
        print(f"  Batch (all): {batch_time:.2f} seconds")
        print(f"\n✓ All models generated in under {batch_time:.0f}s")
    
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    finally:
        db.close()


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Run example demonstrations"""
    print("\n" + "="*70)
    print(" "*15 + "EXCEL MODEL GENERATION EXAMPLES")
    print("="*70)
    
    examples = [
        ("Generate Single DCF Model", example_1_dcf_model),
        ("Generate LBO Model", example_2_lbo_model),
        ("Generate Merger Model", example_3_merger_model),
        ("Batch Generation (All Models)", example_4_batch_generation),
        ("Fund-Wide Generation", example_5_fund_batch_generation),
        ("Scenario Generation", example_6_scenario_generation),
        ("List Existing Models", example_7_list_existing_models),
        ("API Usage Example", example_8_api_usage),
        ("Validate Model", example_9_validate_model),
        ("Performance Test", example_10_performance_test),
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. Run All Examples")
    print(f"  Q. Quit")
    
    choice = input("\nSelect example (1-10, 0 for all, Q to quit): ").strip()
    
    if choice.upper() == 'Q':
        print("Goodbye!")
        return
    
    if choice == '0':
        for name, func in examples:
            func()
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        _, func = examples[int(choice) - 1]
        func()
    else:
        print("Invalid choice")
    
    print("\n" + "="*70)
    print("Examples complete!")
    print("="*70)


if __name__ == '__main__':
    main()
