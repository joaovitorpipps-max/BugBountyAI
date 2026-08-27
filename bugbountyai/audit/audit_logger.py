"""Audit Logging System untuk v2"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json
import sqlite3

logger = logging.getLogger(__name__)


class AuditLogger:
    """System untuk audit logging semua aktivitas"""

    def __init__(self, db_path: str = "audit.db"):
        """Initialize audit logger
        
        Args:
            db_path: Path to audit log database
        """
        self.db_path = db_path
        self._init_database()
        logger.info("AuditLogger initialized")

    def log_action(self, user_id: str, action: str, resource: str, details: Dict) -> None:
        """Log user action
        
        Args:
            user_id: User ID performing action
            action: Action performed (create, read, update, delete)
            resource: Resource type
            details: Additional details
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "details": details,
            "status": "success",
        }
        
        self._store_log(log_entry)
        logger.info(f"Audit log: {action} on {resource} by {user_id}")

    def log_error(self, user_id: str, action: str, error: str) -> None:
        """Log error/failed action
        
        Args:
            user_id: User ID
            action: Failed action
            error: Error message
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "error": error,
            "status": "failed",
        }
        
        self._store_log(log_entry)
        logger.warning(f"Audit error log: {action} failed for {user_id} - {error}")

    def log_security_event(self, event_type: str, details: Dict) -> None:
        """Log security-related events
        
        Args:
            event_type: Type of security event
            details: Event details
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "severity": details.get("severity", "medium"),
            "details": details,
        }
        
        self._store_log(log_entry)
        logger.warning(f"Security event: {event_type}")

    def get_audit_trail(self, user_id: Optional[str] = None, limit: int = 100) -> list:
        """Get audit trail
        
        Args:
            user_id: Filter by user (optional)
            limit: Number of records
            
        Returns:
            List of audit logs
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute(
                    "SELECT * FROM audit_logs WHERE user_id=? ORDER BY timestamp DESC LIMIT ?",
                    (user_id, limit),
                )
            else:
                cursor.execute(
                    "SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?",
                    (limit,),
                )
            
            records = cursor.fetchall()
            conn.close()
            
            return records
        except Exception as e:
            logger.error(f"Error retrieving audit trail: {str(e)}")
            return []

    def _init_database(self) -> None:
        """Initialize SQLite database untuk audit logs"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_id TEXT,
                    action TEXT,
                    resource TEXT,
                    details TEXT,
                    status TEXT,
                    event_type TEXT,
                    severity TEXT,
                    error TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Audit database initialized")
        except Exception as e:
            logger.error(f"Error initializing audit database: {str(e)}")

    def _store_log(self, log_entry: Dict) -> None:
        """Store log entry in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO audit_logs 
                (timestamp, user_id, action, resource, details, status, event_type, severity, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log_entry.get("timestamp"),
                log_entry.get("user_id"),
                log_entry.get("action"),
                log_entry.get("resource"),
                json.dumps(log_entry.get("details", {})),
                log_entry.get("status"),
                log_entry.get("event_type"),
                log_entry.get("severity"),
                log_entry.get("error"),
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error storing audit log: {str(e)}")
