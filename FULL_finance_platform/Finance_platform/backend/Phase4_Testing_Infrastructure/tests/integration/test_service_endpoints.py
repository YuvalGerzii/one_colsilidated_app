"""
Integration tests for service endpoints.

Tests model generation and PDF extraction services.
"""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient

try:
    from app.models import Company, GeneratedModel, PDFDocument
except ImportError:
    Company = GeneratedModel = PDFDocument = None


# ============================================================================
# MODEL GENERATION SERVICE TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.service
class TestModelGenerationEndpoints:
    """Test model generation API endpoints."""
    
    def test_model_service_health(self, client: TestClient):
        """Test GET /api/v1/models/health - Service health check."""
        response = client.get("/api/v1/models/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "ready"]
    
    def test_generate_dcf_model(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_financials: list,
        sample_valuation
    ):
        """Test POST /api/v1/models/generate - Generate DCF model."""
        request_payload = {
            "company_id": sample_company.company_id,
            "model_type": "DCF"
        }
        
        response = client.post("/api/v1/models/generate", json=request_payload)
        
        assert response.status_code in [200, 201, 202]
        data = response.json()
        
        # Verify response structure
        assert "file_url" in data or "file_path" in data or "message" in data
        
        if "file_url" in data:
            assert "DCF" in data["file_url"]
    
    def test_generate_lbo_model(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_financials: list
    ):
        """Test POST /api/v1/models/generate - Generate LBO model."""
        request_payload = {
            "company_id": sample_company.company_id,
            "model_type": "LBO"
        }
        
        response = client.post("/api/v1/models/generate", json=request_payload)
        
        assert response.status_code in [200, 201, 202]
        data = response.json()
        
        if "file_url" in data:
            assert "LBO" in data["file_url"]
    
    def test_generate_merger_model(
        self, 
        client: TestClient,
        sample_company: Company,
        multiple_companies: list
    ):
        """Test POST /api/v1/models/generate-merger - Generate merger model."""
        if len(multiple_companies) >= 2:
            request_payload = {
                "acquirer_id": multiple_companies[0].company_id,
                "target_id": multiple_companies[1].company_id
            }
            
            response = client.post("/api/v1/models/generate-merger", json=request_payload)
            
            assert response.status_code in [200, 201, 202]
            data = response.json()
            
            if "file_url" in data:
                assert "Merger" in data["file_url"]
    
    def test_generate_batch_models(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_financials: list
    ):
        """Test POST /api/v1/models/generate-batch - Generate all models."""
        request_payload = {
            "company_id": sample_company.company_id
        }
        
        response = client.post("/api/v1/models/generate-batch", json=request_payload)
        
        assert response.status_code in [200, 201, 202]
        data = response.json()
        
        # Verify batch response structure
        assert "successful_models" in data or "models" in data or "message" in data
        
        if "successful_models" in data:
            # Should generate DCF and LBO at minimum
            assert data["successful_models"] >= 1
    
    def test_list_generated_models(
        self, 
        client: TestClient,
        sample_company: Company
    ):
        """Test GET /api/v1/models/list/{company_id} - List generated models."""
        response = client.get(f"/api/v1/models/list/{sample_company.company_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
    
    def test_download_model(
        self, 
        client: TestClient,
        sample_company: Company
    ):
        """Test GET /api/v1/models/download/{file} - Download model."""
        # First generate a model
        generate_response = client.post("/api/v1/models/generate", json={
            "company_id": sample_company.company_id,
            "model_type": "DCF"
        })
        
        if generate_response.status_code in [200, 201]:
            generate_data = generate_response.json()
            
            if "file_url" in generate_data:
                # Extract filename from URL
                file_url = generate_data["file_url"]
                filename = Path(file_url).name
                
                # Try to download
                download_response = client.get(f"/api/v1/models/download/{filename}")
                
                # Should return file or redirect
                assert download_response.status_code in [200, 302, 404]
    
    def test_generate_model_without_data(self, client: TestClient, sample_company: Company):
        """Test generating model for company without financial data."""
        # Create a new company without any financial data
        company_payload = {
            "fund_id": sample_company.fund_id,
            "company_name": "Data-less Company",
            "sector": "Technology",
            "investment_date": "2024-01-01",
            "initial_investment": 10000000.00,
            "status": "Active"
        }
        
        create_response = client.post("/api/v1/companies", json=company_payload)
        new_company_id = create_response.json()["company_id"]
        
        # Try to generate model
        response = client.post("/api/v1/models/generate", json={
            "company_id": new_company_id,
            "model_type": "DCF"
        })
        
        # Should either:
        # 1. Return 400/422 (missing required data)
        # 2. Return 200 with warning message
        # 3. Generate model with placeholder data
        assert response.status_code in [200, 201, 400, 422]
    
    def test_generate_invalid_model_type(
        self, 
        client: TestClient,
        sample_company: Company
    ):
        """Test generating model with invalid model type."""
        request_payload = {
            "company_id": sample_company.company_id,
            "model_type": "INVALID_TYPE"
        }
        
        response = client.post("/api/v1/models/generate", json=request_payload)
        
        assert response.status_code in [400, 422]
    
    @pytest.mark.slow
    def test_model_generation_performance(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_financials: list
    ):
        """Test model generation performance."""
        import time
        
        request_payload = {
            "company_id": sample_company.company_id,
            "model_type": "DCF"
        }
        
        start_time = time.time()
        response = client.post("/api/v1/models/generate", json=request_payload)
        end_time = time.time()
        
        assert response.status_code in [200, 201, 202]
        
        # Model generation should complete in < 30 seconds
        generation_time = end_time - start_time
        assert generation_time < 30.0


# ============================================================================
# PDF EXTRACTION SERVICE TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.service
class TestPDFExtractionEndpoints:
    """Test PDF extraction API endpoints."""
    
    def test_pdf_service_health(self, client: TestClient):
        """Test GET /api/v1/pdf/health - Service health check."""
        response = client.get("/api/v1/pdf/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "ready"]
    
    def test_upload_pdf(self, client: TestClient, sample_company: Company):
        """Test POST /api/v1/pdf/upload - Upload PDF for extraction."""
        # Create a dummy PDF file for testing
        pdf_content = b"%PDF-1.4\n%Test PDF content\n%%EOF"
        
        files = {
            "file": ("test_financials.pdf", pdf_content, "application/pdf")
        }
        data = {
            "company_id": sample_company.company_id
        }
        
        response = client.post("/api/v1/pdf/upload", files=files, data=data)
        
        # Should return 200/201 (success) or 422 (invalid PDF format)
        assert response.status_code in [200, 201, 422]
        
        if response.status_code in [200, 201]:
            response_data = response.json()
            assert "document_id" in response_data or "message" in response_data
    
    def test_upload_invalid_file_type(self, client: TestClient, sample_company: Company):
        """Test uploading non-PDF file."""
        # Try to upload a non-PDF file
        files = {
            "file": ("test.txt", b"Not a PDF", "text/plain")
        }
        data = {
            "company_id": sample_company.company_id
        }
        
        response = client.post("/api/v1/pdf/upload", files=files, data=data)
        
        assert response.status_code in [400, 422]
    
    def test_list_pdf_documents(self, client: TestClient, sample_company: Company):
        """Test GET /api/v1/pdf/documents/{company_id} - List PDFs."""
        response = client.get(f"/api/v1/pdf/documents/{sample_company.company_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
    
    def test_get_pdf_extraction_stats(self, client: TestClient):
        """Test GET /api/v1/pdf/stats - Extraction statistics."""
        response = client.get("/api/v1/pdf/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify stats structure
        assert "total_documents" in data or "stats" in data or "message" in data
    
    def test_validate_pdf_extraction(self, client: TestClient):
        """Test POST /api/v1/pdf/validate-extraction - Validate extraction."""
        # This endpoint would validate extracted data against database
        validation_payload = {
            "document_id": 1,  # Assuming document exists
            "extracted_data": {
                "revenue": 100000000.00,
                "ebitda": 20000000.00
            }
        }
        
        response = client.post("/api/v1/pdf/validate-extraction", json=validation_payload)
        
        # Should return 200 (validated) or 404 (document not found)
        assert response.status_code in [200, 404]
    
    def test_reprocess_pdf_with_ai(self, client: TestClient):
        """Test POST /api/v1/pdf/reprocess/{doc_id} - Reprocess with AI."""
        # Assuming document with ID 1 exists
        response = client.post("/api/v1/pdf/reprocess/1", json={"use_ai": True})
        
        # Should return 200 (reprocessed), 404 (not found), or 422 (invalid)
        assert response.status_code in [200, 404, 422]
    
    def test_pdf_extraction_with_ocr(self, client: TestClient, sample_company: Company):
        """Test PDF extraction for scanned documents (OCR)."""
        # This would test OCR functionality for image-based PDFs
        # For now, just verify the endpoint exists
        
        pdf_content = b"%PDF-1.4\n%Scanned PDF content\n%%EOF"
        
        files = {
            "file": ("scanned_document.pdf", pdf_content, "application/pdf")
        }
        data = {
            "company_id": sample_company.company_id,
            "use_ocr": True
        }
        
        response = client.post("/api/v1/pdf/upload", files=files, data=data)
        
        assert response.status_code in [200, 201, 422]
    
    @pytest.mark.slow
    def test_pdf_extraction_performance(self, client: TestClient, sample_company: Company):
        """Test PDF extraction performance."""
        import time
        
        pdf_content = b"%PDF-1.4\n%Test financial statements\n%%EOF"
        
        files = {
            "file": ("performance_test.pdf", pdf_content, "application/pdf")
        }
        data = {
            "company_id": sample_company.company_id
        }
        
        start_time = time.time()
        response = client.post("/api/v1/pdf/upload", files=files, data=data)
        end_time = time.time()
        
        # PDF extraction should complete in < 30 seconds
        extraction_time = end_time - start_time
        assert extraction_time < 30.0


# ============================================================================
# INTEGRATED SERVICE TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.service
class TestIntegratedServices:
    """Test integrated workflows between services."""
    
    def test_pdf_to_model_workflow(
        self, 
        client: TestClient,
        sample_company: Company
    ):
        """Test complete workflow: PDF → extraction → model generation."""
        # Step 1: Upload PDF
        pdf_content = b"%PDF-1.4\n%Financial statements\n%%EOF"
        
        files = {
            "file": ("q4_financials.pdf", pdf_content, "application/pdf")
        }
        data = {
            "company_id": sample_company.company_id
        }
        
        upload_response = client.post("/api/v1/pdf/upload", files=files, data=data)
        
        if upload_response.status_code in [200, 201]:
            # Step 2: Verify financial data was extracted
            financials_response = client.get(
                f"/api/v1/companies/{sample_company.company_id}/financials"
            )
            assert financials_response.status_code == 200
            
            # Step 3: Generate model with new data
            model_response = client.post("/api/v1/models/generate", json={
                "company_id": sample_company.company_id,
                "model_type": "DCF"
            })
            
            assert model_response.status_code in [200, 201]
    
    def test_batch_processing_workflow(
        self, 
        client: TestClient,
        multiple_companies: list
    ):
        """Test batch processing multiple companies."""
        results = []
        
        for company in multiple_companies[:3]:  # Test first 3 companies
            # Generate DCF model for each
            response = client.post("/api/v1/models/generate", json={
                "company_id": company.company_id,
                "model_type": "DCF"
            })
            
            results.append(response.status_code)
        
        # All requests should succeed
        assert all(status in [200, 201, 202] for status in results)
    
    def test_model_refresh_after_data_update(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_financials: list
    ):
        """Test regenerating model after data update."""
        # Step 1: Generate initial model
        initial_response = client.post("/api/v1/models/generate", json={
            "company_id": sample_company.company_id,
            "model_type": "DCF"
        })
        
        if initial_response.status_code in [200, 201]:
            # Step 2: Update financial data
            update_payload = {
                "company_id": sample_company.company_id,
                "period_end_date": "2024-12-31",
                "period_type": "Annual",
                "period_name": "Updated FY 2024",
                "revenue": 90000000.00,  # Updated value
                "ebitda": 18000000.00,
                "net_income": 13500000.00
            }
            
            update_response = client.post(
                f"/api/v1/companies/{sample_company.company_id}/financials",
                json=update_payload
            )
            assert update_response.status_code == 201
            
            # Step 3: Regenerate model with updated data
            regenerate_response = client.post("/api/v1/models/generate", json={
                "company_id": sample_company.company_id,
                "model_type": "DCF"
            })
            
            assert regenerate_response.status_code in [200, 201]
