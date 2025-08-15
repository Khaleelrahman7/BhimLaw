"""
BhimLaw AI - Specialized Agent Router and Manager
Prototype VII - Intelligent Agent Selection and Routing System

This module handles intelligent routing of legal queries to appropriate specialized agents
based on case type analysis and domain expertise matching.
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from specialized_agents import (
    SpecializedLegalAgent,
    PropertyBuildingViolationsAgent,
    EnvironmentalPublicHealthAgent,
    EmployeeServiceMattersAgent,
    RTITransparencyAgent,
    InfrastructurePublicWorksAgent,
    EncroachmentLandAgent,
    LicensingTradeRegulationAgent,
    SlumClearanceResettlementAgent,
    WaterDrainageAgent,
    PublicNuisanceAgent,
    CaseCategory
)

# Configure logging
logger = logging.getLogger("BhimLaw_Agent_Router")

class AgentRouter:
    """
    Intelligent routing system for specialized legal agents
    Analyzes queries and routes to most appropriate specialized agent
    """
    
    def __init__(self):
        self.agents = {}
        self.routing_keywords = {}
        self.case_statistics = {}
        self.initialize_agents()
        self.initialize_routing_keywords()
        logger.info("Agent Router initialized with specialized agents")
    
    def initialize_agents(self):
        """Initialize all specialized agents"""
        try:
            # Initialize specialized agents
            self.agents = {
                CaseCategory.PROPERTY_VIOLATIONS: PropertyBuildingViolationsAgent(),
                CaseCategory.ENVIRONMENTAL_HEALTH: EnvironmentalPublicHealthAgent(),
                CaseCategory.EMPLOYEE_SERVICES: EmployeeServiceMattersAgent(),
                CaseCategory.RTI_TRANSPARENCY: RTITransparencyAgent(),
                CaseCategory.INFRASTRUCTURE_WORKS: InfrastructurePublicWorksAgent(),
                CaseCategory.ENCROACHMENT_LAND: EncroachmentLandAgent(),
                CaseCategory.LICENSING_TRADE: LicensingTradeRegulationAgent(),
                CaseCategory.SLUM_CLEARANCE: SlumClearanceResettlementAgent(),
                CaseCategory.WATER_DRAINAGE: WaterDrainageAgent(),
                CaseCategory.PUBLIC_NUISANCE: PublicNuisanceAgent()
            }
            
            # Initialize case statistics
            for category in self.agents.keys():
                self.case_statistics[category] = {
                    "total_cases": 0,
                    "successful_cases": 0,
                    "average_processing_time": 0.0,
                    "success_rate": 0.0
                }
            
            logger.info(f"Initialized {len(self.agents)} specialized agents")
            
        except Exception as e:
            logger.error(f"Error initializing agents: {str(e)}")
            raise
    
    def initialize_routing_keywords(self):
        """Initialize keyword mapping for intelligent routing"""
        self.routing_keywords = {
            CaseCategory.PROPERTY_VIOLATIONS: [
                "unauthorized construction", "building violation", "property tax",
                "illegal construction", "demolition", "building permit", "zoning",
                "setback violation", "height violation", "fsr violation", "far violation",
                "building plan", "construction without approval", "municipal violation"
            ],
            CaseCategory.ENVIRONMENTAL_HEALTH: [
                "pollution", "waste management", "garbage disposal", "biomedical waste",
                "mosquito breeding", "air pollution", "water pollution", "noise pollution",
                "environmental clearance", "ngt", "green tribunal", "solid waste",
                "hazardous waste", "effluent", "emission", "contamination"
            ],
            CaseCategory.EMPLOYEE_SERVICES: [
                "provident fund", "pf", "epf", "pension", "gratuity", "disciplinary action",
                "service matter", "promotion", "seniority", "transfer", "misconduct",
                "charge sheet", "departmental inquiry", "service rules", "employment"
            ],
            CaseCategory.RTI_TRANSPARENCY: [
                "rti", "right to information", "information disclosure", "transparency",
                "public information officer", "pio", "information commission",
                "appeal", "contempt", "non-disclosure", "information request"
            ],
            CaseCategory.INFRASTRUCTURE_WORKS: [
                "road construction", "infrastructure", "metro construction", "drainage damage",
                "public works", "construction dispute", "compensation claim", "road laying",
                "infrastructure damage", "construction impact", "public project"
            ],
            CaseCategory.ENCROACHMENT_LAND: [
                "encroachment", "illegal occupation", "land dispute", "eviction",
                "unauthorized occupation", "land grabbing", "title dispute", "possession",
                "trespass", "land acquisition", "public land"
            ],
            CaseCategory.LICENSING_TRADE: [
                "trade license", "unlicensed", "vendor", "hawker", "street vending",
                "business license", "shop license", "commercial license", "hoarding",
                "signage", "advertising", "unlicensed trading", "license violation"
            ],
            CaseCategory.SLUM_CLEARANCE: [
                "slum", "slum clearance", "resettlement", "rehabilitation", "eviction",
                "slum dweller", "slum rehabilitation", "housing rights", "displacement",
                "relocation", "slum improvement", "urban development"
            ],
            CaseCategory.WATER_DRAINAGE: [
                "water supply", "drainage", "sewer", "water connection", "water quality",
                "drinking water", "water contamination", "drainage blockage", "flood",
                "stormwater", "sewerage", "water board", "water dispute"
            ],
            CaseCategory.PUBLIC_NUISANCE: [
                "noise complaint", "animal menace", "public nuisance", "disturbance",
                "stray animals", "noise pollution", "loudspeaker", "antisocial behavior",
                "obstruction", "public order", "nuisance activities"
            ]
        }
    
    def analyze_query_keywords(self, query: str) -> Dict[CaseCategory, float]:
        """Analyze query and calculate relevance scores for each agent category"""
        query_lower = query.lower()
        scores = {}
        
        for category, keywords in self.routing_keywords.items():
            score = 0.0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword in query_lower:
                    # Weight longer keywords more heavily
                    weight = len(keyword.split()) * 1.5
                    score += weight
                    matched_keywords.append(keyword)
            
            # Normalize score by query length
            if len(query_lower.split()) > 0:
                scores[category] = score / len(query_lower.split())
            else:
                scores[category] = 0.0
                
            logger.debug(f"{category}: score={scores[category]:.2f}, keywords={matched_keywords}")
        
        return scores
    
    def select_best_agent(self, query: str, case_type: str = None) -> Tuple[CaseCategory, SpecializedLegalAgent, float]:
        """Select the most appropriate agent based on query analysis"""
        try:
            # Analyze query keywords
            keyword_scores = self.analyze_query_keywords(query)
            
            # Consider case_type if provided - direct mapping first
            if case_type:
                case_type_lower = case_type.lower()
                # Direct mapping to category
                for category in self.routing_keywords.keys():
                    if category.value.lower() == case_type_lower:
                        keyword_scores[category] += 10.0  # High boost for direct match
                        logger.info(f"Direct case_type match: {case_type} -> {category}")
                        break
                else:
                    # Fallback to keyword matching in case_type
                    for category, keywords in self.routing_keywords.items():
                        if any(keyword in case_type_lower for keyword in keywords):
                            keyword_scores[category] += 2.0  # Boost score for keyword match
            
            # Find best matching agent
            best_category = max(keyword_scores.items(), key=lambda x: x[1])
            category, confidence_score = best_category
            
            if confidence_score > 0:
                selected_agent = self.agents[category]
                logger.info(f"Selected agent: {selected_agent.agent_name} (confidence: {confidence_score:.2f})")
                return category, selected_agent, confidence_score
            else:
                # Default to property violations agent if no clear match
                default_category = CaseCategory.PROPERTY_VIOLATIONS
                default_agent = self.agents[default_category]
                logger.info(f"No clear match, using default agent: {default_agent.agent_name}")
                return default_category, default_agent, 0.1
                
        except Exception as e:
            logger.error(f"Error selecting agent: {str(e)}")
            # Return default agent on error
            default_category = CaseCategory.PROPERTY_VIOLATIONS
            return default_category, self.agents[default_category], 0.0
    
    def route_query(self, query: str, case_type: str = None) -> Dict[str, Any]:
        """Route query to appropriate specialized agent and get analysis"""
        try:
            start_time = datetime.now()
            
            # Select best agent
            category, agent, confidence = self.select_best_agent(query, case_type)
            
            # Get analysis from selected agent
            analysis = agent.analyze_case(query, case_type or "General Legal Matter")
            
            # Add routing information
            analysis["routing_info"] = {
                "selected_agent": agent.agent_name,
                "agent_category": category.value,
                "selection_confidence": confidence,
                "routing_timestamp": datetime.now().isoformat(),
                "processing_time": (datetime.now() - start_time).total_seconds()
            }
            
            # Update statistics
            self.update_routing_statistics(category, True, (datetime.now() - start_time).total_seconds())
            
            logger.info(f"Query routed successfully to {agent.agent_name}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error routing query: {str(e)}")
            return {
                "error": f"Routing error: {str(e)}",
                "routing_info": {
                    "selected_agent": "Error",
                    "agent_category": "unknown",
                    "selection_confidence": 0.0,
                    "routing_timestamp": datetime.now().isoformat()
                }
            }
    
    def update_routing_statistics(self, category: CaseCategory, success: bool, processing_time: float):
        """Update routing and performance statistics"""
        try:
            stats = self.case_statistics[category]
            stats["total_cases"] += 1
            
            if success:
                stats["successful_cases"] += 1
            
            # Update average processing time
            total_time = stats["average_processing_time"] * (stats["total_cases"] - 1) + processing_time
            stats["average_processing_time"] = total_time / stats["total_cases"]
            
            # Update success rate
            stats["success_rate"] = stats["successful_cases"] / stats["total_cases"]
            
            logger.debug(f"Updated statistics for {category}: {stats}")
            
        except Exception as e:
            logger.error(f"Error updating statistics: {str(e)}")
    
    def get_agent_info(self, category: CaseCategory = None) -> Dict[str, Any]:
        """Get information about agents and their performance"""
        try:
            if category and category in self.agents:
                agent = self.agents[category]
                stats = self.case_statistics[category]
                return {
                    "agent_info": agent.get_agent_info(),
                    "routing_statistics": stats,
                    "specialization_keywords": self.routing_keywords[category]
                }
            else:
                # Return information about all agents
                all_info = {}
                for cat, agent in self.agents.items():
                    all_info[cat.value] = {
                        "agent_info": agent.get_agent_info(),
                        "routing_statistics": self.case_statistics[cat],
                        "specialization_keywords": self.routing_keywords[cat][:5]  # First 5 keywords
                    }
                return all_info
                
        except Exception as e:
            logger.error(f"Error getting agent info: {str(e)}")
            return {"error": str(e)}
    
    def get_routing_recommendations(self, query: str) -> List[Dict[str, Any]]:
        """Get routing recommendations with confidence scores for all agents"""
        try:
            scores = self.analyze_query_keywords(query)
            recommendations = []

            for category, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                if category in self.agents:
                    agent = self.agents[category]
                    recommendations.append({
                        "agent_name": agent.agent_name,
                        "category": category.value,
                        "confidence_score": score,
                        "specialization": agent.specialization,
                        "recommendation": "Highly Recommended" if score > 2.0 else
                                       "Recommended" if score > 1.0 else
                                       "Possible Match" if score > 0.5 else "Low Match"
                    })

            return recommendations

        except Exception as e:
            logger.error(f"Error getting routing recommendations: {str(e)}")
            return []



    def get_agent_by_category(self, category: CaseCategory) -> SpecializedLegalAgent:
        """Get agent by category"""
        return self.agents.get(category)

# Global agent router instance
agent_router = None

def get_agent_router() -> AgentRouter:
    """Get or create global agent router instance"""
    global agent_router
    if agent_router is None:
        agent_router = AgentRouter()
    return agent_router
