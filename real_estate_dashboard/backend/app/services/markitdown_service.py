"""
MarkItDown Document Conversion Service

This service handles document conversion to markdown using Microsoft's MarkItDown library.
Includes comprehensive error handling, fallback mechanisms, and database storage.

Supported formats:
- PDF documents
- Office files (Word, Excel, PowerPoint)
- Images (JPG, PNG, GIF, BMP)
- HTML pages
- Audio files (with transcription)
- URLs and web pages
- And many more...
"""

import os
import io
import hashlib
import logging
from typing import Optional, Dict, Any, BinaryIO, Tuple
from datetime import datetime
from pathlib import Path
import time

from sqlalchemy.orm import Session
from fastapi import UploadFile
try:
    import magic  # python-magic for MIME type detection
except ImportError:
    magic = None
    logger.warning("python-magic not available, MIME type detection will be limited")

from app.models.markitdown_documents import (
    MarkItDownDocument,
    MarkItDownContent,
    MarkItDownFileType,
    ConversionStatus,
    ConversionMethod,
    MarkItDownVersion
)

# Configure logger
logger = logging.getLogger(__name__)


class MarkItDownService:
    """
    Service for converting various document formats to markdown using MarkItDown.

    Features:
    - Multi-format support (PDF, Office, images, HTML, audio, etc.)
    - Automatic file type detection using magika
    - Optional LLM enhancement for image descriptions
    - Comprehensive error handling and fallbacks
    - Database storage with versioning
    - Confidence scoring and quality metrics
    """

    def __init__(self, db: Session, storage_path: str = "/tmp/markitdown_uploads"):
        """
        Initialize MarkItDown service.

        Args:
            db: Database session
            storage_path: Path for temporary file storage
        """
        self.db = db
        self.storage_path = storage_path

        # Ensure storage directory exists
        os.makedirs(storage_path, exist_ok=True)

        # Initialize MarkItDown converter (lazy loading)
        self._converter = None
        self._converter_with_llm = None

    def _get_converter(self, use_llm: bool = False):
        """
        Lazy load MarkItDown converter.

        Args:
            use_llm: Whether to enable LLM enhancement for images

        Returns:
            MarkItDown converter instance
        """
        try:
            from markitdown import MarkItDown

            if use_llm:
                if self._converter_with_llm is None:
                    # Check for OpenAI API key
                    openai_key = os.getenv("OPENAI_API_KEY")
                    if not openai_key:
                        logger.warning("OPENAI_API_KEY not found, falling back to basic conversion")
                        return self._get_converter(use_llm=False)

                    try:
                        from openai import OpenAI
                        client = OpenAI(api_key=openai_key)
                        self._converter_with_llm = MarkItDown(llm_client=client, llm_model="gpt-4o")
                        logger.info("MarkItDown initialized with GPT-4o for image descriptions")
                    except Exception as e:
                        logger.warning(f"Failed to initialize LLM client: {e}, using basic converter")
                        return self._get_converter(use_llm=False)

                return self._converter_with_llm
            else:
                if self._converter is None:
                    self._converter = MarkItDown()
                    logger.info("MarkItDown initialized (basic mode)")
                return self._converter

        except ImportError as e:
            logger.error(f"MarkItDown library not installed: {e}")
            raise RuntimeError("MarkItDown library is not available. Please install with: pip install 'markitdown[all]'")

    def _detect_file_type(self, file_content: bytes, filename: str) -> Tuple[MarkItDownFileType, str]:
        """
        Detect file type using multiple methods.

        Args:
            file_content: File content as bytes
            filename: Original filename

        Returns:
            Tuple of (MarkItDownFileType, mime_type)
        """
        mime_type = "application/octet-stream"

        # Try magika for accurate detection
        try:
            from magika import Magika
            magika = Magika()
            result = magika.identify_bytes(file_content)
            mime_type = result.output.mime_type if result.output.mime_type else mime_type
            logger.info(f"Magika detected: {mime_type}")
        except Exception as e:
            logger.warning(f"Magika detection failed: {e}, falling back to extension-based detection")

        # Fallback: use file extension
        ext = Path(filename).suffix.lower()

        # Map MIME types and extensions to MarkItDownFileType
        if mime_type.startswith("application/pdf") or ext == ".pdf":
            return MarkItDownFileType.PDF, mime_type
        elif mime_type.startswith("application/vnd.openxmlformats-officedocument.wordprocessingml") or ext in [".docx", ".doc"]:
            return MarkItDownFileType.WORD, mime_type
        elif mime_type.startswith("application/vnd.openxmlformats-officedocument.spreadsheetml") or ext in [".xlsx", ".xls"]:
            return MarkItDownFileType.EXCEL, mime_type
        elif mime_type.startswith("application/vnd.openxmlformats-officedocument.presentationml") or ext in [".pptx", ".ppt"]:
            return MarkItDownFileType.POWERPOINT, mime_type
        elif mime_type.startswith("image/") or ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]:
            return MarkItDownFileType.IMAGE, mime_type
        elif mime_type.startswith("text/html") or ext in [".html", ".htm"]:
            return MarkItDownFileType.HTML, mime_type
        elif mime_type.startswith("audio/") or ext in [".mp3", ".wav", ".m4a", ".ogg"]:
            return MarkItDownFileType.AUDIO, mime_type
        elif mime_type.startswith("video/") or ext in [".mp4", ".avi", ".mov"]:
            return MarkItDownFileType.VIDEO, mime_type
        elif mime_type == "application/zip" or ext == ".zip":
            return MarkItDownFileType.ZIP, mime_type
        elif mime_type == "text/csv" or ext == ".csv":
            return MarkItDownFileType.CSV, mime_type
        elif mime_type.startswith("application/xml") or ext == ".xml":
            return MarkItDownFileType.XML, mime_type
        elif mime_type == "application/json" or ext == ".json":
            return MarkItDownFileType.JSON_FILE, mime_type
        elif ext == ".ipynb":
            return MarkItDownFileType.IPYNB, mime_type
        elif mime_type.startswith("text/") or ext == ".txt":
            return MarkItDownFileType.TEXT, mime_type
        else:
            return MarkItDownFileType.OTHER, mime_type

    def _calculate_file_hash(self, file_content: bytes) -> str:
        """Calculate SHA-256 hash of file content."""
        return hashlib.sha256(file_content).hexdigest()

    def _convert_with_markitdown(
        self,
        file_content: bytes,
        filename: str,
        use_llm: bool = False
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Convert document to markdown using MarkItDown.

        Args:
            file_content: File content as bytes
            filename: Original filename
            use_llm: Whether to use LLM for image descriptions

        Returns:
            Tuple of (markdown_text, metadata)
        """
        converter = self._get_converter(use_llm=use_llm)

        # Convert bytes to file-like object (MarkItDown requires binary stream)
        file_stream = io.BytesIO(file_content)
        file_stream.name = filename  # Set filename for extension detection

        # Perform conversion
        result = converter.convert_stream(file_stream, file_extension=Path(filename).suffix)

        # Extract metadata
        metadata = {
            "title": result.title if hasattr(result, 'title') else None,
            "conversion_successful": True
        }

        return result.text_content, metadata

    def _fallback_text_extraction(self, file_content: bytes, file_type: MarkItDownFileType) -> str:
        """
        Fallback text extraction when MarkItDown fails.

        Args:
            file_content: File content as bytes
            file_type: Detected file type

        Returns:
            Extracted text
        """
        logger.warning(f"Using fallback extraction for {file_type}")

        # Basic text extraction for common formats
        try:
            if file_type == MarkItDownFileType.TEXT:
                return file_content.decode('utf-8', errors='ignore')
            elif file_type == MarkItDownFileType.PDF:
                # Try pdfminer as fallback
                try:
                    from pdfminer.high_level import extract_text as pdf_extract_text
                    from io import BytesIO
                    text = pdf_extract_text(BytesIO(file_content))
                    return f"# PDF Content (Fallback Extraction)\n\n{text}"
                except Exception as e:
                    logger.error(f"PDF fallback failed: {e}")
                    return f"# PDF Content\n\n*Failed to extract text: {str(e)}*"
            else:
                return f"# {file_type.value}\n\n*Fallback extraction not available for this file type*"
        except Exception as e:
            logger.error(f"Fallback extraction failed: {e}")
            return f"# Extraction Failed\n\n*Error: {str(e)}*"

    def _calculate_confidence_score(
        self,
        markdown_text: str,
        file_type: MarkItDownFileType,
        conversion_method: ConversionMethod,
        had_errors: bool
    ) -> float:
        """
        Calculate confidence score for conversion quality.

        Args:
            markdown_text: Converted markdown text
            file_type: File type
            conversion_method: Method used
            had_errors: Whether errors occurred

        Returns:
            Confidence score (0.0 to 1.0)
        """
        score = 1.0

        # Penalize for errors
        if had_errors:
            score -= 0.3

        # Penalize for fallback methods
        if conversion_method == ConversionMethod.FALLBACK_TEXT:
            score -= 0.4

        # Penalize for short output (likely failed extraction)
        if len(markdown_text.strip()) < 100:
            score -= 0.3

        # Bonus for LLM enhancement
        if conversion_method == ConversionMethod.MARKITDOWN_WITH_LLM:
            score += 0.1

        # Bonus for structured content (tables, headings)
        if markdown_text.count('#') > 2:  # Has headings
            score += 0.05
        if markdown_text.count('|') > 10:  # Has tables
            score += 0.05

        return max(0.0, min(1.0, score))

    def _analyze_markdown_structure(self, markdown_text: str) -> Dict[str, int]:
        """
        Analyze markdown structure to extract metrics.

        Args:
            markdown_text: Markdown text to analyze

        Returns:
            Dictionary of structure metrics
        """
        return {
            "heading_count": markdown_text.count('\n#'),
            "table_count": markdown_text.count('\n|'),
            "image_count": markdown_text.count('!['),
            "link_count": markdown_text.count(']('),
            "code_block_count": markdown_text.count('```'),
            "character_count": len(markdown_text),
            "word_count": len(markdown_text.split())
        }

    async def convert_document(
        self,
        file: UploadFile,
        company_id: Optional[str] = None,
        use_llm: bool = False,
        user_id: Optional[str] = None
    ) -> MarkItDownDocument:
        """
        Convert an uploaded document to markdown and store in database.

        Args:
            file: Uploaded file
            company_id: Optional company ID for association
            use_llm: Whether to use LLM for image descriptions
            user_id: User performing the conversion

        Returns:
            MarkItDownDocument database record
        """
        start_time = time.time()

        # Read file content
        file_content = await file.read()
        file_size_kb = len(file_content) // 1024
        file_hash = self._calculate_file_hash(file_content)

        # Check for duplicate
        existing = self.db.query(MarkItDownDocument).filter(
            MarkItDownDocument.file_hash == file_hash
        ).first()

        if existing:
            logger.info(f"Duplicate file detected: {file_hash}")
            return existing

        # Detect file type
        file_type, mime_type = self._detect_file_type(file_content, file.filename)
        logger.info(f"Processing {file.filename} as {file_type.value} ({mime_type})")

        # Create document record
        document = MarkItDownDocument(
            document_name=file.filename,
            file_type=file_type,
            mime_type=mime_type,
            company_id=company_id,
            file_path=os.path.join(self.storage_path, file.filename),
            file_size_kb=file_size_kb,
            file_hash=file_hash,
            uploaded_by=user_id,
            conversion_status=ConversionStatus.PROCESSING,
            conversion_started=datetime.utcnow(),
            llm_enhanced=use_llm
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        # Attempt conversion
        markdown_text = ""
        conversion_method = ConversionMethod.MARKITDOWN
        had_errors = False
        error_message = None
        warnings = []

        try:
            # Primary: MarkItDown conversion
            logger.info(f"Converting with MarkItDown (LLM={use_llm})...")
            markdown_text, metadata = self._convert_with_markitdown(
                file_content,
                file.filename,
                use_llm=use_llm
            )

            conversion_method = (
                ConversionMethod.MARKITDOWN_WITH_LLM if use_llm
                else ConversionMethod.MARKITDOWN
            )

            # Store LLM model if used
            if use_llm:
                document.llm_model = "gpt-4o"

        except Exception as e:
            logger.error(f"MarkItDown conversion failed: {e}", exc_info=True)
            had_errors = True
            error_message = str(e)
            warnings.append(f"Primary conversion failed: {str(e)}")

            # Fallback: Basic text extraction
            try:
                logger.info("Attempting fallback extraction...")
                markdown_text = self._fallback_text_extraction(file_content, file_type)
                conversion_method = ConversionMethod.FALLBACK_TEXT
                warnings.append("Using fallback text extraction")
            except Exception as fallback_error:
                logger.error(f"Fallback extraction failed: {fallback_error}")
                markdown_text = f"# Conversion Failed\n\n**Error:** {str(e)}\n\n**Fallback Error:** {str(fallback_error)}"
                document.conversion_status = ConversionStatus.FAILED
                document.error_message = f"All conversion methods failed: {str(e)}"
                self.db.commit()
                return document

        # Calculate metrics
        conversion_duration_ms = int((time.time() - start_time) * 1000)
        structure_metrics = self._analyze_markdown_structure(markdown_text)
        confidence = self._calculate_confidence_score(
            markdown_text,
            file_type,
            conversion_method,
            had_errors
        )

        # Update document record
        document.conversion_status = (
            ConversionStatus.PARTIAL if warnings else ConversionStatus.COMPLETED
        )
        document.conversion_method = conversion_method
        document.conversion_completed = datetime.utcnow()
        document.conversion_duration_ms = conversion_duration_ms
        document.conversion_confidence = confidence
        document.character_count = structure_metrics["character_count"]
        document.word_count = structure_metrics["word_count"]
        document.has_errors = had_errors
        document.error_message = error_message
        document.warnings = warnings if warnings else None
        document.needs_review = confidence < 0.7

        # Create content record
        content = MarkItDownContent(
            document_id=document.id,
            markdown_text=markdown_text,
            heading_count=structure_metrics["heading_count"],
            table_count=structure_metrics["table_count"],
            image_count=structure_metrics["image_count"],
            link_count=structure_metrics["link_count"],
            code_block_count=structure_metrics["code_block_count"]
        )

        self.db.add(content)
        self.db.commit()
        self.db.refresh(document)

        logger.info(
            f"Conversion completed: {file.filename} -> {structure_metrics['word_count']} words, "
            f"confidence={confidence:.2f}, duration={conversion_duration_ms}ms"
        )

        return document

    def get_document(self, document_id: str) -> Optional[MarkItDownDocument]:
        """Get document by ID."""
        return self.db.query(MarkItDownDocument).filter(
            MarkItDownDocument.id == document_id
        ).first()

    def get_document_content(self, document_id: str) -> Optional[str]:
        """Get markdown content for a document."""
        content = self.db.query(MarkItDownContent).filter(
            MarkItDownContent.document_id == document_id
        ).first()

        return content.markdown_text if content else None

    def list_documents(
        self,
        company_id: Optional[str] = None,
        file_type: Optional[MarkItDownFileType] = None,
        limit: int = 100
    ):
        """
        List documents with optional filtering.

        Args:
            company_id: Filter by company
            file_type: Filter by file type
            limit: Maximum number of results

        Returns:
            List of MarkItDownDocument records
        """
        query = self.db.query(MarkItDownDocument)

        if company_id:
            query = query.filter(MarkItDownDocument.company_id == company_id)
        if file_type:
            query = query.filter(MarkItDownDocument.file_type == file_type)

        return query.order_by(MarkItDownDocument.upload_date.desc()).limit(limit).all()

    def mark_reviewed(
        self,
        document_id: str,
        user_id: str,
        review_notes: Optional[str] = None
    ) -> MarkItDownDocument:
        """
        Mark a document as reviewed.

        Args:
            document_id: Document ID
            user_id: Reviewer user ID
            review_notes: Optional review notes

        Returns:
            Updated document
        """
        document = self.get_document(document_id)
        if not document:
            raise ValueError(f"Document not found: {document_id}")

        document.needs_review = False
        document.reviewed_by = user_id
        document.reviewed_date = datetime.utcnow()
        document.review_notes = review_notes

        self.db.commit()
        self.db.refresh(document)

        return document
