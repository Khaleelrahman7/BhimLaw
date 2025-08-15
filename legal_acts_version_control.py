"""
BhimLaw AI - Legal Acts Version Control System
Tracks amendments, notifications, and change history for all legal acts
Ensures transparency and auditability of legal information updates
"""

import json
import sqlite3
import logging
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
from legal_acts_database import legal_acts_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VersionInfo:
    """Version information for legal acts"""
    version: str
    release_date: str
    amendment_type: str
    notification_number: str
    gazette_reference: str
    ministry: str
    summary: str
    sections_affected: List[str]
    checksum: str

@dataclass
class ChangeRecord:
    """Record of changes made to legal acts"""
    change_id: str
    act_id: str
    change_type: str  # "amendment", "correction", "interpretation"
    old_content: str
    new_content: str
    change_date: str
    authority: str
    justification: str
    impact_assessment: str

class LegalActsVersionControl:
    """
    Version Control System for Legal Acts
    Tracks all changes, amendments, and updates with full audit trail
    """
    
    def __init__(self, db_path: str = "legal_acts_version.db"):
        self.db_path = db_path
        self.init_version_database()
    
    def init_version_database(self):
        """Initialize version control database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create version_history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS version_history (
                    version_id TEXT PRIMARY KEY,
                    act_id TEXT NOT NULL,
                    version TEXT NOT NULL,
                    release_date TEXT NOT NULL,
                    amendment_type TEXT NOT NULL,
                    notification_number TEXT,
                    gazette_reference TEXT,
                    ministry TEXT,
                    summary TEXT,
                    sections_affected TEXT,  -- JSON string
                    checksum TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (act_id) REFERENCES legal_acts (act_id)
                )
            ''')
            
            # Create change_records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS change_records (
                    change_id TEXT PRIMARY KEY,
                    act_id TEXT NOT NULL,
                    version_id TEXT NOT NULL,
                    change_type TEXT NOT NULL,
                    section_number TEXT,
                    old_content TEXT,
                    new_content TEXT,
                    change_date TEXT NOT NULL,
                    authority TEXT,
                    justification TEXT,
                    impact_assessment TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (act_id) REFERENCES legal_acts (act_id),
                    FOREIGN KEY (version_id) REFERENCES version_history (version_id)
                )
            ''')
            
            # Create amendment_notifications table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS amendment_notifications (
                    notification_id TEXT PRIMARY KEY,
                    act_id TEXT NOT NULL,
                    notification_number TEXT NOT NULL,
                    notification_date TEXT NOT NULL,
                    gazette_date TEXT,
                    gazette_number TEXT,
                    ministry TEXT,
                    department TEXT,
                    notification_type TEXT,  -- "amendment", "clarification", "correction"
                    content TEXT,
                    effective_date TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create version_comparison table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS version_comparison (
                    comparison_id TEXT PRIMARY KEY,
                    act_id TEXT NOT NULL,
                    old_version TEXT NOT NULL,
                    new_version TEXT NOT NULL,
                    comparison_date TEXT NOT NULL,
                    differences TEXT,  -- JSON string
                    similarity_score REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Version control database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing version database: {str(e)}")
            raise
    
    def create_version(self, act_id: str, version_info: Dict[str, Any]) -> str:
        """Create a new version record for an act"""
        try:
            version_id = f"{act_id}_{version_info['version']}_{datetime.now().strftime('%Y%m%d')}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO version_history (
                    version_id, act_id, version, release_date, amendment_type,
                    notification_number, gazette_reference, ministry, summary,
                    sections_affected, checksum
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                version_id, act_id, version_info['version'], version_info['release_date'],
                version_info['amendment_type'], version_info.get('notification_number'),
                version_info.get('gazette_reference'), version_info.get('ministry'),
                version_info.get('summary'), json.dumps(version_info.get('sections_affected', [])),
                version_info['checksum']
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created version {version_info['version']} for act {act_id}")
            return version_id
            
        except Exception as e:
            logger.error(f"Error creating version: {str(e)}")
            return ""
    
    def record_change(self, change_record: Dict[str, Any]) -> str:
        """Record a specific change made to an act"""
        try:
            change_id = f"CHG_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{change_record['act_id']}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO change_records (
                    change_id, act_id, version_id, change_type, section_number,
                    old_content, new_content, change_date, authority,
                    justification, impact_assessment
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                change_id, change_record['act_id'], change_record.get('version_id'),
                change_record['change_type'], change_record.get('section_number'),
                change_record.get('old_content'), change_record.get('new_content'),
                change_record['change_date'], change_record.get('authority'),
                change_record.get('justification'), change_record.get('impact_assessment')
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Recorded change {change_id} for act {change_record['act_id']}")
            return change_id
            
        except Exception as e:
            logger.error(f"Error recording change: {str(e)}")
            return ""
    
    def add_amendment_notification(self, notification: Dict[str, Any]) -> str:
        """Add an amendment notification"""
        try:
            notification_id = f"NOT_{notification['notification_number']}_{datetime.now().strftime('%Y%m%d')}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO amendment_notifications (
                    notification_id, act_id, notification_number, notification_date,
                    gazette_date, gazette_number, ministry, department,
                    notification_type, content, effective_date, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                notification_id, notification['act_id'], notification['notification_number'],
                notification['notification_date'], notification.get('gazette_date'),
                notification.get('gazette_number'), notification.get('ministry'),
                notification.get('department'), notification.get('notification_type'),
                notification.get('content'), notification.get('effective_date'),
                notification.get('status', 'active')
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added amendment notification {notification_id}")
            return notification_id
            
        except Exception as e:
            logger.error(f"Error adding amendment notification: {str(e)}")
            return ""
    
    def get_version_history(self, act_id: str) -> List[Dict[str, Any]]:
        """Get version history for an act"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT version_id, version, release_date, amendment_type,
                       notification_number, gazette_reference, ministry,
                       summary, sections_affected, checksum
                FROM version_history
                WHERE act_id = ?
                ORDER BY release_date DESC
            ''', (act_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            versions = []
            for row in rows:
                versions.append({
                    "version_id": row[0],
                    "version": row[1],
                    "release_date": row[2],
                    "amendment_type": row[3],
                    "notification_number": row[4],
                    "gazette_reference": row[5],
                    "ministry": row[6],
                    "summary": row[7],
                    "sections_affected": json.loads(row[8]) if row[8] else [],
                    "checksum": row[9]
                })
            
            return versions
            
        except Exception as e:
            logger.error(f"Error getting version history: {str(e)}")
            return []
    
    def get_change_history(self, act_id: str, version_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get change history for an act or specific version"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if version_id:
                cursor.execute('''
                    SELECT change_id, change_type, section_number, old_content,
                           new_content, change_date, authority, justification,
                           impact_assessment
                    FROM change_records
                    WHERE act_id = ? AND version_id = ?
                    ORDER BY change_date DESC
                ''', (act_id, version_id))
            else:
                cursor.execute('''
                    SELECT change_id, change_type, section_number, old_content,
                           new_content, change_date, authority, justification,
                           impact_assessment
                    FROM change_records
                    WHERE act_id = ?
                    ORDER BY change_date DESC
                ''', (act_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            changes = []
            for row in rows:
                changes.append({
                    "change_id": row[0],
                    "change_type": row[1],
                    "section_number": row[2],
                    "old_content": row[3],
                    "new_content": row[4],
                    "change_date": row[5],
                    "authority": row[6],
                    "justification": row[7],
                    "impact_assessment": row[8]
                })
            
            return changes
            
        except Exception as e:
            logger.error(f"Error getting change history: {str(e)}")
            return []
    
    def get_amendment_notifications(self, act_id: str, days: int = 90) -> List[Dict[str, Any]]:
        """Get recent amendment notifications for an act"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT notification_id, notification_number, notification_date,
                       gazette_date, gazette_number, ministry, department,
                       notification_type, content, effective_date, status
                FROM amendment_notifications
                WHERE act_id = ? AND datetime(notification_date) >= datetime('now', '-{} days')
                ORDER BY notification_date DESC
            '''.format(days), (act_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            notifications = []
            for row in rows:
                notifications.append({
                    "notification_id": row[0],
                    "notification_number": row[1],
                    "notification_date": row[2],
                    "gazette_date": row[3],
                    "gazette_number": row[4],
                    "ministry": row[5],
                    "department": row[6],
                    "notification_type": row[7],
                    "content": row[8],
                    "effective_date": row[9],
                    "status": row[10]
                })
            
            return notifications
            
        except Exception as e:
            logger.error(f"Error getting amendment notifications: {str(e)}")
            return []
    
    def compare_versions(self, act_id: str, old_version: str, new_version: str) -> Dict[str, Any]:
        """Compare two versions of an act"""
        try:
            # Get both versions
            old_act = self._get_act_version(act_id, old_version)
            new_act = self._get_act_version(act_id, new_version)
            
            if not old_act or not new_act:
                return {"error": "One or both versions not found"}
            
            # Compare sections
            differences = self._compare_sections(old_act.get("sections", {}), new_act.get("sections", {}))
            
            # Calculate similarity score
            similarity_score = self._calculate_similarity(old_act, new_act)
            
            comparison_result = {
                "act_id": act_id,
                "old_version": old_version,
                "new_version": new_version,
                "comparison_date": datetime.now().isoformat(),
                "differences": differences,
                "similarity_score": similarity_score,
                "summary": self._generate_comparison_summary(differences)
            }
            
            # Store comparison result
            self._store_comparison(comparison_result)
            
            return comparison_result
            
        except Exception as e:
            logger.error(f"Error comparing versions: {str(e)}")
            return {"error": str(e)}
    
    def _get_act_version(self, act_id: str, version: str) -> Optional[Dict[str, Any]]:
        """Get a specific version of an act"""
        # This would typically fetch from version history
        # For now, get current version from main database
        return legal_acts_db.get_act(act_id)
    
    def _compare_sections(self, old_sections: Dict[str, str], new_sections: Dict[str, str]) -> List[Dict[str, Any]]:
        """Compare sections between two versions"""
        differences = []
        
        # Check for modified sections
        for section, content in new_sections.items():
            if section in old_sections:
                if old_sections[section] != content:
                    differences.append({
                        "type": "modified",
                        "section": section,
                        "old_content": old_sections[section],
                        "new_content": content
                    })
            else:
                differences.append({
                    "type": "added",
                    "section": section,
                    "new_content": content
                })
        
        # Check for deleted sections
        for section in old_sections:
            if section not in new_sections:
                differences.append({
                    "type": "deleted",
                    "section": section,
                    "old_content": old_sections[section]
                })
        
        return differences
    
    def _calculate_similarity(self, old_act: Dict[str, Any], new_act: Dict[str, Any]) -> float:
        """Calculate similarity score between two versions"""
        try:
            old_content = json.dumps(old_act.get("sections", {}), sort_keys=True)
            new_content = json.dumps(new_act.get("sections", {}), sort_keys=True)
            
            # Simple similarity calculation based on content length
            if len(old_content) == 0 and len(new_content) == 0:
                return 1.0
            
            max_len = max(len(old_content), len(new_content))
            min_len = min(len(old_content), len(new_content))
            
            return min_len / max_len if max_len > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def _generate_comparison_summary(self, differences: List[Dict[str, Any]]) -> str:
        """Generate a summary of differences"""
        if not differences:
            return "No differences found between versions"
        
        added = len([d for d in differences if d["type"] == "added"])
        modified = len([d for d in differences if d["type"] == "modified"])
        deleted = len([d for d in differences if d["type"] == "deleted"])
        
        summary_parts = []
        if added > 0:
            summary_parts.append(f"{added} sections added")
        if modified > 0:
            summary_parts.append(f"{modified} sections modified")
        if deleted > 0:
            summary_parts.append(f"{deleted} sections deleted")
        
        return ", ".join(summary_parts)
    
    def _store_comparison(self, comparison: Dict[str, Any]):
        """Store comparison result in database"""
        try:
            comparison_id = f"CMP_{comparison['act_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO version_comparison (
                    comparison_id, act_id, old_version, new_version,
                    comparison_date, differences, similarity_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                comparison_id, comparison['act_id'], comparison['old_version'],
                comparison['new_version'], comparison['comparison_date'],
                json.dumps(comparison['differences']), comparison['similarity_score']
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing comparison: {str(e)}")
    
    def get_version_control_stats(self) -> Dict[str, Any]:
        """Get version control statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count total versions
            cursor.execute("SELECT COUNT(*) FROM version_history")
            total_versions = cursor.fetchone()[0]
            
            # Count total changes
            cursor.execute("SELECT COUNT(*) FROM change_records")
            total_changes = cursor.fetchone()[0]
            
            # Count recent notifications
            cursor.execute('''
                SELECT COUNT(*) FROM amendment_notifications 
                WHERE datetime(notification_date) >= datetime('now', '-30 days')
            ''')
            recent_notifications = cursor.fetchone()[0]
            
            # Count acts with versions
            cursor.execute("SELECT COUNT(DISTINCT act_id) FROM version_history")
            acts_with_versions = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_versions": total_versions,
                "total_changes": total_changes,
                "recent_notifications": recent_notifications,
                "acts_with_versions": acts_with_versions,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting version control stats: {str(e)}")
            return {}

# Global instance
legal_acts_version_control = LegalActsVersionControl()
