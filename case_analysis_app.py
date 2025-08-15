"""
BhimLaw AI: Focused Case Analysis System
Streamlined legal case analysis with PDF processing capabilities
"""

import logging
import uuid
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum
from io import BytesIO

# FastAPI and related imports
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# AI libraries
try:
    from openai import OpenAI
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# PDF processing
try:
    from pdf_processor import pdf_processor
    PDF_PROCESSING_AVAILABLE = True
except ImportError:
    PDF_PROCESSING_AVAILABLE = False

# PDF generation
try:
    from pdf_generator import pdf_generator
    PDF_GENERATION_AVAILABLE = True
except ImportError:
    PDF_GENERATION_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title="BhimLaw AI - Case Analysis System",
    description="Focused legal case analysis with PDF processing capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BhimLaw_CaseAnalysis")

# AI Configuration
AI_API_KEY = os.getenv("NVIDIA_API_KEY", "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")
AI_BASE_URL = "https://integrate.api.nvidia.com/v1"
AI_MODEL = "nvidia/llama-3.1-nemotron-ultra-253b-v1"

# Enums
class JurisdictionType(str, Enum):
    INDIA = "India"
    SUPREME_COURT = "Supreme Court of India"
    HIGH_COURT = "High Court"
    DISTRICT_COURT = "District Court"

class ComplexityLevel(str, Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    HIGHLY_COMPLEX = "highly_complex"

class UrgencyLevel(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

# Request Models
class CaseAnalysisRequest(BaseModel):
    query: str = Field(..., description="Legal case details or question", min_length=10)
    jurisdiction: JurisdictionType = Field(default=JurisdictionType.INDIA)
    complexity_level: ComplexityLevel = Field(default=ComplexityLevel.MODERATE)
    urgency_level: UrgencyLevel = Field(default=UrgencyLevel.NORMAL)
    case_type: Optional[str] = Field(default=None, description="Type of case")
    session_id: Optional[str] = Field(default=None)

class PDFCaseAnalysisResponse(BaseModel):
    success: bool
    case_analysis: Dict[str, Any] = Field(default_factory=dict)
    pdf_extraction: Dict[str, Any] = Field(default_factory=dict)
    structured_analysis: Dict[str, Any] = Field(default_factory=dict)
    message: str
    processing_time: float
    session_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

# Global state
case_sessions = {}

# AI Client
ai_client = None

def get_ai_client():
    global ai_client
    if ai_client is None and AI_AVAILABLE:
        try:
            ai_client = OpenAI(
                base_url=AI_BASE_URL,
                api_key=AI_API_KEY
            )
            logger.info("AI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI client: {e}")
            ai_client = None
    return ai_client

class CaseAnalysisEngine:
    """Focused case analysis engine"""
    
    def __init__(self):
        self.ai_client = None
        logger.info("Case Analysis Engine initialized")
    
    def create_session(self) -> str:
        """Create new analysis session"""
        session_id = str(uuid.uuid4())
        case_sessions[session_id] = {
            "created_at": datetime.now().isoformat(),
            "analyses": [],
            "status": "active"
        }
        return session_id
    
    def analyze_case(self, query: str, jurisdiction: JurisdictionType, 
                    complexity: ComplexityLevel, urgency: UrgencyLevel,
                    case_type: str = None) -> Dict[str, Any]:
        """Analyze legal case using AI"""
        try:
            client = get_ai_client()
            if not client:
                return self.generate_fallback_analysis()
            
            prompt = self.create_analysis_prompt(query, jurisdiction, complexity, urgency, case_type)
            
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4000
            )
            
            analysis_text = response.choices[0].message.content
            structured_data = self.extract_structured_data(analysis_text)
            
            return {
                "analysis": analysis_text,
                "legal_issues": structured_data.get("legal_issues", []),
                "applicable_laws": structured_data.get("applicable_laws", []),
                "precedents": structured_data.get("precedents", []),
                "recommendations": structured_data.get("recommendations", []),
                "risk_factors": structured_data.get("risk_factors", []),
                "next_steps": structured_data.get("next_steps", []),
                "confidence_score": 0.85
            }
            
        except Exception as e:
            logger.error(f"Error in case analysis: {e}")
            return self.generate_fallback_analysis()
    
    def get_system_prompt(self) -> str:
        """Get system prompt for case analysis"""
        return """You are BhimLaw AI, an expert legal case analysis system.

EXPERTISE:
- Constitutional Law, Criminal Law, Civil Law, Corporate Law
- Family Law, Labor Law, Tax Law, Environmental Law
- Case strategy and legal reasoning

ANALYSIS STRUCTURE:
Provide comprehensive analysis with:

1. LEGAL CLASSIFICATION
   - Case type and legal domain
   - Applicable jurisdiction and court level
   - Constitutional/statutory framework

2. APPLICABLE LAWS & PROVISIONS
   - Relevant acts and sections
   - Constitutional articles
   - Rules and regulations

3. LANDMARK JUDGMENTS
   - Supreme Court precedents
   - High Court decisions
   - Relevant case law

4. LEGAL REMEDY PATH
   - Step-by-step legal process
   - Filing requirements
   - Procedural timeline

5. ADDITIONAL INSIGHTS
   - Success probability
   - Estimated costs and timeline
   - Alternative approaches

6. PROFESSIONAL ADVICE
   - Immediate actions required
   - Evidence collection
   - Risk mitigation

Format responses professionally without markdown symbols."""
    
    def create_analysis_prompt(self, query: str, jurisdiction: JurisdictionType,
                             complexity: ComplexityLevel, urgency: UrgencyLevel,
                             case_type: str = None) -> str:
        """Create analysis prompt"""
        return f"""
CASE ANALYSIS REQUEST

Query: {query}
Jurisdiction: {jurisdiction.value}
Complexity: {complexity.value}
Urgency: {urgency.value}
Case Type: {case_type or 'General'}

Please provide comprehensive legal case analysis following the structured format.
Focus on practical, actionable legal guidance with proper citations and precedents.
"""
    
    def extract_structured_data(self, analysis_text: str) -> Dict[str, Any]:
        """Extract structured data from analysis"""
        data = {
            "legal_issues": [],
            "applicable_laws": [],
            "precedents": [],
            "recommendations": [],
            "risk_factors": [],
            "next_steps": []
        }
        
        lines = analysis_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Identify sections
            if any(keyword in line.lower() for keyword in ['legal issue', 'issues']):
                current_section = 'legal_issues'
            elif any(keyword in line.lower() for keyword in ['applicable law', 'laws', 'provisions']):
                current_section = 'applicable_laws'
            elif any(keyword in line.lower() for keyword in ['precedent', 'judgment', 'case law']):
                current_section = 'precedents'
            elif any(keyword in line.lower() for keyword in ['recommendation', 'advice']):
                current_section = 'recommendations'
            elif any(keyword in line.lower() for keyword in ['risk', 'challenge']):
                current_section = 'risk_factors'
            elif any(keyword in line.lower() for keyword in ['next step', 'action']):
                current_section = 'next_steps'
            
            # Extract content
            if line.startswith(('- ', '• ', '* ')) or line.startswith(tuple('123456789')):
                content = line.lstrip('- •*0123456789. ').strip()
                if current_section and content:
                    data[current_section].append(content)
        
        return data
    
    def generate_fallback_analysis(self) -> Dict[str, Any]:
        """Generate fallback analysis when AI unavailable"""
        return {
            "analysis": """
BHIMLAW AI - CASE ANALYSIS FRAMEWORK

LEGAL CLASSIFICATION
This case requires comprehensive legal analysis using established legal principles and precedents.

APPLICABLE LAWS & PROVISIONS
- Constitutional provisions as applicable
- Relevant statutory framework
- Procedural laws and rules

LANDMARK JUDGMENTS
- Supreme Court precedents
- High Court decisions
- Binding authorities

LEGAL REMEDY PATH
1. Detailed case preparation
2. Evidence collection and documentation
3. Legal research and precedent analysis
4. Strategic planning and filing

ADDITIONAL INSIGHTS
- Professional legal consultation recommended
- Comprehensive case preparation required
- Evidence documentation essential

PROFESSIONAL ADVICE
- Engage qualified legal counsel
- Systematic case preparation
- Thorough legal research
- Strategic approach development
""",
            "legal_issues": ["Comprehensive legal analysis required"],
            "applicable_laws": ["Constitutional and statutory provisions"],
            "precedents": ["Supreme Court and High Court precedents"],
            "recommendations": ["Professional legal consultation", "Comprehensive case preparation"],
            "risk_factors": ["Complex legal issues", "Procedural requirements"],
            "next_steps": ["Legal consultation", "Case preparation", "Evidence collection"],
            "confidence_score": 0.70
        }

# Initialize engine
case_engine = CaseAnalysisEngine()

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    """Serve the frontend"""
    try:
        with open("bhimlaw_frontend.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>BhimLaw AI - Case Analysis System</h1><p>Frontend not found</p>")

@app.post("/api/case-analysis")
async def analyze_case(request: CaseAnalysisRequest):
    """Analyze legal case"""
    try:
        start_time = datetime.now()
        
        # Create session if needed
        session_id = request.session_id or case_engine.create_session()
        
        # Perform analysis
        result = case_engine.analyze_case(
            request.query,
            request.jurisdiction,
            request.complexity_level,
            request.urgency_level,
            request.case_type
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "success": True,
            "data": result,
            "session_id": session_id,
            "message": "Case analysis completed successfully",
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in case analysis: {e}")
        return {
            "success": False,
            "data": case_engine.generate_fallback_analysis(),
            "session_id": request.session_id,
            "message": f"Analysis error: {str(e)}",
            "processing_time": 0.0,
            "timestamp": datetime.now().isoformat()
        }

@app.post("/api/pdf-case-analysis", response_model=PDFCaseAnalysisResponse)
async def analyze_pdf_case(
    file: UploadFile = File(..., description="PDF file containing legal case"),
    legal_query: str = Form(..., description="Legal query about the case"),
    analysis_type: str = Form(default="comprehensive", description="Type of analysis"),
    jurisdiction: str = Form(default="India", description="Legal jurisdiction"),
    complexity_level: str = Form(default="moderate", description="Case complexity level"),
    urgency_level: str = Form(default="normal", description="Case urgency level"),
    session_id: Optional[str] = Form(default=None)
):
    """Analyze legal case from uploaded PDF"""
    try:
        start_time = datetime.now()

        # Check PDF processing availability
        if not PDF_PROCESSING_AVAILABLE:
            return PDFCaseAnalysisResponse(
                success=False,
                message="PDF processing not available. Please install required libraries.",
                processing_time=0.0,
                session_id=session_id
            )

        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            return PDFCaseAnalysisResponse(
                success=False,
                message="Only PDF files are supported.",
                processing_time=0.0,
                session_id=session_id
            )

        # Read PDF content
        pdf_content = await file.read()

        if len(pdf_content) == 0:
            return PDFCaseAnalysisResponse(
                success=False,
                message="Empty PDF file provided.",
                processing_time=0.0,
                session_id=session_id
            )

        # Create session if needed
        if not session_id:
            session_id = case_engine.create_session()

        # Extract text from PDF
        pdf_analysis = pdf_processor.analyze_legal_case_from_pdf(pdf_content)

        if not pdf_analysis["success"]:
            return PDFCaseAnalysisResponse(
                success=False,
                pdf_extraction=pdf_analysis,
                message=f"Failed to extract text from PDF: {pdf_analysis.get('error', 'Unknown error')}",
                processing_time=(datetime.now() - start_time).total_seconds(),
                session_id=session_id
            )

        # Get extracted text
        extracted_text = pdf_analysis["text_content"]

        if len(extracted_text.strip()) < 50:
            return PDFCaseAnalysisResponse(
                success=False,
                pdf_extraction=pdf_analysis,
                message="Insufficient text extracted from PDF.",
                processing_time=(datetime.now() - start_time).total_seconds(),
                session_id=session_id
            )

        # Combine query with extracted text
        combined_query = f"""
        Legal Query: {legal_query}

        Case Document Content:
        {extracted_text[:4000]}

        Please analyze this case document and provide comprehensive legal analysis addressing the specific query.
        """

        # Convert string parameters to enums
        try:
            jurisdiction_enum = JurisdictionType(jurisdiction)
        except ValueError:
            jurisdiction_enum = JurisdictionType.INDIA

        try:
            complexity_enum = ComplexityLevel(complexity_level)
        except ValueError:
            complexity_enum = ComplexityLevel.MODERATE

        try:
            urgency_enum = UrgencyLevel(urgency_level)
        except ValueError:
            urgency_enum = UrgencyLevel.NORMAL

        # Perform case analysis
        case_analysis_result = case_engine.analyze_case(
            combined_query,
            jurisdiction_enum,
            complexity_enum,
            urgency_enum,
            "pdf_case_analysis"
        )

        # Create structured analysis
        structured_analysis = {
            "case_summary": pdf_analysis.get("legal_analysis", {}).get("case_summary", ""),
            "legal_issues": pdf_analysis.get("legal_analysis", {}).get("legal_issues", []),
            "parties_involved": pdf_analysis.get("legal_analysis", {}).get("parties_involved", {}),
            "court_details": pdf_analysis.get("legal_analysis", {}).get("court_details", {}),
            "key_findings": pdf_analysis.get("legal_analysis", {}).get("key_findings", []),
            "legal_precedents": pdf_analysis.get("legal_analysis", {}).get("legal_precedents", []),
            "applicable_laws": pdf_analysis.get("legal_analysis", {}).get("applicable_laws", []),
            "ai_analysis": case_analysis_result.get("analysis", ""),
            "recommendations": case_analysis_result.get("recommendations", []),
            "risk_assessment": case_analysis_result.get("risk_factors", []),
            "next_steps": case_analysis_result.get("next_steps", [])
        }

        processing_time = (datetime.now() - start_time).total_seconds()

        return PDFCaseAnalysisResponse(
            success=True,
            case_analysis=case_analysis_result,
            pdf_extraction=pdf_analysis,
            structured_analysis=structured_analysis,
            message=f"Successfully analyzed case from {file.filename}",
            processing_time=processing_time,
            session_id=session_id
        )

    except Exception as e:
        logger.error(f"Error in PDF case analysis: {e}")
        return PDFCaseAnalysisResponse(
            success=False,
            message=f"Error analyzing PDF case: {str(e)}",
            processing_time=(datetime.now() - start_time).total_seconds() if 'start_time' in locals() else 0.0,
            session_id=session_id
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
