"""
BhimLaw AI - Specialized Legal Agents
Prototype VII - Municipal and Administrative Law Specialists

This module contains specialized AI agents for handling specific types of legal cases
with deep domain expertise and tailored legal knowledge bases.
"""

import logging
import uuid
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum
from abc import ABC, abstractmethod

# AI libraries
try:
    import requests
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Configure logging
logger = logging.getLogger("BhimLaw_Specialized_Agents")

# Legal Acts Database Integration - Disabled for API compatibility
LEGAL_DB_AVAILABLE = False

# NVIDIA API Configuration
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "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")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL = "nvidia/llama-3.1-nemotron-ultra-253b-v1"

class CaseCategory(str, Enum):
    """Categories of specialized legal cases"""
    PROPERTY_VIOLATIONS = "property_violations"
    ENVIRONMENTAL_HEALTH = "environmental_health"
    EMPLOYEE_SERVICES = "employee_services"
    RTI_TRANSPARENCY = "rti_transparency"
    INFRASTRUCTURE_WORKS = "infrastructure_works"
    ENCROACHMENT_LAND = "encroachment_land"
    LICENSING_TRADE = "licensing_trade"
    SLUM_CLEARANCE = "slum_clearance"
    WATER_DRAINAGE = "water_drainage"
    PUBLIC_NUISANCE = "public_nuisance"

class SpecializedAgentType(str, Enum):
    """Specialized agent types for specific case categories"""
    PROPERTY_BUILDING_VIOLATIONS = "property_building_violations"
    ENVIRONMENTAL_PUBLIC_HEALTH = "environmental_public_health"
    EMPLOYEE_SERVICE_MATTERS = "employee_service_matters"
    RTI_TRANSPARENCY = "rti_transparency"
    INFRASTRUCTURE_PUBLIC_WORKS = "infrastructure_public_works"
    ENCROACHMENT_LAND = "encroachment_land"
    LICENSING_TRADE_REGULATION = "licensing_trade_regulation"
    SLUM_CLEARANCE_RESETTLEMENT = "slum_clearance_resettlement"
    WATER_DRAINAGE = "water_drainage"
    PUBLIC_NUISANCE = "public_nuisance"

class SpecializedLegalAgent(ABC):
    """
    Abstract base class for all specialized legal agents
    Provides common functionality and enforces consistent interface
    """
    
    def __init__(self, agent_name: str, specialization: str):
        self.agent_name = agent_name
        self.specialization = specialization
        self.agent_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.case_count = 0
        self.success_rate = 0.0
        self.knowledge_base = self._initialize_knowledge_base()
        self.legal_procedures = self._initialize_procedures()
        # Use hardcoded acts for API compatibility
        self.relevant_acts = self._initialize_relevant_acts()
        self.common_penalties = self._initialize_penalties()
        self.precedent_cases = self._initialize_precedents()
        self.ai_client = None

        logger.info(f"Initialized {agent_name} - {specialization}")
    
    @abstractmethod
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize agent-specific knowledge base"""
        pass
    
    @abstractmethod
    def _initialize_procedures(self) -> Dict[str, List[str]]:
        """Initialize legal procedures specific to this agent"""
        pass
    
    @abstractmethod
    def _initialize_relevant_acts(self) -> List[str]:
        """Initialize relevant acts and regulations"""
        pass
    
    @abstractmethod
    def _initialize_penalties(self) -> Dict[str, str]:
        """Initialize common penalties and their calculations"""
        pass
    
    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Initialize relevant precedent cases - now optional, AI model generates them dynamically"""
        return []  # Return empty list - precedents will come from AI model response
    
    @abstractmethod
    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze a specific case using agent's specialized knowledge"""
        pass
    
    def is_query_in_domain(self, case_details: str, case_type: str) -> bool:
        """Check if the query falls within this agent's domain expertise"""
        query_lower = (case_details + " " + case_type).lower()
        
        # Check if any domain keywords match
        domain_keywords = self.get_domain_keywords()
        matches = sum(1 for keyword in domain_keywords if keyword in query_lower)

        # For property-related queries, be more lenient with matching
        # If at least 1 keyword matches, consider it within domain
        return matches >= 1
    
    @abstractmethod
    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to this agent's domain"""
        pass
    
    def get_redirect_response(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Generate a redirect response when query is outside domain"""
        from agent_router import get_agent_router
        
        # Get the router to find the best agent
        router = get_agent_router()
        category, best_agent, confidence = router.select_best_agent(case_details, case_type)
        
        redirect_message = f"""I am the {self.agent_name}, specialized in {self.specialization}.

Your query appears to be outside my area of expertise. Based on your question about "{case_details[:100]}...", 
I recommend consulting with the {best_agent.agent_name} who specializes in {best_agent.specialization}.

The {best_agent.agent_name} will be better equipped to provide you with accurate and specialized legal guidance 
for your {case_type} matter.

Would you like me to redirect your query to the {best_agent.agent_name}?"""
        
        return {
            "redirect_required": True,
            "current_agent": self.agent_name,
            "recommended_agent": best_agent.agent_name,
            "recommended_specialization": best_agent.specialization,
            "confidence_score": confidence,
            "message": redirect_message,
            "timestamp": datetime.now().isoformat()
        }

    # Database methods removed for API compatibility - using hardcoded data only
    
    def get_system_prompt(self) -> str:
        """Get specialized system prompt for this agent"""
        return f"""You are {self.agent_name}, a specialized legal AI agent with deep expertise in {self.specialization}.

SPECIALIZATION: {self.specialization}

CORE EXPERTISE:
- Comprehensive knowledge of relevant laws, acts, and regulations
- Detailed understanding of legal procedures and compliance requirements
- Experience with penalty calculations and enforcement mechanisms
- Familiarity with precedent cases and judicial interpretations
- Expertise in risk assessment and mitigation strategies

KNOWLEDGE BASE:
- Relevant Acts: {', '.join(self.relevant_acts[:5])}{'...' if len(self.relevant_acts) > 5 else ''}
- Legal Procedures: {len(self.legal_procedures)} specialized procedures
- Precedent Cases: {len(self.precedent_cases)} relevant cases
- Penalty Framework: {len(self.common_penalties)} penalty types

ANALYSIS APPROACH:
1. Identify specific legal issues within your specialization
2. Apply relevant statutory provisions and regulations
3. Reference applicable precedent cases
4. Calculate penalties and assess compliance requirements
5. Provide step-by-step legal procedures
6. Recommend risk mitigation strategies
7. Suggest alternative legal approaches

FORMATTING:
- Provide clear, structured legal analysis
- Use proper legal citation format
- Include specific section references
- Provide actionable recommendations
- Explain legal procedures step-by-step

Always provide comprehensive, accurate, and specialized legal guidance within your domain of expertise."""

    def get_agent_info(self) -> Dict[str, Any]:
        """Get comprehensive agent information"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "specialization": self.specialization,
            "created_at": self.created_at.isoformat(),
            "case_count": self.case_count,
            "success_rate": self.success_rate,
            "knowledge_areas": len(self.knowledge_base),
            "procedures_count": len(self.legal_procedures),
            "relevant_acts_count": len(self.relevant_acts),
            "precedent_cases_count": len(self.precedent_cases)
        }
    
    def update_metrics(self, success: bool):
        """Update agent performance metrics"""
        self.case_count += 1
        if success:
            self.success_rate = ((self.success_rate * (self.case_count - 1)) + 1) / self.case_count
        else:
            self.success_rate = (self.success_rate * (self.case_count - 1)) / self.case_count

        logger.info(f"{self.agent_name} metrics updated: {self.case_count} cases, {self.success_rate:.2f} success rate")

    def get_ai_client(self):
        """Initialize and return NVIDIA AI client using requests"""
        if self.ai_client is None and AI_AVAILABLE:
            try:
                # Test NVIDIA API connection
                headers = {
                    "Authorization": f"Bearer {NVIDIA_API_KEY}",
                    "Content-Type": "application/json"
                }

                # Simple test request to verify API key
                test_payload = {
                    "model": NVIDIA_MODEL,
                    "messages": [{"role": "user", "content": "test"}],
                    "max_tokens": 10
                }

                response = requests.post(
                    f"{NVIDIA_BASE_URL}/chat/completions",
                    headers=headers,
                    json=test_payload,
                    timeout=10
                )

                if response.status_code == 200:
                    self.ai_client = "requests_client"  # Use requests as client
                    logger.info(f"NVIDIA API connection verified for {self.agent_name}")
                    return self.ai_client
                else:
                    logger.error(f"NVIDIA API test failed with status {response.status_code}")
                    self.ai_client = None
                    return None

            except Exception as e:
                logger.error(f"Failed to initialize NVIDIA API connection: {e}")
                logger.warning(f"Will use fallback responses for {self.agent_name}")
                self.ai_client = None
                return None
        return self.ai_client

    def call_nvidia_api(self, query: str, case_details: str) -> str:
        """Call NVIDIA API for professional legal analysis using requests"""
        try:
            client = self.get_ai_client()
            if not client:
                logger.warning(f"NVIDIA API not available for {self.agent_name}, using fallback response")
                return self.generate_fallback_response(query, case_details)

            # Create specialized system prompt
            system_prompt = self.get_specialized_system_prompt()

            # Create user prompt with professional format
            user_prompt = self.create_professional_prompt(query, case_details)

            logger.info(f"Calling NVIDIA API for {self.agent_name} with model {NVIDIA_MODEL}")

            try:
                headers = {
                    "Authorization": f"Bearer {NVIDIA_API_KEY}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": NVIDIA_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 6000,
                    "top_p": 0.9
                }

                response = requests.post(
                    f"{NVIDIA_BASE_URL}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    response_data = response.json()
                    api_response = response_data['choices'][0]['message']['content']
                    logger.info(f"NVIDIA API response received successfully for {self.agent_name}")

                    # Validate response format
                    if not api_response or len(api_response.strip()) < 100:
                        logger.warning(f"NVIDIA API returned insufficient response for {self.agent_name}, using fallback")
                        return self.generate_fallback_response(query, case_details)

                    return api_response
                else:
                    logger.error(f"NVIDIA API call failed with status {response.status_code}: {response.text}")
                    return self.generate_fallback_response(query, case_details)

            except Exception as api_error:
                logger.error(f"NVIDIA API call failed for {self.agent_name}: {str(api_error)}")
                logger.info(f"Falling back to structured response for {self.agent_name}")
                return self.generate_fallback_response(query, case_details)

        except Exception as e:
            logger.error(f"Error in NVIDIA API call for {self.agent_name}: {str(e)}")
            return self.generate_fallback_response(query, case_details)

    def get_specialized_system_prompt(self) -> str:
        """Get specialized system prompt for BhimLaw AI professional format"""

        base_prompt = f"""You are {self.agent_name}, a senior legal expert with 20+ years of specialized practice in {self.specialization}.

SPECIALIZATION: {self.specialization}

CRITICAL RESPONSE REQUIREMENTS:
You must provide a comprehensive, professional legal analysis in the EXACT JSON format specified below. This is the BhimLaw AI professional format that provides expert-level legal consultation.

REQUIRED JSON STRUCTURE:
{{
    "legal_classification": {{
        "domain": "Specific legal domain (e.g., Service Law / Administrative Law)",
        "jurisdiction": "Applicable jurisdiction (e.g., Central Government India)",
        "relevant_forum": [
            "Primary forum (e.g., Departmental Appellate Authority)",
            "Secondary forum (e.g., Central Administrative Tribunal)",
            "Appellate forum (e.g., High Court under Article 226)"
        ]
    }},
    "applicable_laws": [
        {{
            "law_rule": "Act/Rule name with year",
            "section_clause": "Specific section/clause",
            "description": "Detailed description of provision"
        }}
    ],
    "landmark_judgments": [
        {{
            "case": "Case name with parties",
            "citation": "Full legal citation (AIR/SCC format with year)",
            "principle": "Legal principle established by the case"
        }}
        // CRITICAL: Include 8-10 relevant landmark judgments with proper citations
        // Use real case names, accurate citations, and established legal principles
        // Focus on cases directly relevant to the user's specific legal issue
        // Include both Supreme Court and High Court cases where applicable
        // Ensure citations are in proper AIR/SCC format (e.g., "AIR 2020 SC 1234")
    ],
    "legal_remedy_path": [
        {{
            "step": "Step number and title",
            "action": "Specific action to be taken",
            "time_limit": "Timeline for action",
            "template_available": true/false
        }}
    ],
    "additional_insights": {{
        "bail_applicability": {{
            "applicable": true/false,
            "reasoning": "Explanation of bail applicability"
        }},
        "estimated_legal_fees": "Fee range in INR",
        "timeline_estimate": "Expected duration",
        "success_probability": {{
            "percentage": "Success rate percentage",
            "reasoning": "Factors supporting the assessment"
        }}
    }},
    "professional_advice": {{
        "immediate_actions": ["List of immediate steps"],
        "evidence_required": ["List of required evidence"],
        "risk_factors": ["List of potential risks"]
    }}
}}

EXPERTISE AREAS:
- Comprehensive knowledge of {', '.join(self.relevant_acts[:3])}
- 20+ years of specialized legal practice
- Extensive experience with {self.specialization}
- Deep understanding of procedural and substantive law
- Expert knowledge of case precedents and judicial trends

ANALYSIS REQUIREMENTS:
- Provide detailed, professional legal analysis like a senior advocate
- Include 8-10 relevant landmark judgments with accurate case names and proper legal citations (AIR, SCC format)
- Ensure all case citations are real and verifiable (e.g., "AIR 2020 SC 1234", "2019 SCC OnLine SC 567")
- Include both Supreme Court and High Court cases relevant to the specific legal issue
- Explain complex legal procedures in actionable steps
- Provide strategic legal advice with success probability assessment
- Use professional legal language and terminology
- Be comprehensive and detailed like a legal opinion
- Include constitutional and procedural aspects
- Provide practical implementation guidance
- Use current laws and recent judicial pronouncements

LANDMARK JUDGMENTS REQUIREMENTS:
- Generate 8-10 landmark judgments directly relevant to the user's specific legal issue
- Use accurate case names with proper party names
- Provide proper legal citations in AIR/SCC format with correct years
- Include established legal principles from each case
- Focus on cases that directly support the legal analysis and remedy path
- Include mix of foundational cases and recent relevant judgments
- Ensure all citations are formatted correctly (e.g., "AIR 1986 SC 180", "2020 SCC OnLine NCDRC 1172")

IMPORTANT:
- Respond ONLY in valid JSON format
- No markdown formatting or extra text
- Use real legal principles and established case law
- Provide detailed explanations like a professional legal opinion
- Include strategic considerations and risk assessment
- All legal advice must be current and accurate"""

        # Add specialized prompts for specific agent types
        if "Employee & Service Matters" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR GOVERNMENT EMPLOYEE CASES:
- 20+ years in government service law and employment disputes
- Expert in Central Civil Services Rules and DoPT guidelines
- Extensive CAT practice and Supreme Court service law cases
- Specialized in promotion disputes, salary issues, and harassment cases
- Deep knowledge of constitutional service law principles

FOR PROMOTION/SALARY DISPUTES - INCLUDE:
- Central Civil Services (Conduct) Rules, 1964
- DoPT Promotions Guidelines (Current Version)
- CCS (CCA) Rules, 1965 for appeals
- Constitutional Articles 14, 16 (equality and equal opportunity)
- CAT jurisdiction and procedures
- Service jurisprudence and recent precedents
- Departmental grievance procedures
- RTI strategies for service matters
- Back pay calculations and interest provisions"""

        elif "Property & Building Violations" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR PROPERTY & BUILDING VIOLATIONS:
- 20+ years in municipal law and building regulations
- Expert in Building Bye-laws and Municipal Zoning Guidelines
- Extensive experience with unauthorized construction cases
- Specialized in property tax disputes and building violations
- Deep knowledge of urban planning and development control rules

FOR BUILDING VIOLATION CASES - INCLUDE:
- Building Bye-laws and Municipal Corporation Acts
- Development Control Regulations and Zoning Guidelines
- Property Tax Assessment Rules and Appeals
- Constitutional Articles 19, 300A (property rights)
- High Court and Supreme Court property law precedents
- Municipal tribunal procedures and remedies
- Demolition stay orders and regularization procedures
- Compensation and alternative relief mechanisms"""

        elif "Environmental & Public Health" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR ENVIRONMENTAL & PUBLIC HEALTH:
- 20+ years in environmental law and public health regulations
- Expert in NGT Act, Municipal Health Bye-laws, SWM Rules
- Extensive NGT practice and environmental litigation
- Specialized in pollution control and waste management cases
- Deep knowledge of constitutional environmental law principles

FOR ENVIRONMENTAL CASES - INCLUDE:
- NGT Act 2010 and Environmental Protection Act 1986
- Municipal Health Bye-laws and SWM Rules 2016
- Water and Air Pollution Control Acts
- Constitutional Articles 21, 48A (environmental protection)
- NGT procedures and environmental compensation
- Pollution Control Board powers and remedies
- Public health emergency provisions
- Community participation in environmental protection"""

        elif "RTI & Transparency" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR RTI & TRANSPARENCY:
- 20+ years in information law and transparency advocacy
- Expert in RTI Act 2005 and CIC Guidelines
- Extensive CIC practice and information tribunal cases
- Specialized in government transparency and accountability
- Deep knowledge of constitutional right to information principles

FOR RTI CASES - INCLUDE:
- RTI Act 2005 and CIC Guidelines
- State RTI Rules and Information Commission procedures
- Constitutional Articles 19(1)(a) (freedom of speech and expression)
- Supreme Court and High Court RTI precedents
- CIC jurisdiction and penalty provisions
- Contempt proceedings for RTI violations
- Proactive disclosure requirements
- Third party information and exemption challenges"""

        elif "Infrastructure & Public Works" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR INFRASTRUCTURE & PUBLIC WORKS:
- 20+ years in public works law and infrastructure disputes
- Expert in Public Works Code and Municipal Damage Compensation Rules
- Extensive experience with PWD and urban development cases
- Specialized in road construction, drainage, and metro project impacts
- Deep knowledge of infrastructure development and citizen rights

FOR INFRASTRUCTURE CASES - INCLUDE:
- Public Works Code and PWD Manual
- Municipal Damage Compensation Rules and Urban Development Acts
- Land Acquisition Act 2013 and infrastructure projects
- Constitutional Articles 21, 300A (life and property rights)
- Infrastructure tribunal procedures and compensation
- Environmental clearance and public consultation requirements
- Project affected persons rehabilitation
- Public-private partnership dispute resolution"""

        elif "Encroachment & Land" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR ENCROACHMENT & LAND:
- 20+ years in land law and encroachment disputes
- Expert in Public Land Encroachment Act and Land Revenue Code
- Extensive revenue court and land tribunal practice
- Specialized in illegal encroachment and eviction proceedings
- Deep knowledge of land rights and revenue law principles

FOR ENCROACHMENT CASES - INCLUDE:
- Public Land Encroachment Act and Land Revenue Code
- Survey and Settlement Acts and Revenue Records
- Constitutional Articles 19(1)(f), 300A (property and occupation rights)
- Revenue court procedures and land tribunal jurisdiction
- Tehsildar and Collector powers for eviction
- Survey and demarcation procedures
- Adverse possession and title disputes
- Rehabilitation and alternative accommodation rights"""

        elif "Licensing & Trade Regulation" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR LICENSING & TRADE REGULATION:
- 20+ years in trade law and business licensing
- Expert in Shop & Establishment Act and FSSAI regulations
- Extensive licensing authority and trade tribunal practice
- Specialized in business permits and vendor regulation
- Deep knowledge of commercial law and trade rights

FOR LICENSING CASES - INCLUDE:
- Shop & Establishment Act and Trade License Rules
- FSSAI Act 2006 and Food Safety Regulations
- Street Vendors Act 2014 and Vending Guidelines
- Constitutional Articles 19(1)(g) (trade and business rights)
- Licensing authority procedures and appeal mechanisms
- Municipal corporation powers and trade regulation
- Fire safety and health clearance requirements
- Ease of Doing Business Act provisions"""

        elif "Slum Clearance & Resettlement" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR SLUM CLEARANCE & RESETTLEMENT:
- 20+ years in housing law and slum rehabilitation
- Expert in Slum Rehabilitation Act and RAY Scheme
- Extensive housing tribunal and rehabilitation authority practice
- Specialized in eviction proceedings and resettlement rights
- Deep knowledge of constitutional housing rights and urban development

FOR SLUM REHABILITATION CASES - INCLUDE:
- Slum Rehabilitation Act and State Housing Policies
- RAY Scheme and PMAY Guidelines for urban housing
- Land Acquisition and R&R Act 2013
- Constitutional Articles 21, 19 (right to shelter and residence)
- Housing tribunal procedures and rehabilitation authority powers
- Cut-off date eligibility and survey requirements
- Transit accommodation and permanent housing rights
- Livelihood restoration and community participation"""

        elif "Water & Drainage" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR WATER & DRAINAGE:
- 20+ years in water law and municipal services
- Expert in Water Supply & Sewerage Control Rules
- Extensive water board and municipal tribunal practice
- Specialized in water supply, drainage, and quality issues
- Deep knowledge of constitutional water rights and public health

FOR WATER & DRAINAGE CASES - INCLUDE:
- Water Supply & Sewerage Control Rules
- Municipal Water Board Acts and Service Regulations
- Water (Prevention and Control of Pollution) Act 1974
- Constitutional Articles 21 (right to clean water and sanitation)
- Water board procedures and consumer grievance mechanisms
- Water quality standards and testing requirements
- Drainage system maintenance and flood prevention
- Water tariff disputes and service guarantee provisions"""

        elif "Public Nuisance" in self.agent_name:
            base_prompt += """

SPECIAL EXPERTISE FOR PUBLIC NUISANCE:
- 20+ years in criminal law and public order
- Expert in IPC Section 268 and Noise Pollution Rules
- Extensive magistrate court and police station practice
- Specialized in noise complaints, animal menace, and public disturbances
- Deep knowledge of constitutional public order and individual rights balance

FOR PUBLIC NUISANCE CASES - INCLUDE:
- IPC Sections 268-294A (public nuisance provisions)
- Noise Pollution (Regulation and Control) Rules
- Prevention of Cruelty to Animals Act 1960
- Constitutional Articles 19, 21 (freedom and peaceful environment)
- Magistrate court procedures and police powers
- Municipal corporation enforcement mechanisms
- Environmental court jurisdiction for noise pollution
- Community mediation and alternative dispute resolution"""

        return base_prompt

    def create_professional_prompt(self, query: str, case_details: str) -> str:
        """Create professional legal analysis prompt with enhanced BhimLaw format"""
        return f"""
You are a senior legal expert providing comprehensive analysis. Analyze this legal query with the precision and depth of a seasoned advocate.

LEGAL QUERY: {query}
CASE DETAILS: {case_details}
SPECIALIZATION: {self.specialization}

Provide your analysis in this EXACT JSON format:

{{
    "legal_classification": {{
        "domain": "Specific legal domain (e.g., Service Law / Administrative Law)",
        "jurisdiction": "Applicable jurisdiction (e.g., Central Government India)",
        "relevant_forum": [
            "Primary forum (e.g., Departmental Appellate Authority)",
            "Secondary forum (e.g., Central Administrative Tribunal)",
            "Appellate forum (e.g., High Court under Article 226)"
        ]
    }},
    "applicable_laws": [
        {{
            "law_rule": "Act/Rule name",
            "section_clause": "Specific section/clause",
            "description": "Detailed description of provision"
        }}
    ],
    "landmark_judgments": [
        {{
            "case": "Case name",
            "citation": "Full citation",
            "principle": "Legal principle established"
        }}
    ],
    "legal_remedy_path": [
        {{
            "step": "Step 1: Internal Representation",
            "action": "File written grievance to HOD/Appellate Authority",
            "time_limit": "Within 90 days of denial",
            "template_available": true
        }},
        {{
            "step": "Step 2: RTI Filing",
            "action": "File RTI to obtain DPC minutes, promotion policy, ACR reports",
            "time_limit": "30 days response time",
            "template_available": true
        }},
        {{
            "step": "Step 3: Departmental Inquiry",
            "action": "Demand departmental review if bias established",
            "time_limit": "As per departmental rules",
            "template_available": false
        }},
        {{
            "step": "Step 4: File Before CAT/Court",
            "action": "File formal petition with specific reliefs",
            "time_limit": "Within limitation period",
            "template_available": true
        }}
    ],
    "additional_insights": {{
        "bail_applicability": {{
            "applicable": false,
            "reasoning": "Civil/service matter, not criminal"
        }},
        "estimated_legal_fees": "₹5,000 - ₹50,000 (varies by counsel and location)",
        "timeline_estimate": "6-18 months for CAT + Departmental levels",
        "success_probability": {{
            "percentage": "80%",
            "reasoning": "With documented proof and proper APARs"
        }}
    }},
    "professional_advice": {{
        "immediate_actions": [
            "Document all communications with superior",
            "Collect performance records and ACRs",
            "File RTI for transparency"
        ],
        "evidence_required": [
            "Service records",
            "Performance evaluations",
            "Correspondence with superior",
            "Promotion policy documents"
        ],
        "risk_factors": [
            "Delay in filing may weaken case",
            "Lack of documentary evidence",
            "Departmental politics"
        ]
    }}
}}

Ensure all legal advice is current and includes latest amendments and judicial pronouncements."""

    def generate_fallback_response(self, query: str, case_details: str) -> str:
        """Generate fallback response when AI is unavailable"""
        import json

        fallback_analysis = {
            "legal_issue_identified": {
                "nature_of_grievance": f"Legal matter requiring specialized analysis in {self.specialization}",
                "primary_concern": "Detailed analysis required with expert legal consultation",
                "constitutional_implications": "Constitutional provisions may apply based on case specifics"
            },
            "applicable_legal_framework": {
                "primary_laws": self.relevant_acts[:3],
                "supporting_regulations": ["Applicable rules and regulations", "State-specific provisions"],
                "constitutional_provisions": ["Relevant constitutional articles"],
                "policy_guidelines": ["Government policies and circulars"]
            },
            "action_plan": {
                "step_1": {
                    "title": "Legal Consultation and Case Assessment",
                    "details": [
                        "Consult with qualified legal expert",
                        "Detailed case fact analysis",
                        "Legal merit assessment"
                    ],
                    "importance": "Professional legal guidance essential for complex matters"
                },
                "step_2": {
                    "title": "Documentation and Evidence Collection",
                    "details": [
                        "Gather all relevant documents",
                        "Collect supporting evidence",
                        "Prepare chronological timeline"
                    ],
                    "timeline": "1-2 weeks for comprehensive documentation"
                },
                "step_3": {
                    "title": "Legal Research and Precedent Analysis",
                    "details": [
                        "Research applicable case law",
                        "Analyze relevant precedents",
                        "Study recent judicial trends"
                    ],
                    "optional": "Essential for building strong legal foundation"
                },
                "step_4": {
                    "title": "Legal Proceedings Strategy",
                    "details": [
                        "Determine appropriate forum",
                        "Prepare legal documentation",
                        "File appropriate proceedings"
                    ],
                    "expected_outcome": "Relief as per applicable legal provisions"
                }
            },
            "legal_arguments": {
                "primary_argument": "Legal rights and remedies under applicable statutory provisions",
                "supporting_arguments": [
                    "Constitutional safeguards and protections",
                    "Statutory compliance and procedural requirements",
                    "Precedent-based legal principles"
                ],
                "counter_arguments": "Potential defenses and legal challenges to be addressed"
            },
            "case_precedents_note": "Comprehensive landmark judgments with proper citations are generated by our AI legal expert. Please retry your query to get detailed case precedents relevant to your specific legal issue.",
            "success_probability": {
                "percentage": "Depends on case merits and evidence",
                "factors_favoring": ["Strong legal foundation", "Applicable precedents", "Constitutional protections"],
                "potential_challenges": ["Procedural requirements", "Evidence sufficiency", "Legal complexities"],
                "mitigation_strategies": ["Expert legal representation", "Comprehensive preparation", "Strategic approach"]
            },
            "timeline_and_costs": {
                "departmental_stage": "2-6 months for administrative remedies",
                "legal_proceedings": "6 months to 2 years depending on complexity",
                "estimated_costs": "Legal fees as per case complexity and duration",
                "total_duration": "Varies based on case specifics and legal strategy"
            },
            "professional_recommendations": [
                "Engage qualified legal expert immediately",
                "Comprehensive case documentation and evidence collection",
                "Strategic legal approach based on case merits",
                "Consider alternative dispute resolution where applicable",
                "Ensure compliance with all procedural requirements"
            ],
            "note": "This is a preliminary framework. Detailed legal analysis requires expert consultation and case-specific research."
        }

        return json.dumps(fallback_analysis, indent=2)

    def format_response_with_emojis(self, analysis_data: Dict[str, Any], case_details: str, case_type: str) -> Dict[str, Any]:
        """Format response in the user's preferred style with emojis and detailed structure"""

        # Create the formatted response with emojis and detailed structure
        formatted_response = {
            "case_type": case_type,
            "specialization": self.specialization,
            "agent_name": self.agent_name,
            "analysis_timestamp": datetime.now().isoformat(),
            "ai_analysis_parsed": analysis_data.get("ai_analysis_parsed", True),
            "formatted_response": self.create_emoji_formatted_response(analysis_data, case_details, case_type)
        }

        return formatted_response

    def create_emoji_formatted_response(self, analysis_data: Dict[str, Any], case_details: str, case_type: str) -> str:
        """Create the emoji-formatted response string matching user's example with enhanced formatting"""

        # Get the legal classification data
        legal_class = analysis_data.get("legal_classification", {})
        applicable_laws = analysis_data.get("applicable_laws", [])
        landmark_judgments = analysis_data.get("landmark_judgments", [])
        legal_remedy_path = analysis_data.get("legal_remedy_path", [])
        additional_insights = analysis_data.get("additional_insights", {})
        professional_advice = analysis_data.get("professional_advice", {})

        # Build the formatted response with proper timestamp
        current_time = datetime.now().strftime("%I:%M:%S %p")

        response = f"""{case_details}
{current_time}
👥
🧾 BhimLaw AI – Expert Legal Analysis
{self.agent_name}

🧑‍⚖️ Legal Classification
Domain: {legal_class.get('domain', 'Service Law / Administrative Law')}
Jurisdiction: {legal_class.get('jurisdiction', 'Central Government (India)')}
Relevant Forum:"""

        # Add relevant forums
        forums = legal_class.get('relevant_forum', [
            "Departmental Appellate Authority",
            "Central Administrative Tribunal (CAT)",
            "High Court (under Article 226)"
        ])
        for forum in forums:
            response += f"\n{forum}"

        # Add applicable laws table with proper formatting
        response += f"""

📜 Applicable Laws & Provisions
Law/Rule	Section/Clause	Description"""

        # Ensure we have at least 5 laws
        if not applicable_laws:
            applicable_laws = self.get_default_applicable_laws()

        for law in applicable_laws[:5]:  # Limit to 5 laws
            law_rule = law.get('law_rule', 'N/A')
            section = law.get('section_clause', 'N/A')
            desc = law.get('description', 'N/A')
            response += f"\n{law_rule}	{section}	{desc}"

        # Add landmark judgments table with proper formatting
        response += f"""

📚 Landmark Judgments
Case	Citation	Principle"""

        # Ensure we have at least 3 judgments
        if not landmark_judgments:
            landmark_judgments = self.get_default_landmark_judgments()

        for judgment in landmark_judgments[:3]:  # Limit to 3 judgments
            case = judgment.get('case', 'N/A')
            citation = judgment.get('citation', 'N/A')
            principle = judgment.get('principle', 'N/A')
            response += f"\n{case}	{citation}	{principle}"

        # Add legal remedy path with enhanced formatting
        response += f"""

🔍 Legal Remedy Path"""

        # Ensure we have at least 4 steps
        if not legal_remedy_path:
            legal_remedy_path = self.get_default_legal_remedy_path()

        for i, step in enumerate(legal_remedy_path[:4], 1):  # Limit to 4 steps
            step_title = step.get('step', f'Step {i}')
            action = step.get('action', 'N/A')
            time_limit = step.get('time_limit', 'As applicable')
            template = "✅ Yes" if step.get('template_available', False) else "❌ No"

            response += f"""
{i}
{step_title}
Action: {action}
Time Limit: {time_limit}
Template Available: {template}"""

        # Add additional insights with enhanced formatting
        bail_info = additional_insights.get('bail_applicability', {})
        bail_applicable = "✅ Yes" if bail_info.get('applicable', False) else "❌ No"

        success_prob = additional_insights.get('success_probability', {})
        success_percentage = success_prob.get('percentage', '80%')
        success_reasoning = success_prob.get('reasoning', 'With documented proof and proper APARs')

        response += f"""

📌 Additional Insights
Bail Applicability: {bail_applicable}
{bail_info.get('reasoning', 'Not applicable – civil/service matter')}
Estimated Legal Fees: {additional_insights.get('estimated_legal_fees', '₹5,000 – ₹50,000 (varies by counsel and location)')}
Timeline Estimate: {additional_insights.get('timeline_estimate', '6–18 months for CAT + Departmental levels')}
Success Probability: {success_percentage}
{success_reasoning}

💼 Professional Advice
🔥 Immediate Actions:"""

        # Add immediate actions with defaults if empty
        immediate_actions = professional_advice.get('immediate_actions', [])
        if not immediate_actions:
            immediate_actions = self.get_default_immediate_actions()

        for action in immediate_actions:
            response += f"\n• {action}"

        response += f"""

📋 Evidence Required:"""

        # Add evidence required with defaults if empty
        evidence_required = professional_advice.get('evidence_required', [])
        if not evidence_required:
            evidence_required = self.get_default_evidence_required()

        for evidence in evidence_required:
            response += f"\n• {evidence}"

        response += f"""

⚠️ Risk Factors:"""

        # Add risk factors with defaults if empty
        risk_factors = professional_advice.get('risk_factors', [])
        if not risk_factors:
            risk_factors = self.get_default_risk_factors()

        for risk in risk_factors:
            response += f"\n• {risk}"

        return response

    def get_default_applicable_laws(self) -> List[Dict[str, str]]:
        """Get default applicable laws for this agent's specialization"""
        return [
            {
                "law_rule": "Central Civil Services (Conduct) Rules, 1964",
                "section_clause": "Rule 3(1)(ii)",
                "description": "Obligation of public servant to act fairly and impartially"
            },
            {
                "law_rule": "DoPT Office Memorandum (Promotion Guidelines)",
                "section_clause": "Current Revision",
                "description": "Timelines, benchmarks, and conditions for promotion"
            },
            {
                "law_rule": "CCS (CCA) Rules, 1965",
                "section_clause": "Rule 14",
                "description": "Grounds for disciplinary action against superiors if bias/misconduct proven"
            },
            {
                "law_rule": "CAT Act, 1985",
                "section_clause": "Section 19",
                "description": "Jurisdiction for service disputes including promotion denial"
            },
            {
                "law_rule": "RTI Act, 2005",
                "section_clause": "Sections 6 & 7",
                "description": "Right to obtain promotion criteria, DPC minutes, etc."
            }
        ]

    def get_default_landmark_judgments(self) -> List[Dict[str, str]]:
        """Get default landmark judgments for this agent's specialization"""
        return [
            {
                "case": "Union of India v. Hemraj Singh Chauhan",
                "citation": "(2010) 4 SCC 290",
                "principle": "Delay or denial in DPC violates Article 14 (equality)"
            },
            {
                "case": "Ajit Singh v. State of Punjab",
                "citation": "AIR 1999 SC 3471",
                "principle": "Eligible candidates cannot be ignored arbitrarily for promotion"
            },
            {
                "case": "R.K. Jain v. Union of India",
                "citation": "AIR 1993 SC 1769",
                "principle": "Disciplinary action against officers misusing authority"
            }
        ]

    def get_default_legal_remedy_path(self) -> List[Dict[str, Any]]:
        """Get default legal remedy path for this agent's specialization"""
        return [
            {
                "step": "Step 1: Internal Representation",
                "action": "File written grievance to Head of Department (HOD) or Appellate Authority",
                "time_limit": "Preferably within 90 days of denial",
                "template_available": True
            },
            {
                "step": "Step 2: RTI Filing",
                "action": "File RTI to obtain DPC minutes, promotion policy, ACR/APAR reports, list of promoted employees",
                "time_limit": "30 days response time",
                "template_available": True
            },
            {
                "step": "Step 3: Departmental Inquiry",
                "action": "Demand departmental review if bias is established (trigger Rule 14 proceedings)",
                "time_limit": "As per departmental rules",
                "template_available": False
            },
            {
                "step": "Step 4: File Before CAT",
                "action": "File CAT Form 1 seeking promotion with retrospective effect, salary arrears with interest, disciplinary action against superior",
                "time_limit": "Within limitation period",
                "template_available": True
            }
        ]

    def get_default_immediate_actions(self) -> List[str]:
        """Get default immediate actions for this agent's specialization"""
        return [
            "Document all communications with superior",
            "Collect performance records and ACRs",
            "File RTI for transparency",
            "Maintain detailed correspondence"
        ]

    def get_default_evidence_required(self) -> List[str]:
        """Get default evidence required for this agent's specialization"""
        return [
            "Service records",
            "Performance evaluations (APARs)",
            "Correspondence with superior",
            "Promotion policy documents",
            "DPC minutes"
        ]

    def get_default_risk_factors(self) -> List[str]:
        """Get default risk factors for this agent's specialization"""
        return [
            "Delay in filing may weaken case",
            "Lack of documentary evidence",
            "Departmental politics",
            "Superior's counter-allegations"
        ]

class PropertyBuildingViolationsAgent(SpecializedLegalAgent):
    """
    Specialized agent for Property & Building Violations
    Handles unauthorized constructions, building violations, property tax disputes
    """
    
    def __init__(self):
        super().__init__(
            "Property & Building Violations Specialist",
            "Property Law, Building Regulations, Municipal Law, Zoning Laws"
        )
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "building_regulations": {
                "unauthorized_construction": {
                    "definition": "Construction without proper approvals or permits",
                    "applicable_sections": ["Section 264 of Municipal Corporation Act", "Building Bye-laws"],
                    "penalties": "Fine up to Rs. 50,000 or demolition",
                    "procedure": ["Notice issuance", "Show cause hearing", "Penalty imposition", "Demolition order"]
                },
                "building_violations": {
                    "types": ["Height violations", "Setback violations", "FAR violations", "Parking violations"],
                    "assessment_criteria": ["Building plans", "Site inspection", "Measurement verification"],
                    "remedial_measures": ["Regularization", "Penalty payment", "Structural modifications"]
                }
            },
            "property_tax_disputes": {
                "assessment_appeals": {
                    "grounds": ["Incorrect valuation", "Wrong classification", "Calculation errors"],
                    "procedure": ["Appeal filing", "Document submission", "Hearing", "Order"],
                    "time_limits": "30 days from assessment order"
                }
            },
            "zoning_laws": {
                "land_use_violations": {
                    "commercial_in_residential": "Penalty and closure notice",
                    "industrial_in_commercial": "Heavy penalties and relocation",
                    "mixed_use_violations": "Regularization possible with fees"
                }
            }
        }
    
    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "unauthorized_construction_action": [
                "1. Site inspection and documentation",
                "2. Issue show cause notice under Section 264",
                "3. Conduct hearing within 15 days",
                "4. Pass demolition/penalty order",
                "5. Execute demolition if non-compliance",
                "6. Recover costs from violator"
            ],
            "building_plan_approval": [
                "1. Submit application with required documents",
                "2. Technical scrutiny by building department",
                "3. Site inspection if required",
                "4. Approval/rejection with reasons",
                "5. Fee payment and permit issuance"
            ],
            "property_tax_appeal": [
                "1. File appeal within 30 days",
                "2. Submit supporting documents",
                "3. Pay appeal fee",
                "4. Attend hearing",
                "5. Await appellate order",
                "6. Further appeal to tribunal if needed"
            ]
        }
    
    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Municipal Corporation Act, 1956",
            "Delhi Municipal Corporation Act, 1957",
            "Building Bye-laws",
            "Master Plan for Delhi 2021",
            "Delhi Development Act, 1957",
            "Property Tax Assessment Rules",
            "Urban Land (Ceiling and Regulation) Act, 1976",
            "Real Estate (Regulation and Development) Act, 2016",
            "Environment (Protection) Act, 1986",
            "Fire Prevention and Fire Safety Act"
        ]
    
    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "unauthorized_construction": "Rs. 10,000 to Rs. 50,000 + demolition costs",
            "height_violation": "Rs. 5,000 per sq ft of excess area",
            "setback_violation": "Rs. 2,000 per sq ft of violation",
            "parking_violation": "Rs. 50,000 per missing parking space",
            "commercial_in_residential": "Rs. 25,000 + monthly penalty",
            "property_tax_evasion": "200% of evaded tax + interest",
            "building_plan_violation": "Rs. 1,000 to Rs. 10,000 per violation"
        }
    
    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []
    
    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze property and building violation cases with BhimLaw AI professional format"""
        try:
            import json

            # First check if this query is within our domain
            if not self.is_query_in_domain(case_details, case_type):
                # Query is outside our domain, redirect to appropriate agent
                return self.get_redirect_response(case_details, case_type)

            # Query is in our domain, proceed with full analysis
            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Property Law / Municipal Law",
                    "jurisdiction": "Municipal Corporation / State Government",
                    "relevant_forum": [
                        "Municipal Corporation",
                        "District Collector Office",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [],
                "landmark_judgments": [],
                "legal_remedy_path": [],
                "additional_insights": {},
                "professional_advice": {}
            }

            case_lower = case_details.lower()

            # Enhanced issue identification for property and building cases
            if "unauthorized" in case_lower or "illegal construction" in case_lower or "building violation" in case_lower:
                analysis["applicable_laws"] = [
                    {
                        "law_rule": "Building Bye-laws",
                        "section_clause": "Section 15-20",
                        "description": "Regulations for authorized construction and approval procedures"
                    },
                    {
                        "law_rule": "Municipal Corporation Act",
                        "section_clause": "Section 343-350",
                        "description": "Powers of municipal corporation for building control and demolition"
                    },
                    {
                        "law_rule": "Development Control Regulations",
                        "section_clause": "DCR 33",
                        "description": "Zoning regulations and permissible construction parameters"
                    },
                    {
                        "law_rule": "Right to Fair Compensation and Transparency in Land Acquisition Act, 2013",
                        "section_clause": "Section 24",
                        "description": "Compensation for acquisition and demolition procedures"
                    }
                ]

                analysis["landmark_judgments"] = [
                    {
                        "case": "AI-Generated Landmark Judgments Not Available",
                        "citation": "Please retry query for comprehensive case citations",
                        "principle": "Landmark judgments with proper citations are generated by our AI legal expert"
                    }
                ]

                analysis["legal_remedy_path"] = [
                    {
                        "step": "Step 1: Documentation & Verification",
                        "action": "Collect all building documents, sanctioned plans, and correspondence with municipal authorities",
                        "time_limit": "Immediate - within 7 days of notice",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: RTI Application",
                        "action": "File RTI to obtain copy of sanctioned plan, inspection reports, and demolition procedure compliance",
                        "time_limit": "30 days response time",
                        "template_available": True
                    },
                    {
                        "step": "Step 3: Municipal Representation",
                        "action": "File representation to Municipal Commissioner challenging demolition notice on procedural grounds",
                        "time_limit": "Within 15 days of demolition notice",
                        "template_available": True
                    },
                    {
                        "step": "Step 4: High Court Petition",
                        "action": "File writ petition under Article 226 challenging arbitrary demolition or seeking regularization",
                        "time_limit": "Before demolition date or within limitation",
                        "template_available": True
                    }
                ]

                analysis["additional_insights"] = {
                    "bail_applicability": {
                        "applicable": False,
                        "reasoning": "Civil matter - no criminal charges typically involved"
                    },
                    "estimated_legal_fees": "₹25,000 - ₹2,00,000 (varies by case complexity and court level)",
                    "timeline_estimate": "3-12 months for resolution through legal channels",
                    "success_probability": {
                        "percentage": "60-80%",
                        "reasoning": "If procedural violations or eligibility for regularization can be established"
                    }
                }

                analysis["professional_advice"] = {
                    "immediate_actions": [
                        "Collect all building documents and correspondence",
                        "File RTI for municipal records",
                        "Document any procedural violations by authorities",
                        "Engage qualified architect for compliance assessment"
                    ],
                    "evidence_required": [
                        "Sanctioned building plans",
                        "Municipal correspondence and notices",
                        "Inspection reports",
                        "Photographs of current structure",
                        "Property documents and tax receipts"
                    ],
                    "risk_factors": [
                        "Demolition risk high for clearly unauthorized structures",
                        "Penalty exposure: ₹10,000 to ₹5,00,000 plus costs",
                        "Time-sensitive nature of demolition notices",
                        "Municipal authority discretionary powers"
                    ]
                }

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in property violations analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}

    def get_default_applicable_laws(self) -> List[Dict[str, str]]:
        """Get default applicable laws for Property & Building Violations"""
        return [
            {
                "law_rule": "Building Bye-laws",
                "section_clause": "Section 15-20",
                "description": "Regulations for authorized construction and approval procedures"
            },
            {
                "law_rule": "Municipal Corporation Act, 1956",
                "section_clause": "Section 264",
                "description": "Powers to demolish unauthorized constructions"
            },
            {
                "law_rule": "Delhi Development Act, 1957",
                "section_clause": "Section 32",
                "description": "Prohibition of unauthorized development"
            },
            {
                "law_rule": "Property Tax Assessment Rules",
                "section_clause": "Rule 12-15",
                "description": "Property valuation and tax calculation methods"
            },
            {
                "law_rule": "Real Estate (Regulation and Development) Act, 2016",
                "section_clause": "Section 3",
                "description": "Registration requirements for real estate projects"
            }
        ]

    def get_default_landmark_judgments(self) -> List[Dict[str, str]]:
        """Get default landmark judgments for Property & Building Violations"""
        return [
            {
                "case": "Olga Tellis v. Bombay Municipal Corporation",
                "citation": "AIR 1986 SC 180",
                "principle": "Adequate notice and hearing required before demolition"
            },
            {
                "case": "Almitra Patel v. Union of India",
                "citation": "AIR 2000 SC 1256",
                "principle": "Municipal corporations duty to maintain cleanliness"
            },
            {
                "case": "M.C. Mehta v. Union of India",
                "citation": "AIR 1997 SC 734",
                "principle": "Environmental impact assessment mandatory"
            }
        ]

    def get_default_legal_remedy_path(self) -> List[Dict[str, Any]]:
        """Get default legal remedy path for Property & Building Violations"""
        return [
            {
                "step": "Step 1: Notice Response",
                "action": "Respond to municipal notice within stipulated time",
                "time_limit": "15-30 days from notice date",
                "template_available": True
            },
            {
                "step": "Step 2: Regularization Application",
                "action": "Apply for building plan approval/regularization if eligible",
                "time_limit": "Within 60 days of notice",
                "template_available": True
            },
            {
                "step": "Step 3: Appeal to Higher Authority",
                "action": "File appeal with Municipal Commissioner/District Collector",
                "time_limit": "30 days from adverse order",
                "template_available": True
            },
            {
                "step": "Step 4: High Court Petition",
                "action": "File writ petition under Article 226 for stay and relief",
                "time_limit": "Before demolition execution",
                "template_available": False
            }
        ]

    def get_default_immediate_actions(self) -> List[str]:
        """Get default immediate actions for Property & Building Violations"""
        return [
            "Respond to municipal notice immediately",
            "Collect all property documents and approvals",
            "Engage qualified architect for compliance assessment",
            "Document current structure with photographs"
        ]

    def get_default_evidence_required(self) -> List[str]:
        """Get default evidence required for Property & Building Violations"""
        return [
            "Original property documents",
            "Building plan approvals (if any)",
            "Municipal notices and correspondence",
            "Photographs of current structure",
            "Property tax receipts"
        ]

    def get_default_risk_factors(self) -> List[str]:
        """Get default risk factors for Property & Building Violations"""
        return [
            "Demolition risk high for clearly unauthorized structures",
            "Penalty exposure: ₹10,000 to ₹5,00,000 plus costs",
            "Time-sensitive nature of demolition notices",
            "Municipal authority discretionary powers"
        ]
    
    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to Property & Building Violations domain"""
        return [
            "unauthorized construction", "building violation", "property tax",
            "illegal construction", "demolition", "building permit", "zoning",
            "setback violation", "height violation", "fsr violation", "far violation",
            "building plan", "construction without approval", "municipal violation",
            "property", "building", "construction", "flat", "apartment", "structure",
            "mutation", "inheritance", "inherited", "property record", "property documents",
            "property registration", "property title", "property ownership", "property transfer",
            "revenue records", "land records", "property mutation", "name transfer"
        ]



class EnvironmentalPublicHealthAgent(SpecializedLegalAgent):
    """
    Specialized agent for Environmental & Public Health matters
    Handles garbage disposal, biomedical waste, mosquito breeding, pollution complaints
    """

    def __init__(self):
        super().__init__(
            "Environmental & Public Health Specialist",
            "Environmental Law, Public Health Regulations, Waste Management, Pollution Control"
        )

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "waste_management": {
                "garbage_disposal": {
                    "municipal_responsibility": "Door-to-door collection, segregation, processing",
                    "citizen_duties": "Segregation at source, timely disposal",
                    "violations": "Littering, improper disposal, burning waste",
                    "penalties": "Rs. 500 to Rs. 25,000"
                },
                "biomedical_waste": {
                    "applicable_rules": "Biomedical Waste Management Rules, 2016",
                    "authorization_required": "State Pollution Control Board",
                    "treatment_methods": "Incineration, autoclaving, chemical treatment",
                    "violations": "Improper segregation, unauthorized disposal"
                }
            },
            "pollution_control": {
                "air_pollution": {
                    "sources": ["Industrial emissions", "Vehicle exhaust", "Construction dust"],
                    "standards": "National Ambient Air Quality Standards",
                    "monitoring": "Continuous Ambient Air Quality Monitoring Stations"
                },
                "water_pollution": {
                    "sources": ["Industrial discharge", "Sewage", "Agricultural runoff"],
                    "standards": "Water Quality Standards",
                    "treatment": "Effluent Treatment Plants mandatory"
                },
                "noise_pollution": {
                    "limits": "Day: 55 dB, Night: 45 dB (Residential)",
                    "sources": ["Traffic", "Construction", "Industrial activities"],
                    "enforcement": "Police and Pollution Control Board"
                }
            },
            "public_health": {
                "mosquito_breeding": {
                    "prevention": "Eliminate stagnant water sources",
                    "municipal_action": "Fogging, larvicide treatment",
                    "penalties": "Rs. 500 for allowing breeding sites"
                },
                "food_safety": {
                    "licensing": "FSSAI registration mandatory",
                    "inspections": "Regular health department checks",
                    "violations": "Adulteration, unhygienic conditions"
                }
            }
        }

    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "pollution_complaint": [
                "1. File complaint with Pollution Control Board",
                "2. Provide detailed description and evidence",
                "3. Board conducts inspection within 15 days",
                "4. Issue show cause notice to violator",
                "5. Impose penalties or closure orders",
                "6. Monitor compliance and follow-up"
            ],
            "waste_management_violation": [
                "1. Issue notice to violator",
                "2. Conduct hearing within 7 days",
                "3. Impose penalty as per rules",
                "4. Ensure compliance and cleanup",
                "5. Repeat violations attract higher penalties"
            ],
            "ngt_case_filing": [
                "1. Prepare application with supporting documents",
                "2. Pay prescribed court fees",
                "3. File before appropriate NGT bench",
                "4. Serve notice to respondents",
                "5. Attend hearings and present case",
                "6. Comply with NGT orders"
            ]
        }

    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Environment (Protection) Act, 1986",
            "Water (Prevention and Control of Pollution) Act, 1974",
            "Air (Prevention and Control of Pollution) Act, 1981",
            "Solid Waste Management Rules, 2016",
            "Biomedical Waste Management Rules, 2016",
            "Plastic Waste Management Rules, 2016",
            "National Green Tribunal Act, 2010",
            "Public Health Act (State-specific)",
            "Food Safety and Standards Act, 2006",
            "Noise Pollution (Regulation and Control) Rules, 2000"
        ]

    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "littering": "Rs. 500 to Rs. 5,000",
            "waste_burning": "Rs. 5,000 to Rs. 25,000",
            "biomedical_waste_violation": "Rs. 25,000 to Rs. 1,00,000",
            "air_pollution": "Rs. 10,000 to Rs. 1,00,000 per day",
            "water_pollution": "Rs. 25,000 to Rs. 1,00,000 per day",
            "noise_pollution": "Rs. 1,000 to Rs. 5,000",
            "mosquito_breeding": "Rs. 500 to Rs. 2,000",
            "food_adulteration": "Rs. 25,000 to Rs. 5,00,000"
        }

    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []

    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze environmental and public health cases with BhimLaw AI professional format"""
        try:
            import json

            # First check if this query is within our domain
            if not self.is_query_in_domain(case_details, case_type):
                # Query is outside our domain, redirect to appropriate agent
                return self.get_redirect_response(case_details, case_type)

            # Query is in our domain, proceed with full analysis
            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Environmental Law / Public Health Law",
                    "jurisdiction": "State Pollution Control Board / Municipal Corporation",
                    "relevant_forum": [
                        "State Pollution Control Board",
                        "Municipal Health Department",
                        "National Green Tribunal (NGT)",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [],
                "landmark_judgments": [],
                "legal_remedy_path": [],
                "additional_insights": {},
                "professional_advice": {}
            }

            case_lower = case_details.lower()

            # Enhanced issue identification for environmental and public health cases
            if any(word in case_lower for word in ["garbage", "waste", "disposal", "pollution", "health hazard"]):
                analysis["applicable_laws"] = [
                    {
                        "law_rule": "Solid Waste Management Rules, 2016",
                        "section_clause": "Rule 15-20",
                        "description": "Segregation, collection, and disposal of solid waste by local authorities"
                    },
                    {
                        "law_rule": "Environment (Protection) Act, 1986",
                        "section_clause": "Section 15-17",
                        "description": "Prevention and control of environmental pollution"
                    },
                    {
                        "law_rule": "Water (Prevention and Control of Pollution) Act, 1974",
                        "section_clause": "Section 24-25",
                        "description": "Prohibition of discharge of pollutants into water bodies"
                    },
                    {
                        "law_rule": "Air (Prevention and Control of Pollution) Act, 1981",
                        "section_clause": "Section 21-22",
                        "description": "Control of air pollution and emission standards"
                    },
                    {
                        "law_rule": "National Green Tribunal Act, 2010",
                        "section_clause": "Section 14-15",
                        "description": "Environmental compensation and restoration orders"
                    }
                ]

                analysis["landmark_judgments"] = [
                    {
                        "case": "AI-Generated Landmark Judgments Not Available",
                        "citation": "Please retry query for comprehensive case citations",
                        "principle": "Landmark judgments with proper citations are generated by our AI legal expert"
                    }
                ]

                analysis["legal_remedy_path"] = [
                    {
                        "step": "Step 1: Complaint to Local Authority",
                        "action": "File complaint with Municipal Health Officer or Pollution Control Board with photographic evidence",
                        "time_limit": "Immediate action required for health hazards",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: Environmental Impact Assessment",
                        "action": "Request environmental audit and impact assessment from certified agency",
                        "time_limit": "Within 30 days of complaint",
                        "template_available": True
                    },
                    {
                        "step": "Step 3: Pollution Control Board Action",
                        "action": "Escalate to State Pollution Control Board for enforcement action and penalties",
                        "time_limit": "If no response within 15 days",
                        "template_available": True
                    },
                    {
                        "step": "Step 4: National Green Tribunal",
                        "action": "File application before NGT for environmental compensation and restoration",
                        "time_limit": "Within 6 months of environmental damage",
                        "template_available": True
                    }
                ]

                analysis["additional_insights"] = {
                    "bail_applicability": {
                        "applicable": False,
                        "reasoning": "Environmental matters are civil in nature unless criminal charges under Environment Protection Act"
                    },
                    "estimated_legal_fees": "₹15,000 - ₹1,00,000 (NGT proceedings generally cost-effective)",
                    "timeline_estimate": "2-8 months for NGT resolution, 6-18 months for High Court",
                    "success_probability": {
                        "percentage": "70-85%",
                        "reasoning": "Strong environmental laws and judicial precedents favor environmental protection"
                    }
                }

                analysis["professional_advice"] = {
                    "immediate_actions": [
                        "Document environmental damage with photographs and videos",
                        "Collect water/air quality test reports from certified labs",
                        "File complaint with local pollution control board",
                        "Gather evidence of health impacts on residents"
                    ],
                    "evidence_required": [
                        "Environmental impact assessment reports",
                        "Water/air quality test results",
                        "Medical reports showing health impacts",
                        "Photographs and videos of pollution",
                        "Expert witness statements from environmental scientists"
                    ],
                    "risk_factors": [
                        "Time-sensitive nature of environmental damage",
                        "Need for technical expert evidence",
                        "Potential high costs for environmental restoration",
                        "Corporate defendants with strong legal teams"
                    ]
                }

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in environmental health analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}
    
    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to Environmental & Public Health domain"""
        return [
            "pollution", "waste management", "garbage disposal", "biomedical waste",
            "mosquito breeding", "air pollution", "water pollution", "noise pollution",
            "environmental clearance", "ngt", "green tribunal", "solid waste",
            "hazardous waste", "effluent", "emission", "contamination",
            "environment", "health", "public health", "sanitation"
        ]

class EmployeeServiceMattersAgent(SpecializedLegalAgent):
    """
    Specialized agent for Employee & Service Matters
    Handles staff PF issues, promotions, pension cases, disciplinary actions
    """

    def __init__(self):
        super().__init__(
            "Employee & Service Matters Specialist",
            "Service Law, Employment Law, PF/Pension Rules, Disciplinary Proceedings"
        )

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "government_employee_rights": {
                "promotion_rights": {
                    "eligibility_criteria": "Minimum service period, performance standards, qualifications",
                    "dpc_process": "Departmental Promotion Committee evaluation and recommendations",
                    "seniority_principle": "Seniority-cum-fitness and fitness-cum-seniority",
                    "reservation_policy": "SC/ST/OBC reservation in promotions as per rules",
                    "appeal_mechanism": "Departmental appeal, CAT, High Court hierarchy"
                },
                "salary_increment": {
                    "annual_increment": "Automatic annual increment on due date",
                    "performance_linked": "Merit-based increments and performance pay",
                    "withholding_grounds": "Disciplinary proceedings, adverse remarks",
                    "restoration_procedure": "Appeal process for withheld increments"
                },
                "superior_harassment": {
                    "mala_fide_actions": "Arbitrary decisions, bias, personal vendetta",
                    "procedural_violations": "Non-compliance with service rules",
                    "remedial_measures": "Grievance redressal, transfer, disciplinary action",
                    "legal_protection": "Constitutional safeguards, service law protection"
                }
            },
            "provident_fund": {
                "pf_issues": {
                    "contribution_disputes": "Employee and employer contribution rates",
                    "withdrawal_problems": "PF withdrawal procedures and delays",
                    "transfer_issues": "PF account transfer between establishments",
                    "interest_calculation": "Annual interest rates and calculation methods"
                },
                "epf_act_provisions": {
                    "coverage": "Establishments with 20+ employees",
                    "contribution_rate": "12% employee + 12% employer",
                    "withdrawal_conditions": "Retirement, resignation, unemployment"
                }
            },
            "pension_matters": {
                "pension_calculation": {
                    "formula": "Average salary × years of service × pension factor",
                    "minimum_service": "10 years for pension eligibility",
                    "commutation": "Up to 40% of pension can be commuted"
                },
                "pension_disputes": {
                    "delayed_pension": "Pension processing delays",
                    "incorrect_calculation": "Wrong pension amount calculation",
                    "family_pension": "Spouse and dependent pension rights"
                }
            },
            "disciplinary_actions": {
                "types": {
                    "minor_penalties": ["Censure", "Withholding of increment", "Recovery from pay"],
                    "major_penalties": ["Reduction in rank", "Compulsory retirement", "Dismissal"]
                },
                "procedure": {
                    "charge_sheet": "Specific charges with supporting evidence",
                    "reply_time": "15-30 days for employee response",
                    "inquiry": "Departmental inquiry if charges denied",
                    "punishment": "Proportionate to misconduct"
                }
            },
            "service_disputes": {
                "promotion_issues": {
                    "seniority_disputes": "Seniority list challenges",
                    "reservation_matters": "SC/ST/OBC reservation in promotions",
                    "dpc_proceedings": "Departmental Promotion Committee decisions",
                    "bias_challenges": "Challenging biased or mala fide decisions"
                },
                "transfer_disputes": {
                    "arbitrary_transfers": "Transfers without proper justification",
                    "hardship_transfers": "Medical/family hardship cases",
                    "punishment_transfers": "Transfers as disguised punishment"
                }
            }
        }

    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "pf_grievance": [
                "1. File grievance with PF office",
                "2. Submit supporting documents",
                "3. Follow up within 30 days",
                "4. Escalate to Regional PF Commissioner",
                "5. File appeal with Central PF Commissioner",
                "6. Approach EPF Appellate Tribunal if needed"
            ],
            "disciplinary_inquiry": [
                "1. Issue charge sheet with specific allegations",
                "2. Allow 15 days for written reply",
                "3. Appoint inquiry officer if charges denied",
                "4. Conduct inquiry with evidence and witnesses",
                "5. Submit inquiry report with findings",
                "6. Issue show cause notice for punishment",
                "7. Pass final order after considering reply"
            ],
            "service_tribunal_case": [
                "1. File application within limitation period",
                "2. Pay prescribed court fees",
                "3. Serve notice to respondent department",
                "4. File counter-reply to department's response",
                "5. Attend hearings and present case",
                "6. Comply with tribunal orders"
            ]
        }

    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Employees' Provident Funds and Miscellaneous Provisions Act, 1952",
            "Payment of Gratuity Act, 1972",
            "Central Civil Services (Conduct) Rules, 1964",
            "Central Civil Services (Classification, Control and Appeal) Rules, 1965",
            "Central Civil Services (Pension) Rules, 2021",
            "Industrial Disputes Act, 1947",
            "Administrative Tribunals Act, 1985",
            "Right to Information Act, 2005",
            "Employees' State Insurance Act, 1948",
            "Contract Labour (Regulation and Abolition) Act, 1970"
        ]

    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "pf_non_compliance": "12% interest + penalty up to Rs. 25,000",
            "delayed_pf_payment": "Damage charges @ 12% per annum",
            "gratuity_non_payment": "Compensation up to 10 times gratuity amount",
            "wrongful_dismissal": "Reinstatement + back wages",
            "disciplinary_violation": "As per service rules - censure to dismissal",
            "pension_delay": "Interest @ 8% per annum on delayed amount"
        }

    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []

    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze employee and service matter cases with BhimLaw AI professional format"""
        try:
            import json

            # First check if this query is within our domain
            if not self.is_query_in_domain(case_details, case_type):
                # Query is outside our domain, redirect to appropriate agent
                return self.get_redirect_response(case_details, case_type)

            # Query is in our domain, proceed with full analysis
            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Service Law / Administrative Law",
                    "jurisdiction": "Central Government (India)",
                    "relevant_forum": [
                        "Departmental Appellate Authority",
                        "Central Administrative Tribunal (CAT)",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [],
                "landmark_judgments": [],
                "legal_remedy_path": [],
                "additional_insights": {},
                "professional_advice": {}
            }

            case_lower = case_details.lower()

            # Enhanced issue identification for government employee cases
            if any(word in case_lower for word in ["promotion", "salary hike", "increment", "superior blocking"]):
                analysis["applicable_laws"] = [
                    {
                        "law_rule": "Central Civil Services (Conduct) Rules, 1964",
                        "section_clause": "Rule 3(1)(ii)",
                        "description": "Obligation of public servant to act fairly and impartially"
                    },
                    {
                        "law_rule": "DoPT Office Memorandum (Promotion Guidelines)",
                        "section_clause": "2021 Revision",
                        "description": "Timelines, benchmarks, and conditions for promotion"
                    },
                    {
                        "law_rule": "CCS (CCA) Rules, 1965",
                        "section_clause": "Rule 14",
                        "description": "Grounds for disciplinary action against superiors if bias/misconduct proven"
                    },
                    {
                        "law_rule": "CAT Act, 1985",
                        "section_clause": "Section 19",
                        "description": "Jurisdiction for service disputes including promotion denial"
                    },
                    {
                        "law_rule": "RTI Act, 2005",
                        "section_clause": "Sections 6 & 7",
                        "description": "Right to obtain promotion criteria, DPC minutes, etc."
                    }
                ]

                analysis["landmark_judgments"] = [
                    {
                        "case": "AI-Generated Landmark Judgments Not Available",
                        "citation": "Please retry query for comprehensive case citations",
                        "principle": "Landmark judgments with proper citations are generated by our AI legal expert"
                    }
                ]

                analysis["legal_remedy_path"] = [
                    {
                        "step": "Step 1: Internal Representation",
                        "action": "File written grievance to Head of Department (HOD) or Appellate Authority",
                        "time_limit": "Preferably within 90 days of denial",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: RTI Filing",
                        "action": "File RTI to obtain DPC minutes, promotion policy, ACR/APAR reports, list of promoted employees",
                        "time_limit": "30 days response time",
                        "template_available": True
                    },
                    {
                        "step": "Step 3: Departmental Inquiry",
                        "action": "Demand departmental review if bias is established (trigger Rule 14 proceedings)",
                        "time_limit": "As per departmental rules",
                        "template_available": False
                    },
                    {
                        "step": "Step 4: File Before CAT",
                        "action": "File CAT Form 1 seeking promotion with retrospective effect, salary arrears with interest, disciplinary action against superior",
                        "time_limit": "Within limitation period",
                        "template_available": True
                    }
                ]

                analysis["additional_insights"] = {
                    "bail_applicability": {
                        "applicable": False,
                        "reasoning": "Not applicable – civil/service matter"
                    },
                    "estimated_legal_fees": "₹5,000 – ₹50,000 (varies by counsel and location)",
                    "timeline_estimate": "6–18 months for CAT + Departmental levels",
                    "success_probability": {
                        "percentage": "80%",
                        "reasoning": "With documented proof and proper APARs"
                    }
                }

                analysis["professional_advice"] = {
                    "immediate_actions": [
                        "Document all communications with superior",
                        "Collect performance records and ACRs",
                        "File RTI for transparency",
                        "Maintain detailed correspondence"
                    ],
                    "evidence_required": [
                        "Service records",
                        "Performance evaluations (APARs)",
                        "Correspondence with superior",
                        "Promotion policy documents",
                        "DPC minutes"
                    ],
                    "risk_factors": [
                        "Delay in filing may weaken case",
                        "Lack of documentary evidence",
                        "Departmental politics",
                        "Superior's counter-allegations"
                    ]
                }

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in employee service analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}

    def get_default_applicable_laws(self) -> List[Dict[str, str]]:
        """Get default applicable laws for Employee & Service Matters"""
        return [
            {
                "law_rule": "Central Civil Services (Conduct) Rules, 1964",
                "section_clause": "Rule 3(1)(ii)",
                "description": "Obligation of public servant to act fairly and impartially"
            },
            {
                "law_rule": "DoPT Office Memorandum (Promotion Guidelines)",
                "section_clause": "Current Revision",
                "description": "Timelines, benchmarks, and conditions for promotion"
            },
            {
                "law_rule": "CCS (CCA) Rules, 1965",
                "section_clause": "Rule 14",
                "description": "Grounds for disciplinary action against superiors if bias/misconduct proven"
            },
            {
                "law_rule": "CAT Act, 1985",
                "section_clause": "Section 19",
                "description": "Jurisdiction for service disputes including promotion denial"
            },
            {
                "law_rule": "RTI Act, 2005",
                "section_clause": "Sections 6 & 7",
                "description": "Right to obtain promotion criteria, DPC minutes, etc."
            }
        ]

    def get_default_landmark_judgments(self) -> List[Dict[str, str]]:
        """Get default landmark judgments for Employee & Service Matters"""
        return [
            {
                "case": "Union of India v. Hemraj Singh Chauhan",
                "citation": "(2010) 4 SCC 290",
                "principle": "Delay or denial in DPC violates Article 14 (equality)"
            },
            {
                "case": "Ajit Singh v. State of Punjab",
                "citation": "AIR 1999 SC 3471",
                "principle": "Eligible candidates cannot be ignored arbitrarily for promotion"
            },
            {
                "case": "R.K. Jain v. Union of India",
                "citation": "AIR 1993 SC 1769",
                "principle": "Disciplinary action against officers misusing authority"
            }
        ]

    def get_default_legal_remedy_path(self) -> List[Dict[str, Any]]:
        """Get default legal remedy path for Employee & Service Matters"""
        return [
            {
                "step": "Step 1: Internal Representation",
                "action": "File written grievance to Head of Department (HOD) or Appellate Authority",
                "time_limit": "Preferably within 90 days of denial",
                "template_available": True
            },
            {
                "step": "Step 2: RTI Filing",
                "action": "File RTI to obtain DPC minutes, promotion policy, ACR/APAR reports, list of promoted employees",
                "time_limit": "30 days response time",
                "template_available": True
            },
            {
                "step": "Step 3: Departmental Inquiry",
                "action": "Demand departmental review if bias is established (trigger Rule 14 proceedings)",
                "time_limit": "As per departmental rules",
                "template_available": False
            },
            {
                "step": "Step 4: File Before CAT",
                "action": "File CAT Form 1 seeking promotion with retrospective effect, salary arrears with interest, disciplinary action against superior",
                "time_limit": "Within limitation period",
                "template_available": True
            }
        ]

    def get_default_immediate_actions(self) -> List[str]:
        """Get default immediate actions for Employee & Service Matters"""
        return [
            "Document all communications with superior",
            "Collect performance records and ACRs",
            "File RTI for transparency",
            "Maintain detailed correspondence"
        ]

    def get_default_evidence_required(self) -> List[str]:
        """Get default evidence required for Employee & Service Matters"""
        return [
            "Service records",
            "Performance evaluations (APARs)",
            "Correspondence with superior",
            "Promotion policy documents",
            "DPC minutes"
        ]

    def get_default_risk_factors(self) -> List[str]:
        """Get default risk factors for Employee & Service Matters"""
        return [
            "Delay in filing may weaken case",
            "Lack of documentary evidence",
            "Departmental politics",
            "Superior's counter-allegations"
        ]

    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to Employee & Service Matters domain"""
        return [
            "pf", "provident fund", "pension", "service matters", "employment",
            "promotion", "disciplinary action", "service rules", "gratuity",
            "leave", "salary", "allowance", "increment", "dearness allowance",
            "medical reimbursement", "transfer", "posting", "seniority",
            "employee", "staff", "government employee", "central government",
            "state government", "service law", "employment law"
        ]

class RTITransparencyAgent(SpecializedLegalAgent):
    """
    Specialized agent for RTI & Transparency matters
    Handles RTI applications, deadlines, contempt petitions, compliance monitoring
    """

    def __init__(self):
        super().__init__(
            "RTI & Transparency Specialist",
            "Right to Information Law, Transparency Compliance, Information Disclosure"
        )

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "rti_provisions": {
                "information_rights": {
                    "scope": "All information held by public authorities",
                    "exemptions": "Security, privacy, commercial confidence",
                    "time_limit": "30 days for response (48 hours for life/liberty)",
                    "fees": "Rs. 10 per page for information"
                },
                "public_authority_duties": {
                    "proactive_disclosure": "Mandatory disclosure under Section 4",
                    "pio_appointment": "Public Information Officer designation",
                    "record_maintenance": "Proper cataloguing and indexing",
                    "annual_reports": "RTI implementation reports"
                }
            },
            "rti_procedures": {
                "application_process": {
                    "format": "Written application with specific information sought",
                    "fees": "Application fee + information cost",
                    "language": "Hindi, English, or local official language",
                    "submission": "Online or offline to concerned PIO"
                },
                "appeal_process": {
                    "first_appeal": "To appellate authority within 30 days",
                    "second_appeal": "To Information Commission within 90 days",
                    "grounds": "Non-response, inadequate response, excessive fees"
                }
            },
            "penalties": {
                "pio_penalties": {
                    "non_response": "Rs. 250 per day up to Rs. 25,000",
                    "malafide_denial": "Rs. 25,000 maximum penalty",
                    "frivolous_rejection": "Disciplinary action recommended"
                },
                "contempt_provisions": {
                    "non_compliance": "Contempt of Information Commission",
                    "willful_obstruction": "Criminal contempt proceedings",
                    "repeated_violations": "Departmental action against officers"
                }
            }
        }

    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "rti_application": [
                "1. Draft specific information request",
                "2. Pay prescribed application fee",
                "3. Submit to concerned Public Information Officer",
                "4. Obtain acknowledgment with registration number",
                "5. Follow up if no response within 30 days",
                "6. File first appeal if unsatisfied with response"
            ],
            "rti_appeal": [
                "1. File first appeal within 30 days to appellate authority",
                "2. Pay appeal fee if prescribed",
                "3. Await appellate authority decision",
                "4. File second appeal to Information Commission within 90 days",
                "5. Attend IC hearing and present case",
                "6. Comply with IC orders and directions"
            ],
            "contempt_petition": [
                "1. Document non-compliance with IC orders",
                "2. File contempt petition with Information Commission",
                "3. Serve notice to defaulting officer/authority",
                "4. Present evidence of willful non-compliance",
                "5. Seek appropriate penalty and compliance",
                "6. Monitor implementation of IC directions"
            ]
        }

    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Right to Information Act, 2005",
            "Central Information Commission Rules, 2005",
            "State Information Commission Rules (State-specific)",
            "Official Secrets Act, 1923",
            "Indian Evidence Act, 1872",
            "Code of Civil Procedure, 1908",
            "Contempt of Courts Act, 1971",
            "Public Records Act, 1993",
            "Archives Act (State-specific)",
            "Digital India Act (proposed)"
        ]

    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "pio_non_response": "Rs. 250 per day up to Rs. 25,000",
            "malafide_denial": "Rs. 25,000 maximum",
            "excessive_fees": "Refund + penalty up to Rs. 5,000",
            "delayed_response": "Rs. 250 per day of delay",
            "contempt_of_ic": "As per IC discretion",
            "frivolous_application": "Rs. 10,000 maximum penalty"
        }

    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []

    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze RTI and transparency cases with BhimLaw AI professional format"""
        try:
            import json

            # First check if this query is within our domain
            if not self.is_query_in_domain(case_details, case_type):
                # Query is outside our domain, redirect to appropriate agent
                return self.get_redirect_response(case_details, case_type)

            # Query is in our domain, proceed with full analysis
            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Right to Information Law / Transparency Law",
                    "jurisdiction": "Central/State Information Commission",
                    "relevant_forum": [
                        "Public Information Officer (PIO)",
                        "First Appellate Authority",
                        "State/Central Information Commission",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [
                    {
                        "law_rule": "Right to Information Act, 2005",
                        "section_clause": "Section 6-7",
                        "description": "Right to seek information and time limits for response"
                    },
                    {
                        "law_rule": "RTI Act, 2005",
                        "section_clause": "Section 18-19",
                        "description": "Powers of Information Commission and penalties"
                    },
                    {
                        "law_rule": "RTI Act, 2005",
                        "section_clause": "Section 8-9",
                        "description": "Exemptions from disclosure and partial disclosure"
                    }
                ],
                "landmark_judgments": [
                    {
                        "case": "Central Board of Secondary Education v. Aditya Bandopadhyay",
                        "citation": "AIR 2011 SC 1926",
                        "principle": "Larger public interest over individual privacy in information disclosure"
                    },
                    {
                        "case": "Institute of Chartered Accountants v. Shaunak H. Satya",
                        "citation": "AIR 2011 SC 3527",
                        "principle": "Substantial government funding makes body public authority under RTI"
                    }
                ],
                "legal_remedy_path": [
                    {
                        "step": "Step 1: RTI Application",
                        "action": "File RTI application with Public Information Officer (PIO) with specific information sought",
                        "time_limit": "PIO must respond within 30 days (48 hours for life/liberty matters)",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: First Appeal",
                        "action": "File first appeal with First Appellate Authority if no response or unsatisfactory response",
                        "time_limit": "Within 30 days of PIO response or 60 days if no response",
                        "template_available": True
                    },
                    {
                        "step": "Step 3: Second Appeal to Information Commission",
                        "action": "File second appeal with State/Central Information Commission",
                        "time_limit": "Within 90 days of First Appellate Authority decision",
                        "template_available": True
                    },
                    {
                        "step": "Step 4: High Court Writ Petition",
                        "action": "File writ petition under Article 226 challenging Information Commission order",
                        "time_limit": "Within limitation period from IC order",
                        "template_available": True
                    }
                ],
                "additional_insights": {
                    "bail_applicability": {
                        "applicable": False,
                        "reasoning": "RTI matters are civil/administrative, not criminal"
                    },
                    "estimated_legal_fees": "₹2,000 - ₹25,000 (RTI proceedings are generally cost-effective)",
                    "timeline_estimate": "3-12 months for Information Commission resolution",
                    "success_probability": {
                        "percentage": "75-90%",
                        "reasoning": "Strong RTI framework with clear timelines and penalties for non-compliance"
                    }
                },
                "professional_advice": {
                    "immediate_actions": [
                        "File RTI application with specific information sought",
                        "Maintain records of all correspondence with PIO",
                        "Follow up on statutory timelines",
                        "Document any delays or non-compliance"
                    ],
                    "evidence_required": [
                        "Copy of RTI application with acknowledgment",
                        "PIO response or proof of non-response",
                        "Correspondence with public authority",
                        "Proof of fee payment if applicable"
                    ],
                    "risk_factors": [
                        "Strict timelines for filing appeals",
                        "Information may be exempt under Section 8",
                        "Third party objections may delay process",
                        "Vague or broad RTI applications may be rejected"
                    ]
                }
            }

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in RTI transparency analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}

    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to RTI & Transparency domain"""
        return [
            "rti", "right to information", "information", "transparency",
            "disclosure", "public information", "information commission",
            "pio", "public information officer", "cic", "central information commission",
            "sic", "state information commission", "information request",
            "information denial", "information fee", "contempt petition",
            "transparency", "accountability", "government information",
            "public records", "official documents"
        ]

class InfrastructurePublicWorksAgent(SpecializedLegalAgent):
    """
    Specialized agent for Infrastructure & Public Works
    Handles road laying disputes, drainage damage claims, metro construction impacts
    """

    def __init__(self):
        super().__init__(
            "Infrastructure & Public Works Specialist",
            "Infrastructure Law, Public Works, Construction Disputes, Compensation Claims"
        )

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "road_construction": {
                "disputes": {
                    "land_acquisition": "Compensation for acquired land",
                    "construction_damage": "Damage to adjacent properties",
                    "traffic_disruption": "Business loss due to construction",
                    "quality_issues": "Substandard construction complaints"
                },
                "procedures": {
                    "tender_process": "Transparent bidding procedures",
                    "environmental_clearance": "EIA for major projects",
                    "public_consultation": "Stakeholder engagement requirements"
                }
            },
            "drainage_systems": {
                "damage_claims": {
                    "property_flooding": "Compensation for flood damage",
                    "structural_damage": "Building damage due to poor drainage",
                    "health_hazards": "Disease outbreak due to stagnant water"
                },
                "maintenance": {
                    "municipal_duty": "Regular cleaning and maintenance",
                    "citizen_complaints": "Grievance redressal mechanism",
                    "emergency_response": "Monsoon preparedness"
                }
            },
            "metro_construction": {
                "impact_assessment": {
                    "property_damage": "Vibration and structural damage",
                    "business_disruption": "Loss of access and customers",
                    "noise_pollution": "Construction noise complaints",
                    "dust_pollution": "Air quality deterioration"
                },
                "compensation": {
                    "temporary_loss": "Business interruption compensation",
                    "permanent_damage": "Property value depreciation",
                    "relocation_costs": "Temporary shifting expenses"
                }
            }
        }

    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "compensation_claim": [
                "1. Document damage with photographs and videos",
                "2. Get property valuation from approved valuers",
                "3. File claim with executing agency",
                "4. Submit supporting documents and evidence",
                "5. Attend joint inspection with officials",
                "6. Negotiate settlement or approach tribunal"
            ],
            "public_works_complaint": [
                "1. File complaint with concerned department",
                "2. Provide detailed description of issue",
                "3. Submit photographic evidence",
                "4. Follow up within prescribed time limits",
                "5. Escalate to higher authorities if needed",
                "6. Approach court for mandamus if required"
            ]
        }

    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Land Acquisition, Rehabilitation and Resettlement Act, 2013",
            "Public Works Department Code",
            "Metro Railways (Construction of Works) Act, 1978",
            "Environment (Protection) Act, 1986",
            "Water (Prevention and Control of Pollution) Act, 1974",
            "Municipal Corporation Acts (State-specific)",
            "Delhi Metro Railway (Operation and Maintenance) Act, 2002",
            "National Highways Act, 1956",
            "Indian Roads Congress Guidelines",
            "Central Public Works Department Code"
        ]

    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "construction_delay": "Penalty as per contract terms",
            "quality_defects": "Rectification at contractor cost",
            "environmental_violation": "Rs. 25,000 to Rs. 1,00,000",
            "safety_violations": "Work stoppage + penalty",
            "unauthorized_construction": "Demolition + fine",
            "damage_to_property": "Full compensation + interest"
        }

    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []

    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze infrastructure and public works cases with BhimLaw AI professional format"""
        try:
            import json

            # First check if this query is within our domain
            if not self.is_query_in_domain(case_details, case_type):
                # Query is outside our domain, redirect to appropriate agent
                return self.get_redirect_response(case_details, case_type)

            # Query is in our domain, proceed with full analysis
            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Infrastructure Law / Public Works Law",
                    "jurisdiction": "Municipal Corporation / State PWD",
                    "relevant_forum": [
                        "Municipal Corporation",
                        "Public Works Department",
                        "District Collector Office",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [
                    {
                        "law_rule": "Public Works Department Code",
                        "section_clause": "Section 10-15",
                        "description": "Procedures for public works and compensation for damages"
                    },
                    {
                        "law_rule": "Land Acquisition, Rehabilitation and Resettlement Act, 2013",
                        "section_clause": "Section 24-26",
                        "description": "Compensation for land acquisition and property damage"
                    },
                    {
                        "law_rule": "Municipal Corporation Act",
                        "section_clause": "Section 200-210",
                        "description": "Municipal powers for infrastructure development"
                    }
                ],
                "landmark_judgments": [
                    {
                        "case": "State of Maharashtra v. Narayan Sitaram Patil",
                        "citation": "AIR 2000 SC 2282",
                        "principle": "Compensation for property damage due to public works"
                    },
                    {
                        "case": "Kamala Devi v. State of Bihar",
                        "citation": "AIR 1992 SC 1486",
                        "principle": "Municipal duty to ensure safety standards in public works"
                    }
                ],
                "legal_remedy_path": [
                    {
                        "step": "Step 1: Damage Assessment",
                        "action": "Document property damage with photographs and get assessment from qualified engineer",
                        "time_limit": "Within 30 days of damage occurrence",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: Claim to Authority",
                        "action": "File compensation claim with Municipal Corporation/PWD with damage assessment",
                        "time_limit": "Within 60 days of damage",
                        "template_available": True
                    },
                    {
                        "step": "Step 3: Negotiation & Settlement",
                        "action": "Attend joint inspection and negotiate settlement with authorities",
                        "time_limit": "Within 90 days of claim filing",
                        "template_available": False
                    },
                    {
                        "step": "Step 4: Legal Proceedings",
                        "action": "File suit for compensation if settlement fails",
                        "time_limit": "Within limitation period",
                        "template_available": True
                    }
                ],
                "additional_insights": {
                    "bail_applicability": {
                        "applicable": False,
                        "reasoning": "Civil matter involving compensation claims"
                    },
                    "estimated_legal_fees": "₹10,000 - ₹75,000 (depending on claim amount)",
                    "timeline_estimate": "4-12 months for compensation settlement",
                    "success_probability": {
                        "percentage": "70%",
                        "reasoning": "With proper documentation and professional assessment"
                    }
                },
                "professional_advice": {
                    "immediate_actions": [
                        "Document property damage immediately with photographs",
                        "Get professional damage assessment from qualified engineer",
                        "File compensation claim with relevant authority",
                        "Preserve all evidence and correspondence"
                    ],
                    "evidence_required": [
                        "Property damage photographs and videos",
                        "Professional damage assessment report",
                        "Property ownership documents",
                        "Correspondence with authorities",
                        "Expert witness statements"
                    ],
                    "risk_factors": [
                        "Time limits for filing compensation claims",
                        "Need for professional damage assessment",
                        "Bureaucratic delays in processing claims",
                        "Disputed liability between multiple agencies"
                    ]
                }
            }

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in infrastructure works analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}

    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to Infrastructure & Public Works domain"""
        return [
            "infrastructure", "public works", "road", "drainage", "metro construction",
            "construction damage", "compensation", "road laying", "excavation",
            "utility lines", "water supply", "sewerage", "electricity lines",
            "gas pipeline", "construction impact", "property damage",
            "infrastructure development", "public utilities", "civic works",
            "municipal works", "government construction"
        ]

class EncroachmentLandAgent(SpecializedLegalAgent):
    """
    Specialized agent for Encroachment & Land matters
    Handles illegal encroachment cases, eviction proceedings, land disputes
    """

    def __init__(self):
        super().__init__(
            "Encroachment & Land Specialist",
            "Land Law, Encroachment Removal, Eviction Proceedings, Public Land Protection"
        )

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "encroachment_types": {
                "public_land": "Unauthorized occupation of government land",
                "road_encroachment": "Structures blocking public roads",
                "park_encroachment": "Illegal construction in public parks",
                "drain_encroachment": "Blocking of drainage systems"
            },
            "eviction_procedures": {
                "notice_period": "15-30 days as per local laws",
                "hearing_process": "Show cause hearing before eviction",
                "force_removal": "Police assistance for removal",
                "rehabilitation": "Alternative accommodation if applicable"
            },
            "land_acquisition": {
                "compensation": "Market value + solatium + interest",
                "rehabilitation": "R&R package for affected families",
                "consent": "70% consent for private companies"
            }
        }

    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "encroachment_removal": [
                "1. Survey and identify encroachment",
                "2. Issue removal notice with time limit",
                "3. Conduct hearing if objections filed",
                "4. Pass removal order after hearing",
                "5. Execute removal with police help",
                "6. Prevent re-encroachment"
            ],
            "land_dispute_resolution": [
                "1. Verify land records and ownership",
                "2. File suit for declaration of title",
                "3. Seek interim injunction if needed",
                "4. Present evidence and witnesses",
                "5. Obtain decree and execute",
                "6. Register decree with revenue authorities"
            ]
        }

    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Land Acquisition, Rehabilitation and Resettlement Act, 2013",
            "Public Premises (Eviction of Unauthorised Occupants) Act, 1971",
            "Delhi Land Reforms Act, 1954",
            "Urban Land (Ceiling and Regulation) Act, 1976",
            "Registration Act, 1908",
            "Transfer of Property Act, 1882",
            "Limitation Act, 2963",
            "Code of Civil Procedure, 1908",
            "Municipal Corporation Acts",
            "Delhi Development Act, 1957"
        ]

    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "illegal_encroachment": "Removal + fine Rs. 5,000 to Rs. 50,000",
            "repeat_encroachment": "Double penalty + imprisonment",
            "road_blocking": "Rs. 10,000 + daily penalty",
            "unauthorized_construction": "Demolition + Rs. 25,000 fine",
            "land_grabbing": "Criminal prosecution + eviction"
        }

    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []

    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze encroachment and land cases with BhimLaw AI professional format"""
        try:
            import json

            # First check if this query is within our domain
            if not self.is_query_in_domain(case_details, case_type):
                # Query is outside our domain, redirect to appropriate agent
                return self.get_redirect_response(case_details, case_type)

            # Query is in our domain, proceed with full analysis
            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Land Law / Administrative Law",
                    "jurisdiction": "District Collector / Revenue Department / High Court",
                    "relevant_forum": [
                        "District Collector Office",
                        "Revenue Court",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [],
                "landmark_judgments": [],
                "legal_remedy_path": [],
                "additional_insights": {},
                "professional_advice": {}
            }

            case_lower = case_details.lower()

            # Enhanced issue identification for encroachment and land cases
            if "encroachment" in case_lower or "illegal occupation" in case_lower or "eviction" in case_lower:
                analysis["applicable_laws"] = [
                    {
                        "law_rule": "Public Premises (Eviction of Unauthorised Occupants) Act, 1971",
                        "section_clause": "Section 4-6",
                        "description": "Procedure for eviction of unauthorized occupants from public premises"
                    },
                    {
                        "law_rule": "Land Acquisition Act, 2013",
                        "section_clause": "Section 24-30",
                        "description": "Compensation and rehabilitation provisions for land acquisition"
                    },
                    {
                        "law_rule": "Municipal Corporation Act",
                        "section_clause": "Section 343-350",
                        "description": "Powers for removal of encroachments on public land"
                    }
                ]

                analysis["landmark_judgments"] = [
                    {
                        "case": "AI-Generated Landmark Judgments Not Available",
                        "citation": "Please retry query for comprehensive case citations",
                        "principle": "Landmark judgments with proper citations are generated by our AI legal expert"
                    }
                ]

                analysis["legal_remedy_path"] = [
                    {
                        "step": "Step 1: Document Verification",
                        "action": "Collect all land documents, revenue records, and occupancy proof",
                        "time_limit": "Immediate - within 7 days of notice",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: Revenue Department Representation",
                        "action": "File representation to District Collector challenging eviction notice",
                        "time_limit": "Within 15 days of eviction notice",
                        "template_available": True
                    },
                    {
                        "step": "Step 3: High Court Petition",
                        "action": "File writ petition under Article 226 for protection against arbitrary eviction",
                        "time_limit": "Before eviction date or within limitation",
                        "template_available": True
                    }
                ]

                analysis["additional_insights"] = {
                    "bail_applicability": {
                        "applicable": False,
                        "reasoning": "Civil matter - eviction proceedings are administrative/civil in nature"
                    },
                    "estimated_legal_fees": "₹15,000 - ₹1,50,000 (varies by case complexity and court level)",
                    "timeline_estimate": "6-18 months for resolution through legal channels",
                    "success_probability": {
                        "percentage": "40-70%",
                        "reasoning": "Depends on legitimacy of occupation and procedural compliance by authorities"
                    }
                }

                analysis["professional_advice"] = {
                    "immediate_actions": [
                        "Collect all land ownership and occupancy documents",
                        "Document any procedural violations in eviction notice",
                        "Check for rehabilitation policy applicability",
                        "Engage land law specialist immediately"
                    ],
                    "evidence_required": [
                        "Revenue records and land documents",
                        "Proof of continuous occupation",
                        "Eviction notices and correspondence",
                        "Photographs of occupied land",
                        "Witness statements for occupation period"
                    ],
                    "risk_factors": [
                        "High eviction risk for clearly unauthorized occupation",
                        "Limited rehabilitation options in many cases",
                        "Time-sensitive nature of eviction proceedings",
                        "Administrative discretionary powers"
                    ]
                }

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in encroachment land analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}

    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to Encroachment & Land domain"""
        return [
            "encroachment", "land", "illegal occupation", "eviction", "land dispute",
            "unauthorized occupation", "public land", "government land",
            "land grabbing", "squatter", "trespassing", "land rights",
            "land acquisition", "land records", "revenue records",
            "settlement", "land title", "possession", "occupancy rights",
            "land revenue", "survey settlement"
        ]

class PublicNuisanceAgent(SpecializedLegalAgent):
    """
    Specialized agent for Public Nuisance matters
    Handles noise complaints, animal menace, illegal activities affecting public
    """

    def __init__(self):
        super().__init__(
            "Public Nuisance Specialist",
            "Public Nuisance Law, Noise Pollution, Animal Control, Public Order"
        )

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "noise_pollution": {
                "limits": {
                    "residential": "Day: 55 dB, Night: 45 dB",
                    "commercial": "Day: 65 dB, Night: 55 dB",
                    "industrial": "Day: 75 dB, Night: 70 dB",
                    "silence_zone": "Day: 50 dB, Night: 40 dB"
                },
                "sources": ["Traffic", "Construction", "Loudspeakers", "Industrial activities"],
                "enforcement": "Police and Pollution Control Board"
            },
            "animal_menace": {
                "stray_animals": "Municipal responsibility for control",
                "dangerous_animals": "Immediate removal and action",
                "cattle_menace": "Prohibition in urban areas",
                "dog_bite_cases": "Vaccination and compensation"
            },
            "public_order": {
                "illegal_activities": "Gambling, prostitution, drug peddling",
                "obstruction": "Blocking public ways and spaces",
                "antisocial_behavior": "Disturbing peace and tranquility"
            }
        }

    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "noise_complaint": [
                "1. Measure noise levels with calibrated equipment",
                "2. File complaint with police/pollution board",
                "3. Provide evidence of noise violation",
                "4. Request immediate action for abatement",
                "5. Follow up for compliance monitoring",
                "6. Seek court intervention if needed"
            ],
            "animal_control": [
                "1. Report to municipal animal control",
                "2. Document incidents with photographs",
                "3. Request immediate removal/control",
                "4. Follow up on sterilization programs",
                "5. Seek compensation for damages",
                "6. File police complaint if attacks occur"
            ]
        }

    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Noise Pollution (Regulation and Control) Rules, 2000",
            "Environment (Protection) Act, 1986",
            "Indian Penal Code, 1860 (Public Nuisance sections)",
            "Code of Criminal Procedure, 1973",
            "Prevention of Cruelty to Animals Act, 1960",
            "Municipal Corporation Acts",
            "Police Act (State-specific)",
            "Motor Vehicles Act, 1988",
            "Factories Act, 1948",
            "Public Premises (Eviction) Act, 1971"
        ]

    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "noise_violation": "Rs. 1,000 to Rs. 5,000",
            "loudspeaker_misuse": "Rs. 10,000 + equipment seizure",
            "animal_negligence": "Rs. 50 to Rs. 500",
            "public_nuisance": "Rs. 200 to Rs. 1,000",
            "obstruction": "Rs. 500 to Rs. 2,000",
            "repeat_violations": "Double penalty + possible imprisonment"
        }

    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []

    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze public nuisance cases with BhimLaw AI professional format"""
        try:
            import json

            # First check if this query is within our domain
            if not self.is_query_in_domain(case_details, case_type):
                # Query is outside our domain, redirect to appropriate agent
                return self.get_redirect_response(case_details, case_type)

            # Query is in our domain, proceed with full analysis
            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_raw": ai_analysis_raw,
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Public Nuisance Law / Environmental Law",
                    "jurisdiction": "Municipal Corporation / State Government",
                    "relevant_forum": [
                        "Municipal Corporation",
                        "Police Station",
                        "District Magistrate",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [],
                "landmark_judgments": [],
                "legal_remedy_path": [],
                "additional_insights": {
                    "bail_applicability": {"applicable": False, "reasoning": "Not applicable – civil/administrative matter"},
                    "estimated_legal_fees": "₹2,000 – ₹15,000 (varies by case complexity)",
                    "timeline_estimate": "2–6 months for resolution",
                    "success_probability": {"percentage": "85%", "reasoning": "With proper evidence and documentation"}
                },
                "professional_advice": {
                    "immediate_actions": [],
                    "evidence_required": [],
                    "risk_factors": []
                }
            }

            case_lower = case_details.lower()

            # Enhanced issue identification for public nuisance cases
            if "noise" in case_lower or "loudspeaker" in case_lower:
                analysis["applicable_laws"].extend([
                    {
                        "law_rule": "Noise Pollution (Regulation and Control) Rules",
                        "section_clause": "Rule 3-5",
                        "description": "Ambient noise standards and permissible limits for different areas"
                    },
                    {
                        "law_rule": "Environment Protection Act, 1986",
                        "section_clause": "Section 15",
                        "description": "Powers to control noise pollution and environmental violations"
                    },
                    {
                        "law_rule": "IPC Section 268",
                        "section_clause": "Section 268",
                        "description": "Public nuisance - unlawful obstruction or annoyance to public"
                    }
                ])
                # Landmark judgments will be generated by AI model
                analysis["legal_remedy_path"] = [
                    {
                        "step": "Step 1: File Police Complaint",
                        "action": "File complaint with local police station under IPC Section 268",
                        "time_limit": "Immediately",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: Sound Level Measurement",
                        "action": "Request authorized agency to measure sound levels",
                        "time_limit": "Within 7 days",
                        "template_available": False
                    },
                    {
                        "step": "Step 3: Pollution Control Board",
                        "action": "Approach State Pollution Control Board for noise violation",
                        "time_limit": "Within 15 days",
                        "template_available": True
                    },
                    {
                        "step": "Step 4: Magistrate Court",
                        "action": "File before District Magistrate if no action taken",
                        "time_limit": "Within 30 days",
                        "template_available": True
                    }
                ]
                analysis["professional_advice"]["immediate_actions"] = [
                    "Document noise levels with time stamps",
                    "Record audio/video evidence",
                    "File police complaint immediately",
                    "Gather witness statements"
                ]
                analysis["professional_advice"]["evidence_required"] = [
                    "Sound level measurements",
                    "Audio/video recordings",
                    "Police complaint copy",
                    "Witness statements",
                    "Medical reports if health affected"
                ]
                analysis["professional_advice"]["risk_factors"] = [
                    "Lack of proper evidence documentation",
                    "Delay in filing complaint",
                    "Non-cooperation from authorities",
                    "Repeat violations by offender"
                ]

            # Add default values if not set by specific case type
            if not analysis["applicable_laws"]:
                analysis["applicable_laws"] = [
                    {
                        "law_rule": "IPC Sections 268-294A",
                        "section_clause": "Section 268",
                        "description": "Public nuisance - unlawful obstruction or annoyance to public"
                    },
                    {
                        "law_rule": "Municipal Corporation Act",
                        "section_clause": "Various Sections",
                        "description": "Municipal regulations for public order and nuisance control"
                    }
                ]

            if not analysis["landmark_judgments"]:
                analysis["landmark_judgments"] = [
                    {
                        "case": "AI-Generated Landmark Judgments Not Available",
                        "citation": "Please retry query for comprehensive case citations",
                        "principle": "Landmark judgments with proper citations are generated by our AI legal expert"
                    }
                ]

            if not analysis["legal_remedy_path"]:
                analysis["legal_remedy_path"] = [
                    {
                        "step": "Step 1: File Complaint",
                        "action": "File complaint with local police or municipal authority",
                        "time_limit": "Immediately",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: Seek Administrative Action",
                        "action": "Request municipal corporation to take action",
                        "time_limit": "Within 15 days",
                        "template_available": True
                    }
                ]

            if not analysis["professional_advice"]["immediate_actions"]:
                analysis["professional_advice"]["immediate_actions"] = [
                    "Document the nuisance with evidence",
                    "File complaint with appropriate authority",
                    "Gather witness statements",
                    "Maintain incident records"
                ]

            if not analysis["professional_advice"]["evidence_required"]:
                analysis["professional_advice"]["evidence_required"] = [
                    "Photographs/videos of nuisance",
                    "Witness statements",
                    "Police complaint copy",
                    "Medical reports if applicable"
                ]

            if not analysis["professional_advice"]["risk_factors"]:
                analysis["professional_advice"]["risk_factors"] = [
                    "Insufficient evidence documentation",
                    "Delay in filing complaint",
                    "Non-cooperation from authorities",
                    "Repeat violations"
                ]

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in public nuisance analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}

    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to Public Nuisance domain"""
        return [
            "public nuisance", "noise", "noise pollution", "animal menace",
            "stray animals", "dogs", "cattle", "illegal activities",
            "disturbance", "public order", "nuisance", "harassment",
            "loud music", "construction noise", "traffic noise",
            "air pollution", "smoke", "dust", "odor", "smell",
            "public peace", "community disturbance"
        ]

















class LicensingTradeRegulationAgent(SpecializedLegalAgent):
    """
    Specialized agent for Licensing & Trade Regulation
    Handles unlicensed vendor cases, trade license violations, illegal hoarding complaints
    """

    def __init__(self):
        super().__init__(
            "Licensing & Trade Regulation Specialist",
            "Trade License Law, Commercial Regulations, Vendor Management, Business Compliance"
        )

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "trade_licensing": {
                "shop_establishment": {
                    "definition": "Registration under Shop & Establishment Act for commercial activities",
                    "applicable_sections": ["Shop & Establishment Act", "Municipal Corporation Act"],
                    "penalties": "Fine up to Rs. 25,000 for non-registration",
                    "procedure": ["Application submission", "Document verification", "Inspection", "License issuance"]
                },
                "food_license": {
                    "types": ["FSSAI Basic", "FSSAI State", "FSSAI Central"],
                    "requirements": ["Food safety training", "Premises inspection", "Documentation"],
                    "penalties": "Rs. 25,000 to Rs. 5,00,000 for violations"
                }
            },
            "vendor_management": {
                "street_vendors": {
                    "rights": ["Right to livelihood", "Designated vending zones", "Protection from harassment"],
                    "regulations": ["Vending certificate", "Health certificate", "Identity card"],
                    "violations": ["Unauthorized vending", "Obstruction", "Unhygienic practices"]
                }
            }
        }

    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "trade_license_application": [
                "1. Prepare required documents (ID, address proof, business plan)",
                "2. Submit application to licensing authority",
                "3. Pay prescribed fees",
                "4. Undergo premises inspection",
                "5. Obtain clearances (fire, pollution, health)",
                "6. Receive license certificate"
            ],
            "license_violation_complaint": [
                "1. Document the violation with evidence",
                "2. File complaint with licensing authority",
                "3. Request inspection and verification",
                "4. Seek penalty imposition on violator",
                "5. Follow up for compliance enforcement"
            ]
        }

    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Shop & Establishment Act",
            "Food Safety and Standards Act, 2006",
            "Municipal Corporation Act",
            "Street Vendors Act, 2014",
            "Weights and Measures Act, 1976",
            "Consumer Protection Act, 2019",
            "Goods and Services Tax Act, 2017",
            "Trade Marks Act, 1999",
            "Competition Act, 2002",
            "Foreign Exchange Management Act, 1999"
        ]

    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "unlicensed_trade": "Rs. 5,000 to Rs. 25,000",
            "food_safety_violation": "Rs. 25,000 to Rs. 5,00,000",
            "vendor_violation": "Rs. 500 to Rs. 2,000",
            "weight_measure_violation": "Rs. 2,000 to Rs. 25,000",
            "repeat_violations": "Double penalty + license cancellation"
        }

    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []

    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze licensing and trade regulation cases with BhimLaw AI professional format"""
        try:
            import json

            # First check if this query is within our domain
            if not self.is_query_in_domain(case_details, case_type):
                # Query is outside our domain, redirect to appropriate agent
                return self.get_redirect_response(case_details, case_type)

            # Query is in our domain, proceed with full analysis
            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_raw": ai_analysis_raw,
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Trade License Law / Commercial Regulations",
                    "jurisdiction": "Municipal Corporation / State Government",
                    "relevant_forum": [
                        "Municipal Corporation",
                        "Licensing Authority",
                        "District Collector Office",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [
                    {
                        "law_rule": "Shop & Establishment Act",
                        "section_clause": "Section 5-10",
                        "description": "Registration requirements for commercial establishments"
                    },
                    {
                        "law_rule": "Food Safety and Standards Act, 2006",
                        "section_clause": "Section 31-32",
                        "description": "Licensing requirements for food business operators"
                    },
                    {
                        "law_rule": "Street Vendors Act, 2014",
                        "section_clause": "Section 3-5",
                        "description": "Rights and regulations for street vendors"
                    }
                ],
                "landmark_judgments": [
                    {
                        "case": "Sodan Singh v. NDMC",
                        "citation": "AIR 1989 SC 1988",
                        "principle": "Right to carry on trade and business under Article 19(1)(g)"
                    },
                    {
                        "case": "Olga Tellis v. Bombay Municipal Corporation",
                        "citation": "AIR 1986 SC 180",
                        "principle": "Right to livelihood is part of right to life under Article 21"
                    }
                ],
                "legal_remedy_path": [
                    {
                        "step": "Step 1: License Application",
                        "action": "Apply for appropriate trade license with required documents",
                        "time_limit": "Within 30 days",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: Compliance Check",
                        "action": "Ensure compliance with all regulatory requirements",
                        "time_limit": "Before starting business",
                        "template_available": False
                    },
                    {
                        "step": "Step 3: Appeal Process",
                        "action": "Appeal to higher authority if license denied",
                        "time_limit": "Within 30 days of rejection",
                        "template_available": True
                    }
                ],
                "additional_insights": {
                    "bail_applicability": {"applicable": False, "reasoning": "Not applicable – civil/administrative matter"},
                    "estimated_legal_fees": "₹3,000 – ₹20,000 (varies by case complexity)",
                    "timeline_estimate": "1–3 months for license approval",
                    "success_probability": {"percentage": "90%", "reasoning": "With proper documentation and compliance"}
                },
                "professional_advice": {
                    "immediate_actions": [
                        "Gather all required documents",
                        "Check compliance requirements",
                        "Submit license application",
                        "Maintain proper records"
                    ],
                    "evidence_required": [
                        "Business registration documents",
                        "Identity and address proofs",
                        "Premises ownership/rental documents",
                        "Clearance certificates",
                        "Fee payment receipts"
                    ],
                    "risk_factors": [
                        "Incomplete documentation",
                        "Non-compliance with regulations",
                        "Delay in application submission",
                        "Lack of required clearances"
                    ]
                }
            }

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in licensing trade regulation analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}

    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to Licensing & Trade Regulation domain"""
        return [
            "license", "trade license", "business license", "shop establishment",
            "food license", "vendor", "street vendor", "unlicensed",
            "trade regulation", "commercial", "business", "shop",
            "establishment", "fssai", "trade", "commerce", "vendor license",
            "hawker", "illegal business", "unauthorized trade",
            "licensing authority", "municipal license", "business permit"
        ]

class SlumClearanceResettlementAgent(SpecializedLegalAgent):
    """
    Specialized agent for Slum Clearance & Resettlement
    Handles slum rehabilitation, resettlement rights, housing schemes
    """

    def __init__(self):
        super().__init__(
            "Slum Clearance & Resettlement Specialist",
            "Slum Rehabilitation Law, Resettlement Rights, Housing Schemes, Urban Development"
        )

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "slum_rehabilitation": {
                "eligibility_criteria": {
                    "cutoff_date": "Survey date as per government notification",
                    "proof_requirements": ["Ration card", "Voter ID", "Electricity bill", "School certificate"],
                    "minimum_residence": "Continuous residence since cutoff date"
                },
                "rehabilitation_rights": {
                    "in_situ_rehabilitation": "Right to housing at same location",
                    "alternative_accommodation": "Equivalent housing at alternative site",
                    "compensation": "Monetary compensation as per policy"
                }
            },
            "housing_schemes": {
                "pradhan_mantri_awas_yojana": {
                    "eligibility": ["EWS/LIG families", "No pucca house ownership", "Income criteria"],
                    "benefits": ["Interest subsidy", "Direct assistance", "Affordable housing"]
                },
                "rajiv_awas_yojana": {
                    "objective": "Slum-free India",
                    "components": ["Slum redevelopment", "Affordable housing", "Basic services"]
                }
            }
        }

    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "rehabilitation_claim": [
                "1. Verify eligibility as per survey records",
                "2. Submit application with required documents",
                "3. Attend verification process",
                "4. Await allotment of rehabilitation unit",
                "5. Complete formalities for possession",
                "6. Vacate original premises as per schedule"
            ],
            "resettlement_grievance": [
                "1. File grievance with rehabilitation authority",
                "2. Present evidence of eligibility",
                "3. Request review of rejection/exclusion",
                "4. Appeal to higher authority if needed",
                "5. Approach court for legal remedy"
            ]
        }

    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Slum Areas (Improvement and Clearance) Act, 1956",
            "Urban Land (Ceiling and Regulation) Act, 1976",
            "Land Acquisition, Rehabilitation and Resettlement Act, 2013",
            "Right to Fair Compensation and Transparency in Land Acquisition Act, 2013",
            "Delhi Development Act, 1957",
            "Maharashtra Slum Areas Act, 1971",
            "Tamil Nadu Slum Areas Act, 1971",
            "Housing and Urban Development Corporation Act, 1970",
            "National Housing Bank Act, 1987",
            "Real Estate (Regulation and Development) Act, 2016"
        ]

    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "unauthorized_occupation": "Eviction and penalty as per local laws",
            "false_documentation": "Rs. 10,000 to Rs. 50,000 + disqualification",
            "non_compliance": "Forfeiture of rehabilitation rights",
            "illegal_sale": "Rs. 25,000 to Rs. 1,00,000 + cancellation"
        }

    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []

    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze slum clearance and resettlement cases with BhimLaw AI professional format"""
        try:
            import json

            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_raw": ai_analysis_raw,
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Slum Rehabilitation Law / Urban Development Law",
                    "jurisdiction": "State Government / Urban Development Authority",
                    "relevant_forum": [
                        "Slum Rehabilitation Authority",
                        "Urban Development Department",
                        "District Collector Office",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [
                    {
                        "law_rule": "Slum Areas (Improvement and Clearance) Act, 1956",
                        "section_clause": "Section 3-5",
                        "description": "Powers for slum improvement and clearance"
                    },
                    {
                        "law_rule": "Land Acquisition, Rehabilitation and Resettlement Act, 2013",
                        "section_clause": "Chapter III",
                        "description": "Rehabilitation and resettlement entitlements"
                    }
                ],
                "landmark_judgments": [
                    {
                        "case": "Olga Tellis v. Bombay Municipal Corporation",
                        "citation": "AIR 1986 SC 180",
                        "principle": "Right to livelihood and shelter under Article 21"
                    },
                    {
                        "case": "Ahmedabad Municipal Corporation v. Nawab Khan",
                        "citation": "AIR 1997 SC 152",
                        "principle": "Reasonable notice and alternative accommodation before eviction"
                    }
                ],
                "legal_remedy_path": [
                    {
                        "step": "Step 1: Eligibility Verification",
                        "action": "Verify eligibility as per survey records and cutoff date",
                        "time_limit": "As per notification",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: Documentation",
                        "action": "Submit complete application with required documents",
                        "time_limit": "Within specified period",
                        "template_available": True
                    },
                    {
                        "step": "Step 3: Grievance Redressal",
                        "action": "File grievance if excluded or rejected",
                        "time_limit": "Within 30 days",
                        "template_available": True
                    }
                ],
                "additional_insights": {
                    "bail_applicability": {"applicable": False, "reasoning": "Not applicable – civil/administrative matter"},
                    "estimated_legal_fees": "₹5,000 – ₹25,000 (varies by case complexity)",
                    "timeline_estimate": "6 months – 2 years for rehabilitation",
                    "success_probability": {"percentage": "75%", "reasoning": "With proper documentation and eligibility proof"}
                },
                "professional_advice": {
                    "immediate_actions": [
                        "Collect all eligibility documents",
                        "Verify survey records",
                        "Submit rehabilitation application",
                        "Maintain residence proof"
                    ],
                    "evidence_required": [
                        "Survey records and cutoff date proof",
                        "Continuous residence documents",
                        "Identity and family documents",
                        "Utility bills and ration card",
                        "School certificates for children"
                    ],
                    "risk_factors": [
                        "Lack of proper documentation",
                        "Missing cutoff date eligibility",
                        "Incomplete application",
                        "Non-cooperation with authorities"
                    ]
                }
            }

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in slum clearance resettlement analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}

    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to Slum Clearance & Resettlement domain"""
        return [
            "slum", "slum clearance", "resettlement", "rehabilitation",
            "slum dwellers", "housing", "housing scheme", "slum redevelopment",
            "in-situ rehabilitation", "alternative accommodation",
            "pradhan mantri awas yojana", "rajiv awas yojana",
            "cutoff date", "survey", "slum survey", "eligibility",
            "housing rights", "urban development", "slum free"
        ]

class WaterDrainageAgent(SpecializedLegalAgent):
    """
    Specialized agent for Water & Drainage
    Handles water supply issues, drainage problems, sewerage complaints
    """

    def __init__(self):
        super().__init__(
            "Water & Drainage Specialist",
            "Water Supply Law, Drainage Systems, Sewerage Management, Municipal Services"
        )

    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        return {
            "water_supply": {
                "rights_and_obligations": {
                    "right_to_water": "Fundamental right under Article 21",
                    "municipal_duty": "Provision of adequate water supply",
                    "quality_standards": "As per Bureau of Indian Standards"
                },
                "service_issues": {
                    "inadequate_supply": "Less than prescribed minimum per capita",
                    "quality_issues": "Contaminated or unsafe water",
                    "irregular_supply": "Inconsistent timing and pressure"
                }
            },
            "drainage_systems": {
                "storm_water_drainage": {
                    "design_standards": "As per municipal engineering standards",
                    "maintenance_responsibility": "Municipal corporation",
                    "citizen_obligations": "No obstruction or dumping"
                },
                "sewerage_system": {
                    "connection_rights": "Mandatory connection in sewered areas",
                    "treatment_standards": "As per pollution control norms",
                    "user_charges": "As per municipal tariff"
                }
            }
        }

    def _initialize_procedures(self) -> Dict[str, List[str]]:
        return {
            "water_supply_complaint": [
                "1. File complaint with water supply department",
                "2. Document the issue with photographs/videos",
                "3. Request inspection and rectification",
                "4. Escalate to higher authority if no response",
                "5. Approach consumer forum for compensation",
                "6. File writ petition if fundamental right violated"
            ],
            "drainage_blockage_complaint": [
                "1. Report to municipal health department",
                "2. Document health hazards and property damage",
                "3. Request immediate cleaning and repair",
                "4. Seek compensation for damages",
                "5. File public interest litigation if widespread"
            ]
        }

    def _initialize_relevant_acts(self) -> List[str]:
        return [
            "Water (Prevention and Control of Pollution) Act, 1974",
            "Environment (Protection) Act, 1986",
            "Municipal Corporation Acts",
            "Public Health Engineering Department Rules",
            "Indian Easements Act, 1882",
            "Consumer Protection Act, 2019",
            "Right to Information Act, 2005",
            "National Water Policy, 2012",
            "Swachh Bharat Mission Guidelines",
            "Jal Jeevan Mission Guidelines"
        ]

    def _initialize_penalties(self) -> Dict[str, str]:
        return {
            "water_pollution": "Rs. 10,000 to Rs. 1,00,000",
            "unauthorized_connection": "Rs. 5,000 to Rs. 25,000",
            "drainage_obstruction": "Rs. 1,000 to Rs. 10,000",
            "sewerage_violation": "Rs. 2,000 to Rs. 50,000"
        }

    def _initialize_precedents(self) -> List[Dict[str, str]]:
        """Precedents are now generated dynamically by AI model"""
        return []

    def analyze_case(self, case_details: str, case_type: str) -> Dict[str, Any]:
        """Analyze water and drainage cases with BhimLaw AI professional format"""
        try:
            import json

            # Get AI-powered analysis using the new format
            ai_analysis_raw = self.call_nvidia_api(case_details, case_type)

            # Try to parse JSON response
            try:
                ai_analysis_json = json.loads(ai_analysis_raw)
                ai_analysis_parsed = True

                # Return the AI analysis directly if it's in the correct format
                if "legal_classification" in ai_analysis_json and "applicable_laws" in ai_analysis_json:
                    # Format the response in the user's preferred style
                    formatted_response = self.format_response_with_emojis(ai_analysis_json, case_details, case_type)
                    self.update_metrics(True)
                    return formatted_response

            except json.JSONDecodeError:
                ai_analysis_parsed = False

            # Fallback: Create structured response if AI didn't return proper format
            analysis = {
                "case_type": case_type,
                "specialization": self.specialization,
                "agent_name": self.agent_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_analysis_raw": ai_analysis_raw,
                "ai_analysis_parsed": ai_analysis_parsed,
                "legal_classification": {
                    "domain": "Water Supply Law / Municipal Services Law",
                    "jurisdiction": "Municipal Corporation / State Government",
                    "relevant_forum": [
                        "Municipal Corporation",
                        "Water Supply Department",
                        "Pollution Control Board",
                        "Consumer Forum",
                        "High Court (under Article 226)"
                    ]
                },
                "applicable_laws": [
                    {
                        "law_rule": "Water (Prevention and Control of Pollution) Act, 1974",
                        "section_clause": "Section 24-25",
                        "description": "Prevention of water pollution and quality standards"
                    },
                    {
                        "law_rule": "Municipal Corporation Act",
                        "section_clause": "Various Sections",
                        "description": "Municipal duty to provide water supply and drainage"
                    },
                    {
                        "law_rule": "Consumer Protection Act, 2019",
                        "section_clause": "Section 2(7)",
                        "description": "Water supply as service under consumer protection"
                    }
                ],
                "landmark_judgments": [
                    {
                        "case": "Subhash Kumar v. State of Bihar",
                        "citation": "AIR 1991 SC 420",
                        "principle": "Right to clean water as part of right to life under Article 21"
                    },
                    {
                        "case": "A.P. Pollution Control Board v. M.V. Nayudu",
                        "citation": "AIR 1999 SC 812",
                        "principle": "Polluter pays principle and precautionary principle"
                    }
                ],
                "legal_remedy_path": [
                    {
                        "step": "Step 1: Complaint to Department",
                        "action": "File complaint with water supply/drainage department",
                        "time_limit": "Immediately",
                        "template_available": True
                    },
                    {
                        "step": "Step 2: Consumer Forum",
                        "action": "Approach consumer forum for service deficiency",
                        "time_limit": "Within 2 years",
                        "template_available": True
                    },
                    {
                        "step": "Step 3: Writ Petition",
                        "action": "File writ petition for fundamental right violation",
                        "time_limit": "Within limitation",
                        "template_available": True
                    }
                ],
                "additional_insights": {
                    "bail_applicability": {"applicable": False, "reasoning": "Not applicable – civil/service matter"},
                    "estimated_legal_fees": "₹3,000 – ₹15,000 (varies by forum)",
                    "timeline_estimate": "2–8 months for resolution",
                    "success_probability": {"percentage": "80%", "reasoning": "Strong legal framework for water rights"}
                },
                "professional_advice": {
                    "immediate_actions": [
                        "Document water/drainage issues",
                        "File complaint with department",
                        "Collect evidence of health hazards",
                        "Gather witness statements"
                    ],
                    "evidence_required": [
                        "Photographs/videos of issues",
                        "Water quality test reports",
                        "Medical reports if health affected",
                        "Complaint acknowledgments",
                        "Property damage evidence"
                    ],
                    "risk_factors": [
                        "Health hazards from contaminated water",
                        "Property damage from drainage issues",
                        "Delay in complaint filing",
                        "Lack of proper documentation"
                    ]
                }
            }

            # Format the response in the user's preferred style
            formatted_response = self.format_response_with_emojis(analysis, case_details, case_type)
            self.update_metrics(True)
            return formatted_response

        except Exception as e:
            logger.error(f"Error in water drainage analysis: {str(e)}")
            self.update_metrics(False)
            return {"error": str(e), "agent": self.agent_name}

    def get_domain_keywords(self) -> List[str]:
        """Get keywords specific to Water & Drainage domain"""
        return [
            "water", "water supply", "drainage", "sewerage", "water quality",
            "water pollution", "drainage blockage", "water shortage",
            "water connection", "sewerage connection", "water bill",
            "drainage system", "storm water", "water treatment",
            "water contamination", "drainage overflow", "water pressure",
            "municipal water", "water department", "drainage complaint"
        ]
