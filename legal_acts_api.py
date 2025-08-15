"""
BhimLaw AI - Legal Acts API Endpoints
API endpoints to manage legal acts updates, view current versions, and trigger manual updates
Provides comprehensive access to the legal acts database and version control system
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from legal_acts_database import legal_acts_db
from legal_acts_updater import legal_acts_updater
from legal_acts_version_control import legal_acts_version_control

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Create router
legal_acts_router = APIRouter(prefix="/api/legal-acts", tags=["Legal Acts Management"])

# Pydantic models for API requests/responses
class LegalActResponse(BaseModel):
    """Response model for legal act data"""
    act_id: str
    name: str
    year: int
    sections: Dict[str, str]
    amendments: List[Dict[str, Any]]
    last_updated: str
    source_url: str
    notification_number: str
    ministry: str
    category: str
    status: str
    version: str

class LegalActSummary(BaseModel):
    """Summary model for legal act listings"""
    act_id: str
    name: str
    year: int
    last_updated: str
    version: str
    category: str
    ministry: str

class UpdateRequest(BaseModel):
    """Request model for manual updates"""
    act_ids: Optional[List[str]] = Field(None, description="Specific acts to update (if empty, updates all)")
    force_update: bool = Field(False, description="Force update even if recently updated")
    sources: Optional[List[str]] = Field(None, description="Specific sources to use for updates")

class VersionHistoryResponse(BaseModel):
    """Response model for version history"""
    version_id: str
    version: str
    release_date: str
    amendment_type: str
    notification_number: Optional[str]
    gazette_reference: Optional[str]
    ministry: Optional[str]
    summary: Optional[str]
    sections_affected: List[str]

class AmendmentNotificationResponse(BaseModel):
    """Response model for amendment notifications"""
    notification_id: str
    notification_number: str
    notification_date: str
    gazette_date: Optional[str]
    gazette_number: Optional[str]
    ministry: Optional[str]
    department: Optional[str]
    notification_type: Optional[str]
    content: Optional[str]
    effective_date: Optional[str]
    status: str

class DatabaseStatsResponse(BaseModel):
    """Response model for database statistics"""
    total_acts: int
    category_counts: Dict[str, int]
    recent_updates: int
    last_update: Optional[str]
    database_version: str

class UpdateResultResponse(BaseModel):
    """Response model for update results"""
    total_checked: int
    updated: int
    errors: int
    new_acts: int
    sources_used: List[str]
    update_summary: List[str]
    timestamp: str

# API Endpoints

@legal_acts_router.get("/", response_model=List[LegalActSummary])
async def get_all_acts(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in act names and content"),
    limit: int = Query(100, description="Maximum number of results")
):
    """Get all legal acts with optional filtering"""
    try:
        if search:
            acts = legal_acts_db.search_acts(search)
        elif category:
            acts = legal_acts_db.get_acts_by_category(category)
        else:
            acts = legal_acts_db.get_all_acts()
        
        # Limit results
        acts = acts[:limit]
        
        return [
            LegalActSummary(
                act_id=act["act_id"],
                name=act["name"],
                year=act["year"],
                last_updated=act["last_updated"],
                version=act["version"],
                category=act["category"],
                ministry=act["ministry"]
            )
            for act in acts
        ]
        
    except Exception as e:
        logger.error(f"Error getting acts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.get("/{act_id}", response_model=LegalActResponse)
async def get_act(act_id: str):
    """Get a specific legal act by ID"""
    try:
        act = legal_acts_db.get_act(act_id)
        
        if not act:
            raise HTTPException(status_code=404, detail=f"Act {act_id} not found")
        
        return LegalActResponse(**act)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting act {act_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.get("/{act_id}/versions", response_model=List[VersionHistoryResponse])
async def get_act_versions(act_id: str):
    """Get version history for a specific act"""
    try:
        versions = legal_acts_version_control.get_version_history(act_id)
        
        return [
            VersionHistoryResponse(**version)
            for version in versions
        ]
        
    except Exception as e:
        logger.error(f"Error getting versions for {act_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.get("/{act_id}/amendments", response_model=List[AmendmentNotificationResponse])
async def get_act_amendments(
    act_id: str,
    days: int = Query(90, description="Number of days to look back for amendments")
):
    """Get recent amendment notifications for a specific act"""
    try:
        amendments = legal_acts_version_control.get_amendment_notifications(act_id, days)
        
        return [
            AmendmentNotificationResponse(**amendment)
            for amendment in amendments
        ]
        
    except Exception as e:
        logger.error(f"Error getting amendments for {act_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.get("/{act_id}/changes")
async def get_act_changes(
    act_id: str,
    version_id: Optional[str] = Query(None, description="Specific version to get changes for")
):
    """Get change history for a specific act"""
    try:
        changes = legal_acts_version_control.get_change_history(act_id, version_id)
        
        return {
            "act_id": act_id,
            "version_id": version_id,
            "changes": changes,
            "total_changes": len(changes)
        }
        
    except Exception as e:
        logger.error(f"Error getting changes for {act_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.post("/{act_id}/check-updates")
async def check_act_updates(act_id: str):
    """Check if a specific act needs updates"""
    try:
        update_check = legal_acts_updater.check_for_updates(act_id)
        
        return {
            "act_id": act_id,
            "check_timestamp": datetime.now().isoformat(),
            **update_check
        }
        
    except Exception as e:
        logger.error(f"Error checking updates for {act_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.post("/update", response_model=UpdateResultResponse)
async def trigger_updates(
    background_tasks: BackgroundTasks,
    request: UpdateRequest = UpdateRequest()
):
    """Trigger manual updates for legal acts"""
    try:
        # Add update task to background
        background_tasks.add_task(perform_updates, request)
        
        return UpdateResultResponse(
            total_checked=0,
            updated=0,
            errors=0,
            new_acts=0,
            sources_used=[],
            update_summary=["Update task started in background"],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error triggering updates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.get("/stats/database", response_model=DatabaseStatsResponse)
async def get_database_stats():
    """Get database statistics"""
    try:
        stats = legal_acts_db.get_database_stats()
        
        return DatabaseStatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Error getting database stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.get("/stats/version-control")
async def get_version_control_stats():
    """Get version control statistics"""
    try:
        stats = legal_acts_version_control.get_version_control_stats()
        
        return {
            "version_control_stats": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting version control stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.get("/recent-updates")
async def get_recent_updates(
    days: int = Query(30, description="Number of days to look back")
):
    """Get recently updated acts"""
    try:
        updates = legal_acts_db.get_recent_updates(days)
        
        return {
            "recent_updates": updates,
            "days_range": days,
            "total_updates": len(updates),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting recent updates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.get("/categories")
async def get_categories():
    """Get all available legal act categories"""
    try:
        stats = legal_acts_db.get_database_stats()
        categories = stats.get("category_counts", {})
        
        return {
            "categories": list(categories.keys()),
            "category_counts": categories,
            "total_categories": len(categories)
        }
        
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.post("/{act_id}/compare-versions")
async def compare_act_versions(
    act_id: str,
    old_version: str = Query(..., description="Old version to compare"),
    new_version: str = Query(..., description="New version to compare")
):
    """Compare two versions of an act"""
    try:
        comparison = legal_acts_version_control.compare_versions(act_id, old_version, new_version)
        
        return comparison
        
    except Exception as e:
        logger.error(f"Error comparing versions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@legal_acts_router.get("/health")
async def health_check():
    """Health check endpoint for the legal acts system"""
    try:
        # Check database connectivity
        stats = legal_acts_db.get_database_stats()
        version_stats = legal_acts_version_control.get_version_control_stats()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database_connected": bool(stats),
            "version_control_connected": bool(version_stats),
            "total_acts": stats.get("total_acts", 0),
            "system_version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# Background task functions
async def perform_updates(request: UpdateRequest):
    """Perform updates in background"""
    try:
        logger.info("Starting background legal acts update")
        
        if request.act_ids:
            # Update specific acts
            for act_id in request.act_ids:
                legal_acts_updater.check_for_updates(act_id)
        else:
            # Update all acts
            legal_acts_updater.update_all_acts()
        
        logger.info("Background legal acts update completed")
        
    except Exception as e:
        logger.error(f"Error in background update: {str(e)}")

# Export router
__all__ = ["legal_acts_router"]
