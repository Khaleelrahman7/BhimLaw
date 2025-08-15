"""
BhimLaw AI - PDF Processing Module
Advanced PDF text extraction and analysis for legal case documents
"""

import logging
import io
import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

try:
    import PyPDF2
    import pdfplumber
    PDF_PROCESSING_AVAILABLE = True
except ImportError:
    PDF_PROCESSING_AVAILABLE = False
    PyPDF2 = None
    pdfplumber = None

# Configure logging
logger = logging.getLogger("BhimLaw_PDF_Processor")

class LegalPDFProcessor:
    """
    Advanced PDF processor for legal documents
    Extracts text, metadata, and structured information from legal case PDFs
    """
    
    def __init__(self):
        if not PDF_PROCESSING_AVAILABLE:
            logger.warning("PDF processing libraries not available. Install PyPDF2 and pdfplumber.")
            self.available = False
        else:
            self.available = True
            logger.info("Legal PDF Processor initialized successfully")
    
    def extract_text_from_pdf(self, pdf_content: Union[bytes, io.BytesIO]) -> Dict[str, Any]:
        """
        Extract text content from PDF using multiple methods for best results
        
        Args:
            pdf_content: PDF content as bytes or BytesIO object
            
        Returns:
            Dict containing extracted text and metadata
        """
        if not self.available:
            raise RuntimeError("PDF processing not available. Install required libraries.")
        
        try:
            # Convert bytes to BytesIO if needed
            if isinstance(pdf_content, bytes):
                pdf_stream = io.BytesIO(pdf_content)
            else:
                pdf_stream = pdf_content
            
            # Try pdfplumber first (better for complex layouts)
            text_content = self._extract_with_pdfplumber(pdf_stream)
            
            # If pdfplumber fails or returns minimal text, try PyPDF2
            if not text_content or len(text_content.strip()) < 100:
                pdf_stream.seek(0)
                text_content = self._extract_with_pypdf2(pdf_stream)
            
            # Extract metadata
            pdf_stream.seek(0)
            metadata = self._extract_metadata(pdf_stream)
            
            # Analyze document structure
            document_analysis = self._analyze_document_structure(text_content)
            
            return {
                "success": True,
                "text_content": text_content,
                "metadata": metadata,
                "document_analysis": document_analysis,
                "extraction_method": "pdfplumber" if len(text_content) > 100 else "pypdf2",
                "extracted_at": datetime.now().isoformat(),
                "character_count": len(text_content),
                "word_count": len(text_content.split()) if text_content else 0
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "text_content": "",
                "metadata": {},
                "document_analysis": {}
            }
    
    def _extract_with_pdfplumber(self, pdf_stream: io.BytesIO) -> str:
        """Extract text using pdfplumber (better for tables and complex layouts)"""
        try:
            text_parts = []
            with pdfplumber.open(pdf_stream) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            
            return "\n\n".join(text_parts)
            
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {str(e)}")
            return ""
    
    def _extract_with_pypdf2(self, pdf_stream: io.BytesIO) -> str:
        """Extract text using PyPDF2 (fallback method)"""
        try:
            text_parts = []
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            return "\n\n".join(text_parts)
            
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {str(e)}")
            return ""
    
    def _extract_metadata(self, pdf_stream: io.BytesIO) -> Dict[str, Any]:
        """Extract PDF metadata"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            metadata = {}
            
            if pdf_reader.metadata:
                metadata.update({
                    "title": pdf_reader.metadata.get("/Title", ""),
                    "author": pdf_reader.metadata.get("/Author", ""),
                    "subject": pdf_reader.metadata.get("/Subject", ""),
                    "creator": pdf_reader.metadata.get("/Creator", ""),
                    "producer": pdf_reader.metadata.get("/Producer", ""),
                    "creation_date": str(pdf_reader.metadata.get("/CreationDate", "")),
                    "modification_date": str(pdf_reader.metadata.get("/ModDate", ""))
                })
            
            metadata["page_count"] = len(pdf_reader.pages)
            return metadata
            
        except Exception as e:
            logger.warning(f"Metadata extraction failed: {str(e)}")
            return {"page_count": 0}
    
    def _analyze_document_structure(self, text_content: str) -> Dict[str, Any]:
        """Analyze document structure to identify legal document type and key sections"""
        if not text_content:
            return {}
        
        analysis = {
            "document_type": "unknown",
            "sections_found": [],
            "legal_indicators": [],
            "case_references": [],
            "court_mentions": [],
            "date_references": [],
            "party_names": []
        }
        
        # Identify document type based on content patterns
        text_lower = text_content.lower()
        
        if any(term in text_lower for term in ["judgment", "judgement", "court", "petitioner", "respondent"]):
            analysis["document_type"] = "court_judgment"
        elif any(term in text_lower for term in ["petition", "writ", "application"]):
            analysis["document_type"] = "court_petition"
        elif any(term in text_lower for term in ["contract", "agreement", "party", "whereas"]):
            analysis["document_type"] = "legal_contract"
        elif any(term in text_lower for term in ["act", "section", "rule", "regulation"]):
            analysis["document_type"] = "legal_statute"
        
        # Find legal sections
        section_patterns = [
            r"(?i)(background|facts|issues?|arguments?|findings?|conclusion|order|relief)",
            r"(?i)(section \d+|article \d+|rule \d+)",
            r"(?i)(whereas|therefore|ordered|directed)"
        ]
        
        for pattern in section_patterns:
            matches = re.findall(pattern, text_content)
            analysis["sections_found"].extend(matches)
        
        # Find case references
        case_patterns = [
            r"(?i)(\d{4}\s+\w+\s+\d+)",  # Year Citation Number
            r"(?i)(AIR\s+\d{4}\s+\w+\s+\d+)",  # AIR citations
            r"(?i)(\(\d{4}\)\s+\d+\s+\w+\s+\d+)"  # (Year) Volume Reporter Page
        ]
        
        for pattern in case_patterns:
            matches = re.findall(pattern, text_content)
            analysis["case_references"].extend(matches)
        
        # Find court mentions
        court_patterns = [
            r"(?i)(supreme court|high court|district court|sessions court|magistrate)",
            r"(?i)(hon'ble|honourable)\s+(court|judge)"
        ]
        
        for pattern in court_patterns:
            matches = re.findall(pattern, text_content)
            analysis["court_mentions"].extend(matches)
        
        # Find dates
        date_patterns = [
            r"\d{1,2}[/-]\d{1,2}[/-]\d{4}",
            r"\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}"
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text_content)
            analysis["date_references"].extend(matches)
        
        return analysis
    
    def analyze_legal_case_from_pdf(self, pdf_content: Union[bytes, io.BytesIO]) -> Dict[str, Any]:
        """
        Comprehensive analysis of legal case from PDF
        Combines text extraction with legal document analysis
        """
        # Extract text from PDF
        extraction_result = self.extract_text_from_pdf(pdf_content)
        
        if not extraction_result["success"]:
            return extraction_result
        
        text_content = extraction_result["text_content"]
        
        # Perform legal analysis on extracted text
        legal_analysis = {
            "case_summary": self._extract_case_summary(text_content),
            "legal_issues": self._extract_legal_issues(text_content),
            "parties_involved": self._extract_parties(text_content),
            "court_details": self._extract_court_details(text_content),
            "key_findings": self._extract_key_findings(text_content),
            "legal_precedents": self._extract_precedents(text_content),
            "applicable_laws": self._extract_applicable_laws(text_content)
        }
        
        # Combine extraction and analysis results
        result = extraction_result.copy()
        result["legal_analysis"] = legal_analysis
        result["analysis_type"] = "comprehensive_case_analysis"
        
        return result
    
    def _extract_case_summary(self, text: str) -> str:
        """Extract case summary from text"""
        # Look for summary sections
        summary_patterns = [
            r"(?i)summary:?\s*(.{100,500})",
            r"(?i)brief:?\s*(.{100,500})",
            r"(?i)facts:?\s*(.{100,500})"
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # If no specific summary found, return first few sentences
        sentences = text.split('.')[:5]
        return '. '.join(sentences) + '.' if sentences else ""
    
    def _extract_legal_issues(self, text: str) -> List[str]:
        """Extract legal issues from text"""
        issues = []
        
        # Look for issues sections
        issue_patterns = [
            r"(?i)issues?:?\s*(.+?)(?=\n\n|\n[A-Z]|$)",
            r"(?i)questions?:?\s*(.+?)(?=\n\n|\n[A-Z]|$)",
            r"(?i)points? for determination:?\s*(.+?)(?=\n\n|\n[A-Z]|$)"
        ]
        
        for pattern in issue_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                # Split by numbers or bullet points
                issue_items = re.split(r'\d+\.|•|\n-', match)
                issues.extend([item.strip() for item in issue_items if item.strip()])
        
        return issues[:10]  # Limit to 10 issues
    
    def _extract_parties(self, text: str) -> Dict[str, List[str]]:
        """Extract parties involved in the case"""
        parties = {"petitioners": [], "respondents": [], "appellants": [], "defendants": []}
        
        # Look for party mentions
        party_patterns = {
            "petitioners": r"(?i)petitioner[s]?:?\s*(.+?)(?=\n|respondent|vs?\.)",
            "respondents": r"(?i)respondent[s]?:?\s*(.+?)(?=\n|petitioner|vs?\.)",
            "appellants": r"(?i)appellant[s]?:?\s*(.+?)(?=\n|respondent|vs?\.)",
            "defendants": r"(?i)defendant[s]?:?\s*(.+?)(?=\n|plaintiff|vs?\.)"
        }
        
        for party_type, pattern in party_patterns.items():
            matches = re.findall(pattern, text)
            parties[party_type] = [match.strip() for match in matches]
        
        return parties
    
    def _extract_court_details(self, text: str) -> Dict[str, str]:
        """Extract court details"""
        court_info = {}
        
        # Look for court name
        court_pattern = r"(?i)(supreme court|high court|district court|sessions court|magistrate court)[^.]*"
        court_match = re.search(court_pattern, text)
        if court_match:
            court_info["court_name"] = court_match.group(0)
        
        # Look for judge name
        judge_pattern = r"(?i)(hon'ble|honourable)\s+(justice|judge)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
        judge_match = re.search(judge_pattern, text)
        if judge_match:
            court_info["judge_name"] = judge_match.group(3)
        
        return court_info
    
    def _extract_key_findings(self, text: str) -> List[str]:
        """Extract key findings from the case"""
        findings = []
        
        finding_patterns = [
            r"(?i)findings?:?\s*(.+?)(?=\n\n|\n[A-Z]|conclusion|order)",
            r"(?i)held:?\s*(.+?)(?=\n\n|\n[A-Z]|conclusion|order)",
            r"(?i)decision:?\s*(.+?)(?=\n\n|\n[A-Z]|conclusion|order)"
        ]
        
        for pattern in finding_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                # Split into individual findings
                finding_items = re.split(r'\d+\.|•|\n-', match)
                findings.extend([item.strip() for item in finding_items if item.strip()])
        
        return findings[:10]  # Limit to 10 findings
    
    def _extract_precedents(self, text: str) -> List[str]:
        """Extract legal precedents cited"""
        precedents = []
        
        # Look for case citations
        citation_patterns = [
            r"(?i)(AIR\s+\d{4}\s+\w+\s+\d+)",
            r"(?i)(\d{4}\s+\w+\s+\d+)",
            r"(?i)(\(\d{4}\)\s+\d+\s+\w+\s+\d+)"
        ]
        
        for pattern in citation_patterns:
            matches = re.findall(pattern, text)
            precedents.extend(matches)
        
        return list(set(precedents))  # Remove duplicates
    
    def _extract_applicable_laws(self, text: str) -> List[str]:
        """Extract applicable laws and sections"""
        laws = []
        
        law_patterns = [
            r"(?i)(section\s+\d+[a-z]?\s+of\s+[^.]+act[^.]*)",
            r"(?i)(article\s+\d+[a-z]?\s+of\s+[^.]+)",
            r"(?i)([^.]*act[^.]*\d{4}[^.]*)",
            r"(?i)(rule\s+\d+[a-z]?\s+of\s+[^.]+)"
        ]
        
        for pattern in law_patterns:
            matches = re.findall(pattern, text)
            laws.extend([match.strip() for match in matches])
        
        return list(set(laws))  # Remove duplicates

# Global PDF processor instance
pdf_processor = LegalPDFProcessor()
