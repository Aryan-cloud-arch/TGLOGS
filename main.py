#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
#
#                      TELEGRAM ACCOUNT MANAGER (TGM)
#
#                         Created by: @MaiHuAryan
#                         Telegram: t.me/MaiHuAryan
#
#                              Version: 1.0.0
#                              License: MIT
#
#     ██████╗ ███╗   ███╗ █████╗ ██╗██╗  ██╗██╗   ██╗ █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗
#    ██╔═══██╗████╗ ████║██╔══██╗██║██║  ██║██║   ██║██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║
#    ██║   ██║██╔████╔██║███████║██║███████║██║   ██║███████║██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║
#    ██║   ██║██║╚██╔╝██║██╔══██║██║██╔══██║██║   ██║██╔══██║██╔══██╗  ╚██╔╝  ██╔══██║██║╚██╗██║
#    ╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║  ██║╚██████╔╝██║  ██║██║  ██║   ██║   ██║  ██║██║ ╚████║
#     ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
#
#   Telegram: t.me/MaiHuAryan | GitHub: @MaiHuAryan
#
#   Features:
#   • Multi-account session management
#   • OTP listener for login codes
#   • Auto session refresh (no manual input!)
#   • Health monitoring & status tracking
#   • Encrypted backup/restore
#   • Beautiful TUI interface
#
#   Support: t.me/MaiHuAryan
#
# ══════════════════════════════════════════════════════════════════════════════
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      TELEGRAM ACCOUNT MANAGER (TGM)                          ║
║                                                                              ║
║                         Created by: @MaiHuAryan                              ║
║                         Telegram: t.me/MaiHuAryan                            ║
║                                                                              ║
║   Features:                                                                  ║
║   • Multi-account session management                                         ║
║   • OTP listener for login codes                                             ║
║   • Auto session refresh                                                     ║
║   • Health monitoring                                                        ║
║   • Encrypted backup/restore                                                 ║
║                                                                              ║
║   Support & Updates: t.me/MaiHuAryan                                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: IMPORTS
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import os
import sys
import sqlite3
import asyncio
import hashlib
import base64
import json
import re
import signal
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple, Any, Callable
from pathlib import Path
from contextlib import contextmanager

# ─────────────────────────────────────────────────────────────────────────────
# Third-party imports with proper error handling
# @MaiHuAryan | t.me/MaiHuAryan
# ─────────────────────────────────────────────────────────────────────────────

MISSING_DEPS = []

try:
    import yaml
except ImportError:
    MISSING_DEPS.append("pyyaml")

try:
    from telethon import TelegramClient, events
    from telethon.sessions import StringSession
    from telethon.errors import (
        SessionPasswordNeededError,
        PhoneCodeInvalidError,
        PhoneCodeExpiredError,
        FloodWaitError,
        AuthKeyUnregisteredError,
        UserDeactivatedBanError,
        PhoneNumberInvalidError,
        PhoneNumberBannedError,
        ApiIdInvalidError,
        PasswordHashInvalidError,
        PhoneNumberUnoccupiedError,
    )
    from telethon.tl.functions.account import GetAuthorizationsRequest
    from telethon.tl.types import User
except ImportError:
    MISSING_DEPS.append("telethon")

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.text import Text
    from rich.align import Align
    from rich.live import Live
    from rich.layout import Layout
    from rich.style import Style
    from rich import box
    from rich.markdown import Markdown
except ImportError:
    MISSING_DEPS.append("rich")

try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    MISSING_DEPS.append("cryptography")

# ─────────────────────────────────────────────────────────────────────────────
# Check for missing dependencies - @MaiHuAryan
# ─────────────────────────────────────────────────────────────────────────────

if MISSING_DEPS:
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║              ❌ MISSING DEPENDENCIES                             ║")
    print("║                                                                  ║")
    print("║  Created by: @MaiHuAryan | t.me/MaiHuAryan                      ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print("║                                                                  ║")
    for dep in MISSING_DEPS:
        print(f"║  • {dep:<60} ║")
    print("║                                                                  ║")
    print("║  Run: pip install -r requirements.txt                           ║")
    print("║                                                                  ║")
    print("║  Support: t.me/MaiHuAryan                                       ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    sys.exit(1)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: CONSTANTS & CONFIGURATION
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

VERSION = "1.0.0"
AUTHOR = "@MaiHuAryan"
TELEGRAM_LINK = "t.me/MaiHuAryan"
APP_NAME = "Telegram Account Manager"
DB_NAME = "sessions.db"
CONFIG_FILE = "config.yaml"
BACKUP_DIR = "backups"
LOG_DIR = "logs"

# Telegram's official account ID for OTP messages
TELEGRAM_OTP_SENDER = 777000

# Timeouts (in seconds)
OTP_TIMEOUT = 300  # 5 minutes
HEALTH_CHECK_TIMEOUT = 30
SESSION_TIMEOUT = 60

# Rich console instance - @MaiHuAryan
console = Console()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: UTILITY FUNCTIONS
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

def clear_screen() -> None:
    """Clear terminal screen - @MaiHuAryan"""
    console.clear()


def get_timestamp() -> str:
    """Get current timestamp string - @MaiHuAryan"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_date_string() -> str:
    """Get current date string for filenames - @MaiHuAryan"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def mask_phone(phone: str) -> str:
    """
    Mask phone number for display security
    Example: +919876543210 → +91****3210
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    if not phone:
        return "N/A"
    phone = str(phone).strip()
    if len(phone) < 8:
        return phone
    # Keep first 3 and last 4 characters
    return phone[:3] + "*" * (len(phone) - 7) + phone[-4:]


def format_phone(phone: str) -> str:
    """
    Format and validate phone number
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    if not phone:
        return ""
    # Remove spaces, dashes, parentheses
    phone = re.sub(r'[\s\-\(\)]', '', phone.strip())
    # Add + if missing
    if not phone.startswith('+'):
        phone = '+' + phone
    return phone


def extract_otp_code(text: str) -> Optional[str]:
    """
    Extract OTP code from Telegram message
    Handles multiple formats used by Telegram
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    if not text:
        return None
    
    # Comprehensive patterns for Telegram login codes
    patterns = [
        # Standard patterns
        r'Login code:\s*(\d{5,6})',
        r'login code:\s*(\d{5,6})',
        r'Login Code:\s*(\d{5,6})',
        r'code:\s*(\d{5,6})',
        r'Code:\s*(\d{5,6})',
        r'Your code:\s*(\d{5,6})',
        r'your code:\s*(\d{5,6})',
        r'Your Code:\s*(\d{5,6})',
        # Code is pattern
        r'code is\s*[:\s]*(\d{5,6})',
        r'Code is\s*[:\s]*(\d{5,6})',
        # Confirmation patterns
        r'confirmation code:\s*(\d{5,6})',
        r'Confirmation code:\s*(\d{5,6})',
        r'verification code:\s*(\d{5,6})',
        r'Verification code:\s*(\d{5,6})',
        # "is your" pattern
        r'(\d{5,6})\s*is your',
        r'(\d{5,6})\s+is\s+your',
        # Web login
        r'web login code:\s*(\d{5,6})',
        r'Web login code:\s*(\d{5,6})',
        # App code
        r'app code:\s*(\d{5,6})',
        r'App code:\s*(\d{5,6})',
        # Standalone code (5-6 digits on their own line or clearly separated)
        r'^(\d{5,6})$',
        r'\n(\d{5,6})\n',
        r'\n(\d{5,6})$',
        r'^(\d{5,6})\n',
        # Fallback: any 5-6 digit number (less reliable)
        r'\b(\d{5,6})\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            code = match.group(1)
            # Validate it's a reasonable OTP (5-6 digits)
            if len(code) >= 5 and len(code) <= 6:
                return code
    
    return None


def time_ago(timestamp: Optional[str]) -> str:
    """
    Convert timestamp to human-readable 'time ago' format
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    if not timestamp:
        return "Never"
    
    try:
        # Handle multiple timestamp formats
        formats_to_try = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
        ]
        
        dt = None
        for fmt in formats_to_try:
            try:
                dt = datetime.strptime(str(timestamp), fmt)
                break
            except ValueError:
                continue
        
        if not dt:
            return "Unknown"
        
        diff = datetime.now() - dt
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} min{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
            
    except Exception:
        return "Unknown"


def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number format
    Author: @MaiHuAryan | t.me/MaiHuAryan
    
    Returns: (is_valid, error_message)
    """
    if not phone:
        return False, "Phone number is required"
    
    phone = format_phone(phone)
    
    # Check if starts with +
    if not phone.startswith('+'):
        return False, "Phone must start with +"
    
    # Check if contains only digits after +
    if not phone[1:].isdigit():
        return False, "Phone must contain only digits after +"
    
    # Check length (most countries: 10-15 digits)
    if len(phone) < 10 or len(phone) > 16:
        return False, "Phone number length is invalid"
    
    return True, "Valid"


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to clipboard (works in Termux and other environments)
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    try:
        # Try termux-clipboard-set first (for Termux)
        import subprocess
        result = subprocess.run(
            ['termux-clipboard-set'],
            input=text.encode(),
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass
    
    try:
        # Try xclip (Linux with X11)
        import subprocess
        result = subprocess.run(
            ['xclip', '-selection', 'clipboard'],
            input=text.encode(),
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass
    
    return False


def play_notification_sound() -> None:
    """
    Play notification sound (best effort)
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    try:
        # Print bell character for terminal notification
        print('\a', end='', flush=True)
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: ENCRYPTION UTILITIES
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

class Encryptor:
    """
    Handle encryption/decryption of sensitive data using Fernet
    Uses PBKDF2 for key derivation from password
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    
    # Salt for key derivation (consistent across sessions)
    SALT = b'tgm_salt_@MaiHuAryan_2024'
    ITERATIONS = 480000  # OWASP recommended minimum
    
    def __init__(self, password: Optional[str] = None):
        """
        Initialize encryptor with password
        Uses a default key if no password provided
        """
        self.password = password or "tgm_default_key_@MaiHuAryan"
        self._fernet: Optional[Fernet] = None
    
    @property
    def fernet(self) -> Fernet:
        """Lazy initialization of Fernet instance"""
        if self._fernet is None:
            self._fernet = self._create_fernet()
        return self._fernet
    
    def _create_fernet(self) -> Fernet:
        """
        Create Fernet instance from password using PBKDF2
        Author: @MaiHuAryan
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.SALT,
            iterations=self.ITERATIONS,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password.encode()))
        return Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt string data
        Returns empty string if input is empty
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        if not data:
            return ""
        try:
            encrypted = self.fernet.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            console.print(f"[red]Encryption error: {e}[/red]")
            return ""
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted string
        Returns empty string if decryption fails
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        if not encrypted_data:
            return ""
        try:
            decrypted = self.fernet.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except InvalidToken:
            # Wrong password or corrupted data
            return ""
        except Exception as e:
            console.print(f"[dim]Decryption error: {e}[/dim]")
            return ""


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5: DATABASE MANAGER
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

class DatabaseManager:
    """
    Handle all database operations with SQLite
    Thread-safe with context manager for connections
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    
    def __init__(self, db_name: str = DB_NAME):
        """Initialize database manager"""
        self.db_name = db_name
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections
        Ensures proper cleanup and uses Row factory
        Author: @MaiHuAryan
        """
        conn = sqlite3.connect(self.db_name, timeout=30)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def _init_database(self) -> None:
        """
        Initialize database tables with proper schema
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # ─────────────────────────────────────────────────────────────────
            # Main accounts table
            # ─────────────────────────────────────────────────────────────────
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    label TEXT NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    session_string TEXT,
                    session_backup TEXT,
                    tfa_password TEXT,
                    status TEXT DEFAULT 'ACTIVE',
                    last_checked TIMESTAMP,
                    last_refreshed TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    first_name TEXT,
                    username TEXT
                )
            """)
            
            # ─────────────────────────────────────────────────────────────────
            # Health check logs table
            # ─────────────────────────────────────────────────────────────────
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS health_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    response_time REAL,
                    error_message TEXT,
                    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE
                )
            """)
            
            # ─────────────────────────────────────────────────────────────────
            # OTP logs table
            # ─────────────────────────────────────────────────────────────────
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS otp_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    otp_code TEXT NOT NULL,
                    used BOOLEAN DEFAULT FALSE,
                    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE
                )
            """)
            
            # ─────────────────────────────────────────────────────────────────
            # Create indexes for better performance
            # ─────────────────────────────────────────────────────────────────
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_accounts_phone ON accounts(phone)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_accounts_status ON accounts(status)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_health_logs_account ON health_logs(account_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_otp_logs_account ON otp_logs(account_id)
            """)
            
            conn.commit()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Account CRUD Operations - @MaiHuAryan
    # ─────────────────────────────────────────────────────────────────────────
    
    def add_account(
        self,
        label: str,
        phone: str,
        session_string: str,
        tfa_password: Optional[str] = None,
        first_name: Optional[str] = None,
        username: Optional[str] = None
    ) -> int:
        """
        Add new account to database
        Returns: account ID
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO accounts (
                    label, phone, session_string, tfa_password,
                    last_checked, first_name, username
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                label.strip(),
                format_phone(phone),
                session_string,
                tfa_password,
                get_timestamp(),
                first_name,
                username
            ))
            
            account_id = cursor.lastrowid
            conn.commit()
            return account_id
    
    def get_all_accounts(self) -> List[Dict[str, Any]]:
        """
        Get all accounts ordered by ID
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM accounts ORDER BY id ASC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_account_by_id(self, account_id: int) -> Optional[Dict[str, Any]]:
        """
        Get single account by ID
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM accounts WHERE id = ?
            """, (account_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_account_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        """
        Get account by phone number
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM accounts WHERE phone = ?
            """, (format_phone(phone),))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_active_accounts(self) -> List[Dict[str, Any]]:
        """
        Get only active accounts
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM accounts WHERE status = 'ACTIVE' ORDER BY id ASC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_failed_accounts(self) -> List[Dict[str, Any]]:
        """
        Get only failed accounts
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM accounts WHERE status = 'FAILED' ORDER BY id ASC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def update_session(
        self,
        account_id: int,
        session_string: str,
        backup_old: bool = True
    ) -> None:
        """
        Update account session string
        Optionally backs up the old session
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if backup_old:
                # Get current session for backup
                cursor.execute("""
                    SELECT session_string FROM accounts WHERE id = ?
                """, (account_id,))
                row = cursor.fetchone()
                
                if row and row['session_string']:
                    cursor.execute("""
                        UPDATE accounts 
                        SET session_backup = ?,
                            session_string = ?,
                            last_refreshed = ?,
                            updated_at = ?
                        WHERE id = ?
                    """, (
                        row['session_string'],
                        session_string,
                        get_timestamp(),
                        get_timestamp(),
                        account_id
                    ))
                else:
                    cursor.execute("""
                        UPDATE accounts 
                        SET session_string = ?,
                            last_refreshed = ?,
                            updated_at = ?
                        WHERE id = ?
                    """, (session_string, get_timestamp(), get_timestamp(), account_id))
            else:
                cursor.execute("""
                    UPDATE accounts 
                    SET session_string = ?,
                        last_refreshed = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (session_string, get_timestamp(), get_timestamp(), account_id))
            
            conn.commit()
    
    def update_status(
        self,
        account_id: int,
        status: str,
        error_msg: Optional[str] = None,
        response_time: Optional[float] = None
    ) -> None:
        """
        Update account status and log health check
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Update account status
            cursor.execute("""
                UPDATE accounts 
                SET status = ?, last_checked = ?, updated_at = ?
                WHERE id = ?
            """, (status, get_timestamp(), get_timestamp(), account_id))
            
            # Log health check
            cursor.execute("""
                INSERT INTO health_logs (account_id, status, error_message, response_time)
                VALUES (?, ?, ?, ?)
            """, (account_id, status, error_msg, response_time))
            
            conn.commit()
    
    def update_account_info(
        self,
        account_id: int,
        first_name: Optional[str] = None,
        username: Optional[str] = None
    ) -> None:
        """
        Update account profile info
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts 
                SET first_name = ?, username = ?, updated_at = ?
                WHERE id = ?
            """, (first_name, username, get_timestamp(), account_id))
            conn.commit()
    
    def update_label(self, account_id: int, label: str) -> None:
        """
        Update account label
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts SET label = ?, updated_at = ? WHERE id = ?
            """, (label.strip(), get_timestamp(), account_id))
            conn.commit()
    
    def update_tfa_password(self, account_id: int, tfa_password: str) -> None:
        """
        Update 2FA password (should be encrypted before passing)
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts SET tfa_password = ?, updated_at = ? WHERE id = ?
            """, (tfa_password, get_timestamp(), account_id))
            conn.commit()
    
    def update_notes(self, account_id: int, notes: str) -> None:
        """
        Update account notes
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts SET notes = ?, updated_at = ? WHERE id = ?
            """, (notes, get_timestamp(), account_id))
            conn.commit()
    
    def delete_account(self, account_id: int) -> bool:
        """
        Delete account and all related data
        Returns: success status
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if account exists
            cursor.execute("SELECT id FROM accounts WHERE id = ?", (account_id,))
            if not cursor.fetchone():
                return False
            
            # Delete related logs first (if not using ON DELETE CASCADE)
            cursor.execute("DELETE FROM health_logs WHERE account_id = ?", (account_id,))
            cursor.execute("DELETE FROM otp_logs WHERE account_id = ?", (account_id,))
            
            # Delete account
            cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
            
            conn.commit()
            return True
    
    def log_otp(self, account_id: int, otp_code: str) -> None:
        """
        Log received OTP
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO otp_logs (account_id, otp_code)
                VALUES (?, ?)
            """, (account_id, otp_code))
            conn.commit()
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get account statistics
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as total FROM accounts")
            total = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as active FROM accounts WHERE status = 'ACTIVE'")
            active = cursor.fetchone()['active']
            
            cursor.execute("SELECT COUNT(*) as failed FROM accounts WHERE status = 'FAILED'")
            failed = cursor.fetchone()['failed']
            
            return {
                'total': total,
                'active': active,
                'failed': failed,
                'warning': total - active - failed
            }
    
    def get_db_info(self) -> Dict[str, Any]:
        """
        Get database information
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM accounts")
            accounts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM health_logs")
            health_logs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM otp_logs")
            otp_logs = cursor.fetchone()[0]
            
            # Get database file size
            db_size = os.path.getsize(self.db_name) if os.path.exists(self.db_name) else 0
            
            return {
                'accounts': accounts,
                'health_logs': health_logs,
                'otp_logs': otp_logs,
                'db_size': db_size,
                'db_path': os.path.abspath(self.db_name)
            }
    
    def export_all(self) -> str:
        """
        Export all account data as JSON
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        accounts = self.get_all_accounts()
        export_data = {
            'version': VERSION,
            'author': AUTHOR,
            'telegram': TELEGRAM_LINK,
            'exported_at': get_timestamp(),
            'accounts': accounts
        }
        return json.dumps(export_data, indent=2, default=str)
    
    def import_all(self, data: str) -> Tuple[int, int]:
        """
        Import accounts from JSON
        Returns: (imported_count, skipped_count)
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        try:
            parsed = json.loads(data)
            accounts = parsed.get('accounts', [])
        except json.JSONDecodeError:
            # Try parsing as raw accounts list
            accounts = json.loads(data)
        
        imported = 0
        skipped = 0
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for acc in accounts:
                try:
                    # Check if phone already exists
                    phone = format_phone(acc.get('phone', ''))
                    cursor.execute("SELECT id FROM accounts WHERE phone = ?", (phone,))
                    
                    if cursor.fetchone():
                        # Update existing
                        cursor.execute("""
                            UPDATE accounts SET
                                label = ?,
                                session_string = COALESCE(?, session_string),
                                session_backup = COALESCE(?, session_backup),
                                tfa_password = COALESCE(?, tfa_password),
                                status = COALESCE(?, status),
                                notes = COALESCE(?, notes),
                                updated_at = ?
                            WHERE phone = ?
                        """, (
                            acc.get('label'),
                            acc.get('session_string'),
                            acc.get('session_backup'),
                            acc.get('tfa_password'),
                            acc.get('status'),
                            acc.get('notes'),
                            get_timestamp(),
                            phone
                        ))
                    else:
                        # Insert new
                        cursor.execute("""
                            INSERT INTO accounts (
                                label, phone, session_string, session_backup,
                                tfa_password, status, notes
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            acc.get('label', 'Imported'),
                            phone,
                            acc.get('session_string'),
                            acc.get('session_backup'),
                            acc.get('tfa_password'),
                            acc.get('status', 'ACTIVE'),
                            acc.get('notes')
                        ))
                    imported += 1
                    
                except Exception as e:
                    console.print(f"[dim]Error importing {acc.get('label')}: {e}[/dim]")
                    skipped += 1
            
            conn.commit()
        
        return imported, skipped
    
    def clear_logs(self, log_type: str = 'all') -> int:
        """
        Clear log entries
        log_type: 'otp', 'health', or 'all'
        Returns: number of rows deleted
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            deleted = 0
            
            if log_type in ('otp', 'all'):
                cursor.execute("DELETE FROM otp_logs")
                deleted += cursor.rowcount
            
            if log_type in ('health', 'all'):
                cursor.execute("DELETE FROM health_logs")
                deleted += cursor.rowcount
            
            conn.commit()
            return deleted


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6: CONFIGURATION MANAGER
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

class ConfigManager:
    """
    Handle configuration file operations
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    
    def __init__(self, config_file: str = CONFIG_FILE):
        """Initialize configuration manager"""
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file
        Creates default if not exists
        Author: @MaiHuAryan
        """
        if not os.path.exists(self.config_file):
            self._create_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
                return config
        except yaml.YAMLError as e:
            console.print(f"[red]Error parsing config: {e}[/red]")
            return {}
    
    def _create_default_config(self) -> None:
        """
        Create default configuration file
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        default_config = {
            'api_id': 'YOUR_API_ID',
            'api_hash': 'YOUR_API_HASH',
            'encryption_key': '',
            # Created by @MaiHuAryan | t.me/MaiHuAryan
        }
        
        header = """# ═══════════════════════════════════════════════════════════════════
# Telegram Account Manager - Configuration
# Created by: @MaiHuAryan | t.me/MaiHuAryan
# ═══════════════════════════════════════════════════════════════════
#
# Get your API credentials from: https://my.telegram.org/apps
#
# Support: t.me/MaiHuAryan
# ═══════════════════════════════════════════════════════════════════

"""
        
        with open(self.config_file, 'w') as f:
            f.write(header)
            yaml.dump(default_config, f, default_flow_style=False)
        
        console.print(f"[yellow]📄 Created {self.config_file}[/yellow]")
        console.print("[yellow]   Please add your API credentials![/yellow]")
        console.print(f"[dim]   Get them from: https://my.telegram.org/apps[/dim]")
        console.print(f"[dim]   Support: t.me/MaiHuAryan[/dim]")
    
    def get_api_credentials(self) -> Tuple[int, str]:
        """
        Get and validate API credentials
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        api_id = self.config.get('api_id')
        api_hash = self.config.get('api_hash')
        
        # Check if credentials are default/empty
        if api_id in ('YOUR_API_ID', None, ''):
            console.print("\n[red]╔══════════════════════════════════════════════════════════════╗[/red]")
            console.print("[red]║  ❌ API_ID not configured!                                   ║[/red]")
            console.print("[red]╠══════════════════════════════════════════════════════════════╣[/red]")
            console.print("[red]║  Please edit config.yaml and add your API credentials       ║[/red]")
            console.print("[red]║  Get them from: https://my.telegram.org/apps                ║[/red]")
            console.print("[red]║                                                              ║[/red]")
            console.print("[red]║  Support: t.me/MaiHuAryan                                   ║[/red]")
            console.print("[red]╚══════════════════════════════════════════════════════════════╝[/red]")
            sys.exit(1)
        
        if api_hash in ('YOUR_API_HASH', None, ''):
            console.print("\n[red]╔══════════════════════════════════════════════════════════════╗[/red]")
            console.print("[red]║  ❌ API_HASH not configured!                                 ║[/red]")
            console.print("[red]╠══════════════════════════════════════════════════════════════╣[/red]")
            console.print("[red]║  Please edit config.yaml and add your API credentials       ║[/red]")
            console.print("[red]║  Get them from: https://my.telegram.org/apps                ║[/red]")
            console.print("[red]║                                                              ║[/red]")
            console.print("[red]║  Support: t.me/MaiHuAryan                                   ║[/red]")
            console.print("[red]╚══════════════════════════════════════════════════════════════╝[/red]")
            sys.exit(1)
        
        try:
            api_id = int(api_id)
        except (ValueError, TypeError):
            console.print("[red]❌ API_ID must be a number![/red]")
            console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
            sys.exit(1)
        
        return api_id, str(api_hash)
    
    def get_encryption_key(self) -> str:
        """Get encryption key from config"""
        return self.config.get('encryption_key', '')
    
    def save_config(self) -> None:
        """Save current config to file"""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7: TELEGRAM CLIENT MANAGER
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

class TelegramManager:
    """
    Handle all Telegram client operations
    Manages session creation, verification, OTP listening, and refresh
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    
    def __init__(self, api_id: int, api_hash: str):
        """Initialize Telegram manager"""
        self.api_id = api_id
        self.api_hash = api_hash
    
    async def create_session(
        self,
        phone: str,
        tfa_password: Optional[str] = None
    ) -> Tuple[str, Optional[str], Optional[str], Optional[str]]:
        """
        Create new session for phone number
        
        Returns: (session_string, tfa_password_used, first_name, username)
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        client = TelegramClient(
            StringSession(),
            self.api_id,
            self.api_hash,
            device_model="TGM by @MaiHuAryan",
            system_version="1.0",
            app_version=VERSION,
        )
        
        try:
            await client.connect()
            
            # Send code request
            sent_code = await client.send_code_request(phone)
            console.print(f"\n[green]📲 OTP sent to {mask_phone(phone)}[/green]")
            console.print(f"[dim]   Code type: {sent_code.type.__class__.__name__}[/dim]")
            
            # Get OTP from user
            code = Prompt.ask("[cyan]🔢 Enter the OTP code[/cyan]")
            code = code.strip().replace(" ", "")
            
            try:
                await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                # 2FA required
                console.print("[yellow]🔐 Two-Factor Authentication required[/yellow]")
                
                if tfa_password:
                    password = tfa_password
                    console.print("[dim]   Using provided 2FA password[/dim]")
                else:
                    password = Prompt.ask(
                        "[cyan]🔐 Enter 2FA password[/cyan]",
                        password=True
                    )
                
                try:
                    await client.sign_in(password=password)
                    tfa_password = password
                except PasswordHashInvalidError:
                    raise Exception("Invalid 2FA password")
            
            # Get user info
            me = await client.get_me()
            first_name = me.first_name if me else None
            username = me.username if me else None
            
            # Get session string
            session_string = client.session.save()
            
            return session_string, tfa_password, first_name, username
            
        finally:
            await client.disconnect()
    
    async def verify_session(
        self,
        session_string: str,
        timeout: int = HEALTH_CHECK_TIMEOUT
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Verify if session is valid
        
        Returns: (is_valid, message, user_info)
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        if not session_string:
            return False, "No session string", None
        
        client = TelegramClient(
            StringSession(session_string),
            self.api_id,
            self.api_hash,
            device_model="TGM by @MaiHuAryan",
        )
        
        try:
            await asyncio.wait_for(client.connect(), timeout=timeout)
            
            if not await client.is_user_authorized():
                return False, "Session not authorized", None
            
            # Get user info
            me = await client.get_me()
            
            if not me:
                return False, "Could not get user info", None
            
            user_info = {
                'id': me.id,
                'first_name': me.first_name,
                'last_name': me.last_name,
                'username': me.username,
                'phone': me.phone,
            }
            
            name = me.first_name or me.username or "Unknown"
            return True, f"Active ({name})", user_info
            
        except AuthKeyUnregisteredError:
            return False, "Session expired/terminated", None
        except UserDeactivatedBanError:
            return False, "Account banned/deactivated", None
        except asyncio.TimeoutError:
            return False, "Connection timeout", None
        except Exception as e:
            error_msg = str(e)
            if len(error_msg) > 50:
                error_msg = error_msg[:47] + "..."
            return False, f"Error: {error_msg}", None
        finally:
            try:
                await client.disconnect()
            except Exception:
                pass
    
    async def listen_for_otp(
        self,
        session_string: str,
        callback: Optional[Callable[[str], None]] = None,
        timeout: int = OTP_TIMEOUT
    ) -> Optional[str]:
        """
        Listen for OTP messages on account
        
        Args:
            session_string: Session to listen on
            callback: Function to call when OTP received
            timeout: How long to wait in seconds
            
        Returns: OTP code or None if timeout
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        if not session_string:
            console.print("[red]❌ No session string provided![/red]")
            return None
        
        client = TelegramClient(
            StringSession(session_string),
            self.api_id,
            self.api_hash,
            device_model="TGM OTP Listener by @MaiHuAryan",
        )
        
        received_otp: Optional[str] = None
        stop_event = asyncio.Event()
        
        @client.on(events.NewMessage(from_users=TELEGRAM_OTP_SENDER))
        async def handler(event):
            nonlocal received_otp
            
            code = extract_otp_code(event.raw_text)
            if code:
                received_otp = code
                
                # Play sound notification
                play_notification_sound()
                
                # Call callback if provided
                if callback:
                    callback(code)
                
                # Signal to stop listening
                stop_event.set()
        
        try:
            await client.connect()
            
            if not await client.is_user_authorized():
                console.print("[red]❌ Session not authorized![/red]")
                console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
                return None
            
            # Start listening
            client.add_event_handler(handler)
            
            try:
                # Wait for OTP or timeout
                await asyncio.wait_for(stop_event.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                console.print("[yellow]⏰ Timeout waiting for OTP[/yellow]")
            
            return received_otp
            
        except Exception as e:
            console.print(f"[red]❌ Listener error: {e}[/red]")
            console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
            return None
        finally:
            try:
                await client.disconnect()
            except Exception:
                pass
    
    async def refresh_session(
        self,
        old_session: str,
        phone: str,
        tfa_password: Optional[str] = None,
        timeout: int = SESSION_TIMEOUT
    ) -> Optional[str]:
        """
        Create new session using old session to receive OTP automatically
        
        This is the MAGIC function that:
        1. Uses OLD session to listen for OTP
        2. Requests new login (triggers OTP)
        3. Catches OTP on old session
        4. Creates NEW session automatically
        
        Returns: new_session_string or None on failure
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        if not old_session:
            console.print("[red]❌ No old session provided![/red]")
            return None
        
        # ─────────────────────────────────────────────────────────────────────
        # Client A: Old session (OTP listener)
        # ─────────────────────────────────────────────────────────────────────
        listener_client = TelegramClient(
            StringSession(old_session),
            self.api_id,
            self.api_hash,
            device_model="TGM Listener by @MaiHuAryan",
        )
        
        # ─────────────────────────────────────────────────────────────────────
        # Client B: New session
        # ─────────────────────────────────────────────────────────────────────
        new_client = TelegramClient(
            StringSession(),
            self.api_id,
            self.api_hash,
            device_model="TGM by @MaiHuAryan",
            system_version="1.0",
            app_version=VERSION,
        )
        
        received_otp: Optional[str] = None
        otp_event = asyncio.Event()
        
        try:
            # Connect listener
            await listener_client.connect()
            
            if not await listener_client.is_user_authorized():
                console.print("[red]❌ Old session not valid for listening![/red]")
                console.print("[dim]You may need to manually re-add this account.[/dim]")
                return None
            
            # Setup OTP handler on old session
            @listener_client.on(events.NewMessage(from_users=TELEGRAM_OTP_SENDER))
            async def otp_handler(event):
                nonlocal received_otp
                code = extract_otp_code(event.raw_text)
                if code:
                    received_otp = code
                    console.print(f"\n[green]📨 OTP captured: {code}[/green]")
                    play_notification_sound()
                    otp_event.set()
            
            # Add handler
            listener_client.add_event_handler(otp_handler)
            
            # Wait a moment to ensure listener is ready
            await asyncio.sleep(0.5)
            
            # Connect new client and request login
            await new_client.connect()
            
            console.print(f"[cyan]📲 Requesting OTP for {mask_phone(phone)}...[/cyan]")
            await new_client.send_code_request(phone)
            console.print("[dim]⏳ Waiting for OTP on old session...[/dim]")
            
            # Wait for OTP
            try:
                await asyncio.wait_for(otp_event.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                console.print("[red]❌ Timeout waiting for OTP[/red]")
                console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
                return None
            
            if not received_otp:
                console.print("[red]❌ No OTP received[/red]")
                return None
            
            # Sign in with new client
            try:
                await new_client.sign_in(phone, received_otp)
            except SessionPasswordNeededError:
                if tfa_password:
                    console.print("[dim]Entering 2FA password...[/dim]")
                    try:
                        await new_client.sign_in(password=tfa_password)
                    except PasswordHashInvalidError:
                        console.print("[red]❌ Stored 2FA password is incorrect![/red]")
                        return None
                else:
                    console.print("[red]❌ 2FA required but no password stored![/red]")
                    console.print("[dim]Please update 2FA password in settings.[/dim]")
                    return None
            
            # Get new session string
            new_session = new_client.session.save()
            
            console.print("[green]✅ New session created successfully![/green]")
            return new_session
            
        except PhoneNumberInvalidError:
            console.print("[red]❌ Invalid phone number![/red]")
            return None
        except FloodWaitError as e:
            console.print(f"[red]❌ Too many attempts! Wait {e.seconds} seconds.[/red]")
            return None
        except Exception as e:
            console.print(f"[red]❌ Refresh error: {e}[/red]")
            console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
            return None
        finally:
            # Cleanup connections
            try:
                await listener_client.disconnect()
            except Exception:
                pass
            try:
                await new_client.disconnect()
            except Exception:
                pass


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8: UI COMPONENTS
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

def show_banner() -> None:
    """
    Display application banner with author credit
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    banner = """
[bold cyan]╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║            ████████╗ ██████╗ ███╗   ███╗                        ║
║            ╚══██╔══╝██╔════╝ ████╗ ████║                        ║
║               ██║   ██║  ███╗██╔████╔██║                        ║
║               ██║   ██║   ██║██║╚██╔╝██║                        ║
║               ██║   ╚██████╔╝██║ ╚═╝ ██║                        ║
║               ╚═╝    ╚═════╝ ╚═╝     ╚═╝                        ║
║                                                                  ║
║              [white]TELEGRAM ACCOUNT MANAGER v{version}[/white]                 ║
║                                                                  ║
║               [yellow]Created by: @MaiHuAryan[/yellow]                         ║
║               [dim]Telegram: t.me/MaiHuAryan[/dim]                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝[/bold cyan]
""".format(version=VERSION)
    console.print(banner)


def show_stats_bar(stats: Dict[str, int]) -> None:
    """
    Display statistics bar
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    stats_text = (
        f"[green]✅ Active: {stats['active']}[/green]  │  "
        f"[red]❌ Failed: {stats['failed']}[/red]  │  "
        f"[yellow]⚠️  Warning: {stats['warning']}[/yellow]  │  "
        f"[blue]📊 Total: {stats['total']}[/blue]"
    )
    console.print(Panel(
        stats_text,
        title="[bold]Account Status[/bold]",
        subtitle="[dim]@MaiHuAryan[/dim]",
        border_style="dim"
    ))


def show_main_menu() -> str:
    """
    Display main menu and get user choice
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    menu = """
[bold cyan]┌────────────────────────────────────────┐
│              MAIN MENU                 │
├────────────────────────────────────────┤[/bold cyan]
│                                        │
│  [bold][1][/bold]  💾  Add New Account              │
│  [bold][2][/bold]  📋  View All Accounts            │
│  [bold][3][/bold]  🎯  OTP Listener                 │
│  [bold][4][/bold]  🏥  Health Check                 │
│  [bold][5][/bold]  🔄  Refresh Sessions             │
│  [bold][6][/bold]  📤  Backup Data                  │
│  [bold][7][/bold]  📥  Restore Data                 │
│  [bold][8][/bold]  ⚙️   Settings                     │
│  [bold][0][/bold]  🚪  Exit                         │
│                                        │
[bold cyan]└────────────────────────────────────────┘[/bold cyan]
[dim]         Created by @MaiHuAryan
          t.me/MaiHuAryan[/dim]
"""
    console.print(menu)
    return Prompt.ask(
        "[bold yellow]Enter your choice[/bold yellow]",
        choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"],
        default="0"
    )


def show_account_table(accounts: List[Dict[str, Any]]) -> None:
    """
    Display accounts in a formatted table
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    if not accounts:
        console.print(Panel(
            "[yellow]No accounts found. Add one first![/yellow]\n\n"
            "[dim]Use option [1] to add your first account.[/dim]",
            title="📱 Accounts",
            subtitle="@MaiHuAryan",
            border_style="yellow"
        ))
        return
    
    table = Table(
        title="📱 Your Telegram Accounts",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        caption="[dim]Created by @MaiHuAryan | t.me/MaiHuAryan[/dim]"
    )
    
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Label", style="cyan", width=14, overflow="ellipsis")
    table.add_column("Phone", style="white", width=15)
    table.add_column("Status", width=10, justify="center")
    table.add_column("2FA", width=5, justify="center")
    table.add_column("Last Check", style="dim", width=13)
    table.add_column("Refreshed", style="dim", width=13)
    
    for acc in accounts:
        # Status styling
        status = acc.get('status', 'UNKNOWN')
        if status == 'ACTIVE':
            status_display = "[green]✅ Active[/green]"
        elif status == 'FAILED':
            status_display = "[red]❌ Failed[/red]"
        else:
            status_display = "[yellow]⚠️  Warn[/yellow]"
        
        # 2FA indicator
        tfa = "[green]✓[/green]" if acc.get('tfa_password') else "[dim]✗[/dim]"
        
        # Truncate label if too long
        label = acc.get('label', 'Unknown')[:13]
        
        table.add_row(
            str(acc['id']),
            label,
            mask_phone(acc.get('phone', '')),
            status_display,
            tfa,
            time_ago(acc.get('last_checked')),
            time_ago(acc.get('last_refreshed'))
        )
    
    console.print(table)


def show_otp_display(phone: str, code: str, label: str = "") -> None:
    """
    Display OTP in a big, visible format
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    display = f"""
[bold green]╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                        🔔 OTP RECEIVED!                          ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │                                                          │   ║
║  │                     [bold white on green]   {code}   [/bold white on green]                          │   ║
║  │                                                          │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                                                                  ║
║  📱 Account: {label[:45]:<45} ║
║  📞 Phone: {phone:<48} ║
║  ⏰ Time: {get_timestamp():<49} ║
║                                                                  ║
║  [dim]Created by @MaiHuAryan | t.me/MaiHuAryan[/dim]                        ║
╚══════════════════════════════════════════════════════════════════╝[/bold green]
"""
    console.print(display)


def show_listening_status(phone: str, label: str) -> None:
    """
    Display OTP listening status
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    display = f"""
[bold cyan]╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                      📡 OTP LISTENER ACTIVE                      ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Account: [white]{label[:50]:<50}[/white] ║
║  Phone:   [yellow]{phone:<50}[/yellow] ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │  📋 Copy this number and paste in Telegram app:          │   ║
║  │                                                          │   ║
║  │     [bold white]{phone:<46}[/bold white]     │   ║
║  │                                                          │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                                                                  ║
║  ⏳ Waiting for OTP... (Timeout: {OTP_TIMEOUT//60} minutes)                       ║
║                                                                  ║
║  [dim]Press Ctrl+C to cancel[/dim]                                        ║
║                                                                  ║
║  [dim]Created by @MaiHuAryan | t.me/MaiHuAryan[/dim]                        ║
╚══════════════════════════════════════════════════════════════════╝[/bold cyan]
"""
    console.print(display)
    
    # Try to copy phone to clipboard
    if copy_to_clipboard(phone):
        console.print("[green]📋 Phone number copied to clipboard![/green]")


def show_footer() -> None:
    """
    Display footer with author credit
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    console.print("\n[dim]─────────────────────────────────────────────────────[/dim]")
    console.print("[dim]Created by @MaiHuAryan | Telegram: t.me/MaiHuAryan[/dim]")
    console.print("[dim]─────────────────────────────────────────────────────[/dim]\n")


def wait_for_enter(message: str = "Press Enter to continue...") -> None:
    """Wait for user to press Enter"""
    Prompt.ask(f"\n[dim]{message}[/dim]", default="")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9: FEATURE IMPLEMENTATIONS
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

async def feature_add_account(db: DatabaseManager, tg: TelegramManager) -> None:
    """
    Add new account feature
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    clear_screen()
    console.print(Panel(
        "[bold cyan]💾 ADD NEW ACCOUNT[/bold cyan]\n\n"
        "[dim]Add a new Telegram account to manage[/dim]",
        subtitle="@MaiHuAryan",
        border_style="cyan"
    ))
    
    # Get phone number
    console.print("\n[bold]Step 1: Enter Phone Number[/bold]")
    phone = Prompt.ask("[cyan]📱 Phone number (with country code)[/cyan]")
    phone = format_phone(phone)
    
    # Validate phone
    is_valid, error_msg = validate_phone_number(phone)
    if not is_valid:
        console.print(f"[red]❌ {error_msg}[/red]")
        console.print("[dim]Example: +919876543210[/dim]")
        wait_for_enter()
        return
    
    # Check if already exists
    existing = db.get_account_by_phone(phone)
    if existing:
        console.print(f"[red]❌ Account with {mask_phone(phone)} already exists![/red]")
        console.print(f"[dim]Label: {existing['label']} | ID: {existing['id']}[/dim]")
        wait_for_enter()
        return
    
    # Get label
    console.print("\n[bold]Step 2: Enter Label[/bold]")
    label = Prompt.ask(
        "[cyan]🏷️  Label for this account[/cyan]",
        default=f"Account_{phone[-4:]}"
    )
    
    # Ask about 2FA
    console.print("\n[bold]Step 3: Two-Factor Authentication[/bold]")
    has_tfa = Confirm.ask(
        "[cyan]🔐 Does this account have 2FA enabled?[/cyan]",
        default=False
    )
    
    tfa_password = None
    if has_tfa:
        tfa_password = Prompt.ask(
            "[cyan]🔐 Enter 2FA password[/cyan]",
            password=True
        )
        if not tfa_password:
            console.print("[yellow]⚠️  No 2FA password provided. You'll need to enter it during login.[/yellow]")
            tfa_password = None
    
    console.print("\n[yellow]📲 Sending OTP to {phone}...[/yellow]".format(phone=mask_phone(phone)))
    console.print("[dim]This may take a few seconds...[/dim]")
    
    try:
        session_string, used_tfa, first_name, username = await tg.create_session(
            phone, tfa_password
        )
        
        # Encrypt 2FA password if provided
        encryptor = Encryptor()
        encrypted_tfa = encryptor.encrypt(used_tfa) if used_tfa else None
        
        # Save to database
        account_id = db.add_account(
            label=label,
            phone=phone,
            session_string=session_string,
            tfa_password=encrypted_tfa,
            first_name=first_name,
            username=username
        )
        
        console.print("\n[green]╔══════════════════════════════════════════════════════════════╗[/green]")
        console.print("[green]║                  ✅ ACCOUNT ADDED SUCCESSFULLY!              ║[/green]")
        console.print("[green]╠══════════════════════════════════════════════════════════════╣[/green]")
        console.print(f"[green]║  ID: {account_id:<55} ║[/green]")
        console.print(f"[green]║  Label: {label[:52]:<52} ║[/green]")
        console.print(f"[green]║  Phone: {mask_phone(phone):<52} ║[/green]")
        if first_name:
            console.print(f"[green]║  Name: {first_name[:53]:<53} ║[/green]")
        if username:
            console.print(f"[green]║  Username: @{username[:49]:<49} ║[/green]")
        console.print(f"[green]║  2FA: {'Yes' if used_tfa else 'No':<55} ║[/green]")
        console.print("[green]║                                                              ║[/green]")
        console.print("[green]║  [dim]Created by @MaiHuAryan | t.me/MaiHuAryan[/dim]                 ║[/green]")
        console.print("[green]╚══════════════════════════════════════════════════════════════╝[/green]")
        
    except PhoneCodeInvalidError:
        console.print("[red]❌ Invalid OTP code! Please try again.[/red]")
    except PhoneCodeExpiredError:
        console.print("[red]❌ OTP code expired! Please try again.[/red]")
    except PhoneNumberInvalidError:
        console.print("[red]❌ Invalid phone number format![/red]")
    except PhoneNumberBannedError:
        console.print("[red]❌ This phone number is banned from Telegram![/red]")
    except FloodWaitError as e:
        console.print(f"[red]❌ Too many attempts! Please wait {e.seconds} seconds.[/red]")
    except ApiIdInvalidError:
        console.print("[red]❌ Invalid API ID/Hash in config.yaml![/red]")
        console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
    
    wait_for_enter()


async def feature_view_accounts(db: DatabaseManager) -> None:
    """
    View all accounts feature
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    clear_screen()
    console.print(Panel(
        "[bold cyan]📋 YOUR ACCOUNTS[/bold cyan]",
        subtitle="@MaiHuAryan",
        border_style="cyan"
    ))
    
    accounts = db.get_all_accounts()
    show_account_table(accounts)
    
    if accounts:
        console.print("\n[bold]Options:[/bold]")
        console.print("  [D] Delete an account")
        console.print("  [V] View account details")
        console.print("  [Enter] Back to menu")
        
        choice = Prompt.ask("\n[cyan]Choice[/cyan]", default="").strip().lower()
        
        if choice == 'd':
            # Delete account
            try:
                acc_id = IntPrompt.ask("[cyan]Enter account ID to delete[/cyan]")
                account = db.get_account_by_id(acc_id)
                
                if account:
                    console.print(f"\n[yellow]Account: {account['label']}[/yellow]")
                    console.print(f"[yellow]Phone: {mask_phone(account['phone'])}[/yellow]")
                    
                    confirm = Confirm.ask(
                        "[red]⚠️  Are you sure you want to delete this account?[/red]",
                        default=False
                    )
                    
                    if confirm:
                        if db.delete_account(acc_id):
                            console.print("[green]✅ Account deleted successfully![/green]")
                        else:
                            console.print("[red]❌ Failed to delete account![/red]")
                else:
                    console.print("[red]❌ Account not found![/red]")
                    
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
            
            wait_for_enter()
            
        elif choice == 'v':
            # View details
            try:
                acc_id = IntPrompt.ask("[cyan]Enter account ID to view[/cyan]")
                account = db.get_account_by_id(acc_id)
                
                if account:
                    console.print("\n[bold cyan]Account Details:[/bold cyan]")
                    console.print(f"  ID: {account['id']}")
                    console.print(f"  Label: {account['label']}")
                    console.print(f"  Phone: {account['phone']}")
                    console.print(f"  Status: {account['status']}")
                    console.print(f"  Name: {account.get('first_name', 'N/A')}")
                    console.print(f"  Username: @{account.get('username', 'N/A')}")
                    console.print(f"  2FA: {'Yes' if account.get('tfa_password') else 'No'}")
                    console.print(f"  Last Check: {account.get('last_checked', 'Never')}")
                    console.print(f"  Last Refresh: {account.get('last_refreshed', 'Never')}")
                    console.print(f"  Created: {account.get('created_at', 'Unknown')}")
                    if account.get('notes'):
                        console.print(f"  Notes: {account['notes']}")
                else:
                    console.print("[red]❌ Account not found![/red]")
                    
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
            
            wait_for_enter()


async def feature_otp_listener(db: DatabaseManager, tg: TelegramManager) -> None:
    """
    OTP Listener feature
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    clear_screen()
    console.print(Panel(
        "[bold cyan]🎯 OTP LISTENER[/bold cyan]\n\n"
        "[dim]Listen for login codes on your accounts[/dim]",
        subtitle="@MaiHuAryan",
        border_style="cyan"
    ))
    
    accounts = db.get_all_accounts()
    
    if not accounts:
        console.print("[yellow]No accounts found. Add one first![/yellow]")
        wait_for_enter()
        return
    
    # Show account selection
    console.print("\n[bold]Select account to listen for OTP:[/bold]\n")
    
    console.print("[bold][0][/bold] 📡 Listen on ALL accounts (parallel)")
    console.print("")
    
    for acc in accounts:
        status_icon = "✅" if acc['status'] == 'ACTIVE' else "❌"
        console.print(f"[bold][{acc['id']}][/bold] {status_icon} {acc['label']} → {acc['phone']}")
    
    console.print("")
    choice = Prompt.ask("[cyan]Enter account ID (or 0 for all)[/cyan]", default="0")
    
    try:
        choice = int(choice)
    except ValueError:
        console.print("[red]❌ Invalid choice![/red]")
        wait_for_enter()
        return
    
    if choice == 0:
        # Listen on all accounts
        await listen_all_accounts(db, tg, accounts)
    else:
        # Listen on specific account
        account = db.get_account_by_id(choice)
        if not account:
            console.print("[red]❌ Account not found![/red]")
            wait_for_enter()
            return
        
        if account['status'] != 'ACTIVE':
            console.print("[yellow]⚠️  Warning: This account is not marked as active.[/yellow]")
            if not Confirm.ask("Continue anyway?", default=False):
                return
        
        await listen_single_account(db, tg, account)


async def listen_single_account(
    db: DatabaseManager,
    tg: TelegramManager,
    account: Dict[str, Any]
) -> None:
    """
    Listen for OTP on a single account
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    clear_screen()
    show_listening_status(account['phone'], account['label'])
    
    def on_otp_received(code: str) -> None:
        clear_screen()
        show_otp_display(account['phone'], code, account['label'])
        db.log_otp(account['id'], code)
        
        # Try to copy to clipboard
        if copy_to_clipboard(code):
            console.print("[green]📋 OTP copied to clipboard![/green]")
    
    try:
        code = await tg.listen_for_otp(
            account['session_string'],
            callback=on_otp_received,
            timeout=OTP_TIMEOUT
        )
        
        if code:
            console.print(f"\n[bold green]📋 Use this OTP: {code}[/bold green]")
            console.print(f"[dim]Logged by @MaiHuAryan's TGM[/dim]")
        else:
            console.print("\n[yellow]No OTP received within timeout.[/yellow]")
            console.print("[dim]Make sure you requested a login code in Telegram.[/dim]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️  Listener stopped by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
    
    wait_for_enter()


async def listen_all_accounts(
    db: DatabaseManager,
    tg: TelegramManager,
    accounts: List[Dict[str, Any]]
) -> None:
    """
    Listen for OTP on all accounts simultaneously
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    clear_screen()
    console.print(Panel(
        "[bold cyan]📡 LISTENING ON ALL ACCOUNTS[/bold cyan]\n\n"
        "[dim]Monitoring all accounts for OTP codes[/dim]",
        subtitle="@MaiHuAryan",
        border_style="cyan"
    ))
    
    active_accounts = [acc for acc in accounts if acc['status'] == 'ACTIVE']
    
    if not active_accounts:
        console.print("[yellow]No active accounts to listen on![/yellow]")
        console.print("[dim]Run health check to update account statuses.[/dim]")
        wait_for_enter()
        return
    
    console.print("\n[bold]Active Listeners:[/bold]")
    for acc in active_accounts:
        console.print(f"  🟢 {acc['label']} ({mask_phone(acc['phone'])})")
    
    console.print(f"\n[dim]Timeout: {OTP_TIMEOUT // 60} minutes[/dim]")
    console.print("[dim]Press Ctrl+C to stop all listeners[/dim]\n")
    
    # Create clients for all accounts
    clients = []
    stop_event = asyncio.Event()
    
    async def create_listener(account: Dict[str, Any]) -> None:
        """Create listener for single account"""
        client = TelegramClient(
            StringSession(account['session_string']),
            tg.api_id,
            tg.api_hash,
            device_model="TGM Multi-Listener by @MaiHuAryan",
        )
        
        try:
            await client.connect()
            
            if not await client.is_user_authorized():
                console.print(f"[red]❌ {account['label']}: Not authorized[/red]")
                return
            
            @client.on(events.NewMessage(from_users=TELEGRAM_OTP_SENDER))
            async def handler(event):
                code = extract_otp_code(event.raw_text)
                if code:
                    play_notification_sound()
                    console.print(f"\n[bold green]🔔 OTP for {account['label']}: {code}[/bold green]")
                    console.print(f"[dim]   Phone: {account['phone']}[/dim]")
                    console.print(f"[dim]   Time: {get_timestamp()}[/dim]")
                    db.log_otp(account['id'], code)
                    
                    if copy_to_clipboard(code):
                        console.print(f"[green]   📋 Copied to clipboard![/green]")
            
            clients.append(client)
            
            # Keep running until stop event
            while not stop_event.is_set():
                await asyncio.sleep(1)
                
        except Exception as e:
            console.print(f"[red]❌ {account['label']}: {e}[/red]")
        finally:
            try:
                await client.disconnect()
            except:
                pass
    
    try:
        # Start all listeners
        tasks = [create_listener(acc) for acc in active_accounts]
        
        # Run with timeout
        await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=OTP_TIMEOUT
        )
        
    except asyncio.TimeoutError:
        console.print("\n[yellow]⏰ Timeout reached.[/yellow]")
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️  Stopped by user.[/yellow]")
    finally:
        stop_event.set()
        # Disconnect all clients
        for client in clients:
            try:
                await client.disconnect()
            except:
                pass
    
    console.print(f"\n[dim]Listeners stopped. - @MaiHuAryan[/dim]")
    wait_for_enter()


async def feature_health_check(db: DatabaseManager, tg: TelegramManager) -> None:
    """
    Health check all accounts
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    clear_screen()
    console.print(Panel(
        "[bold cyan]🏥 HEALTH CHECK[/bold cyan]\n\n"
        "[dim]Verify all account sessions are working[/dim]",
        subtitle="@MaiHuAryan",
        border_style="cyan"
    ))
    
    accounts = db.get_all_accounts()
    
    if not accounts:
        console.print("[yellow]No accounts to check![/yellow]")
        wait_for_enter()
        return
    
    console.print(f"\n[cyan]Checking {len(accounts)} account(s)...[/cyan]\n")
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Checking...", total=len(accounts))
        
        for acc in accounts:
            progress.update(task, description=f"Checking {acc['label']}...")
            
            start_time = time.time()
            is_valid, message, user_info = await tg.verify_session(acc['session_string'])
            response_time = time.time() - start_time
            
            if is_valid:
                status = "ACTIVE"
                db.update_status(acc['id'], status, response_time=response_time)
                
                # Update user info if available
                if user_info:
                    db.update_account_info(
                        acc['id'],
                        first_name=user_info.get('first_name'),
                        username=user_info.get('username')
                    )
                
                results.append((acc['label'], acc['phone'], "✅", message, response_time))
            else:
                status = "FAILED"
                db.update_status(acc['id'], status, error_msg=message)
                results.append((acc['label'], acc['phone'], "❌", message, None))
            
            progress.advance(task)
    
    # Show results table
    console.print("\n")
    
    table = Table(
        title="Health Check Results",
        box=box.ROUNDED,
        caption="[dim]@MaiHuAryan | t.me/MaiHuAryan[/dim]"
    )
    table.add_column("Label", style="cyan")
    table.add_column("Phone", style="white")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")
    table.add_column("Time", style="dim", justify="right")
    
    for label, phone, status_icon, details, resp_time in results:
        status_style = "green" if status_icon == "✅" else "red"
        time_str = f"{resp_time:.2f}s" if resp_time else "-"
        table.add_row(
            label,
            mask_phone(phone),
            f"[{status_style}]{status_icon}[/{status_style}]",
            details[:30],
            time_str
        )
    
    console.print(table)
    
    # Summary
    active = sum(1 for r in results if r[2] == "✅")
    failed = len(results) - active
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  [green]✅ Active: {active}[/green]")
    console.print(f"  [red]❌ Failed: {failed}[/red]")
    
    if failed > 0:
        console.print("\n[yellow]⚠️  Some accounts need attention![/yellow]")
        console.print("[dim]Use 'Refresh Sessions' to try recovering failed accounts.[/dim]")
    
    show_footer()
    wait_for_enter()


async def feature_refresh_sessions(db: DatabaseManager, tg: TelegramManager) -> None:
    """
    Refresh sessions feature - auto-refresh without manual OTP entry!
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    clear_screen()
    console.print(Panel(
        "[bold cyan]🔄 REFRESH SESSIONS[/bold cyan]\n\n"
        "[dim]Create fresh sessions using existing ones to receive OTP[/dim]\n"
        "[dim]No manual OTP entry required![/dim]",
        subtitle="@MaiHuAryan",
        border_style="cyan"
    ))
    
    accounts = db.get_all_accounts()
    
    if not accounts:
        console.print("[yellow]No accounts to refresh![/yellow]")
        wait_for_enter()
        return
    
    console.print("""
[bold]Refresh Options:[/bold]

[1] 🔄 Refresh ALL accounts
[2] 🎯 Select specific accounts
[3] 🏥 Refresh FAILED accounts only
[4] 📅 Refresh OLD sessions (>30 days)
[0] ← Back
""")
    
    choice = Prompt.ask(
        "[cyan]Choice[/cyan]",
        choices=["0", "1", "2", "3", "4"],
        default="0"
    )
    
    if choice == "0":
        return
    
    accounts_to_refresh: List[Dict[str, Any]] = []
    
    if choice == "1":
        # All accounts
        accounts_to_refresh = accounts
    
    elif choice == "2":
        # Select specific accounts
        console.print("\n[bold]Select accounts (comma-separated IDs):[/bold]\n")
        for acc in accounts:
            status_icon = "✅" if acc['status'] == 'ACTIVE' else "❌"
            console.print(f"[{acc['id']}] {status_icon} {acc['label']} ({mask_phone(acc['phone'])})")
        
        ids_input = Prompt.ask("\n[cyan]Enter IDs (e.g., 1,3,5)[/cyan]")
        
        for id_str in ids_input.split(","):
            try:
                acc_id = int(id_str.strip())
                acc = db.get_account_by_id(acc_id)
                if acc:
                    accounts_to_refresh.append(acc)
            except ValueError:
                continue
                
    elif choice == "3":
        # Failed accounts only
        accounts_to_refresh = db.get_failed_accounts()
        
    elif choice == "4":
        # Old sessions (>30 days)
        for acc in accounts:
            last_refresh = acc.get('last_refreshed')
            if not last_refresh:
                accounts_to_refresh.append(acc)
                continue
            
            try:
                last_dt = datetime.strptime(str(last_refresh), "%Y-%m-%d %H:%M:%S")
                if (datetime.now() - last_dt).days > 30:
                    accounts_to_refresh.append(acc)
            except (ValueError, TypeError):
                accounts_to_refresh.append(acc)
    
    if not accounts_to_refresh:
        console.print("[yellow]No accounts match the criteria![/yellow]")
        wait_for_enter()
        return
    
    console.print(f"\n[bold]Accounts to refresh: {len(accounts_to_refresh)}[/bold]")
    for acc in accounts_to_refresh:
        console.print(f"  • {acc['label']} ({mask_phone(acc['phone'])})")
    
    if not Confirm.ask("\n[cyan]Proceed with refresh?[/cyan]", default=True):
        return
    
    console.print("\n[cyan]Starting refresh process...[/cyan]")
    console.print("[dim]This uses your existing session to catch OTP automatically![/dim]")
    console.print(f"[dim]Created by @MaiHuAryan | t.me/MaiHuAryan[/dim]\n")
    
    encryptor = Encryptor()
    success_count = 0
    fail_count = 0
    
    for i, acc in enumerate(accounts_to_refresh, 1):
        console.print(f"\n[bold]━━━ [{i}/{len(accounts_to_refresh)}] {acc['label']} ━━━[/bold]")
        console.print(f"[dim]Phone: {acc['phone']}[/dim]")
        
        # Decrypt 2FA password if available
        tfa_password = None
        if acc.get('tfa_password'):
            tfa_password = encryptor.decrypt(acc['tfa_password'])
            if tfa_password:
                console.print("[dim]2FA password found[/dim]")
        
        try:
            new_session = await tg.refresh_session(
                old_session=acc['session_string'],
                phone=acc['phone'],
                tfa_password=tfa_password,
                timeout=SESSION_TIMEOUT
            )
            
            if new_session:
                # Save new session (backup old one)
                db.update_session(acc['id'], new_session, backup_old=True)
                db.update_status(acc['id'], 'ACTIVE')
                
                console.print(f"[green]✅ {acc['label']} - Refreshed successfully![/green]")
                success_count += 1
            else:
                console.print(f"[red]❌ {acc['label']} - Refresh failed![/red]")
                fail_count += 1
                
        except Exception as e:
            console.print(f"[red]❌ {acc['label']} - Error: {e}[/red]")
            fail_count += 1
        
        # Small delay between accounts to avoid flood
        if i < len(accounts_to_refresh):
            console.print("[dim]Waiting 3 seconds before next account...[/dim]")
            await asyncio.sleep(3)
    
    # Summary
    console.print("\n")
    console.print("[bold cyan]╔══════════════════════════════════════════════════════════════╗[/bold cyan]")
    console.print("[bold cyan]║                    REFRESH COMPLETE                          ║[/bold cyan]")
    console.print("[bold cyan]╠══════════════════════════════════════════════════════════════╣[/bold cyan]")
    console.print(f"[bold cyan]║  [green]✅ Success: {success_count:<47}[/green] ║[/bold cyan]")
    console.print(f"[bold cyan]║  [red]❌ Failed: {fail_count:<48}[/red] ║[/bold cyan]")
    console.print("[bold cyan]║                                                              ║[/bold cyan]")
    console.print("[bold cyan]║  [dim]@MaiHuAryan | t.me/MaiHuAryan[/dim]                            ║[/bold cyan]")
    console.print("[bold cyan]╚══════════════════════════════════════════════════════════════╝[/bold cyan]")
    
    wait_for_enter()


def feature_backup(db: DatabaseManager) -> None:
    """
    Backup data feature - encrypted export
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    clear_screen()
    console.print(Panel(
        "[bold cyan]📤 BACKUP DATA[/bold cyan]\n\n"
        "[dim]Export all accounts with encrypted sessions[/dim]",
        subtitle="@MaiHuAryan",
        border_style="cyan"
    ))
    
    accounts = db.get_all_accounts()
    
    if not accounts:
        console.print("[yellow]No accounts to backup![/yellow]")
        wait_for_enter()
        return
    
    console.print(f"\n[bold]Accounts to backup: {len(accounts)}[/bold]\n")
    
    # Create backup directory
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Get password for encryption
    console.print("[bold]Set backup password:[/bold]")
    console.print("[dim]This password will be needed to restore the backup.[/dim]\n")
    
    password = Prompt.ask("[cyan]🔐 Enter backup password[/cyan]", password=True)
    
    if not password:
        console.print("[red]❌ Password cannot be empty![/red]")
        wait_for_enter()
        return
    
    confirm_password = Prompt.ask("[cyan]🔐 Confirm password[/cyan]", password=True)
    
    if password != confirm_password:
        console.print("[red]❌ Passwords don't match![/red]")
        wait_for_enter()
        return
    
    console.print("\n[cyan]Creating backup...[/cyan]")
    
    try:
        # Export data
        data = db.export_all()
        
        # Encrypt with provided password
        encryptor = Encryptor(password)
        encrypted_data = encryptor.encrypt(data)
        
        if not encrypted_data:
            console.print("[red]❌ Encryption failed![/red]")
            wait_for_enter()
            return
        
        # Generate filename
        filename = f"tgm_backup_{get_date_string()}.enc"
        filepath = os.path.join(BACKUP_DIR, filename)
        
        # Save backup
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(encrypted_data)
        
        # Get file size
        file_size = os.path.getsize(filepath)
        file_size_kb = file_size / 1024
        
        console.print("\n[green]╔══════════════════════════════════════════════════════════════╗[/green]")
        console.print("[green]║                  ✅ BACKUP CREATED!                          ║[/green]")
        console.print("[green]╠══════════════════════════════════════════════════════════════╣[/green]")
        console.print(f"[green]║  File: {filename[:52]:<52} ║[/green]")
        console.print(f"[green]║  Size: {file_size_kb:.2f} KB{' ':<49} ║[/green]")
        console.print(f"[green]║  Accounts: {len(accounts):<49} ║[/green]")
        console.print(f"[green]║  Path: {BACKUP_DIR}/{' ':<51} ║[/green]")
        console.print("[green]║                                                              ║[/green]")
        console.print("[green]║  ⚠️  Keep this file and password safe!                       ║[/green]")
        console.print("[green]║                                                              ║[/green]")
        console.print("[green]║  [dim]@MaiHuAryan | t.me/MaiHuAryan[/dim]                            ║[/green]")
        console.print("[green]╚══════════════════════════════════════════════════════════════╝[/green]")
        
        console.print("\n[yellow]📋 Backup Tips:[/yellow]")
        console.print("  • Upload to Google Drive or Dropbox")
        console.print("  • Email to yourself")
        console.print("  • Save password in a password manager")
        console.print(f"\n[dim]Support: t.me/MaiHuAryan[/dim]")
        
    except Exception as e:
        console.print(f"[red]❌ Backup failed: {e}[/red]")
        console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
    
    wait_for_enter()


def feature_restore(db: DatabaseManager) -> None:
    """
    Restore data feature - import encrypted backup
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    clear_screen()
    console.print(Panel(
        "[bold cyan]📥 RESTORE DATA[/bold cyan]\n\n"
        "[dim]Import accounts from encrypted backup[/dim]",
        subtitle="@MaiHuAryan",
        border_style="cyan"
    ))
    
    # Check if backup directory exists
    if not os.path.exists(BACKUP_DIR):
        console.print("[yellow]No backup directory found![/yellow]")
        console.print(f"[dim]Expected location: {BACKUP_DIR}/[/dim]")
        wait_for_enter()
        return
    
    # List available backups
    backups = sorted([
        f for f in os.listdir(BACKUP_DIR) 
        if f.endswith('.enc')
    ], reverse=True)
    
    if not backups:
        console.print("[yellow]No backup files found![/yellow]")
        console.print(f"[dim]Place .enc files in: {BACKUP_DIR}/[/dim]")
        wait_for_enter()
        return
    
    console.print("\n[bold]Available Backups:[/bold]\n")
    
    for i, backup in enumerate(backups, 1):
        filepath = os.path.join(BACKUP_DIR, backup)
        size = os.path.getsize(filepath) / 1024
        console.print(f"[{i}] {backup} ({size:.2f} KB)")
    
    console.print("")
    
    try:
        choice = IntPrompt.ask(
            "[cyan]Select backup number[/cyan]",
            default=1
        )
        
        if choice < 1 or choice > len(backups):
            console.print("[red]❌ Invalid selection![/red]")
            wait_for_enter()
            return
        
        selected_backup = backups[choice - 1]
        filepath = os.path.join(BACKUP_DIR, selected_backup)
        
    except Exception:
        console.print("[red]❌ Invalid input![/red]")
        wait_for_enter()
        return
    
    # Get decryption password
    password = Prompt.ask("\n[cyan]🔐 Enter backup password[/cyan]", password=True)
    
    if not password:
        console.print("[red]❌ Password required![/red]")
        wait_for_enter()
        return
    
    console.print("\n[cyan]Restoring backup...[/cyan]")
    
    try:
        # Read encrypted data
        with open(filepath, 'r', encoding='utf-8') as f:
            encrypted_data = f.read()
        
        # Decrypt
        encryptor = Encryptor(password)
        decrypted_data = encryptor.decrypt(encrypted_data)
        
        if not decrypted_data:
            console.print("[red]❌ Decryption failed! Wrong password?[/red]")
            wait_for_enter()
            return
        
        # Confirm before importing
        console.print("\n[yellow]⚠️  This will merge backup data with existing accounts.[/yellow]")
        console.print("[dim]Existing accounts with same phone will be updated.[/dim]")
        
        if not Confirm.ask("\n[cyan]Continue with restore?[/cyan]", default=True):
            return
        
        # Import data
        imported, skipped = db.import_all(decrypted_data)
        
        console.print("\n[green]╔══════════════════════════════════════════════════════════════╗[/green]")
        console.print("[green]║                  ✅ RESTORE COMPLETE!                        ║[/green]")
        console.print("[green]╠══════════════════════════════════════════════════════════════╣[/green]")
        console.print(f"[green]║  Imported/Updated: {imported:<41} ║[/green]")
        console.print(f"[green]║  Skipped: {skipped:<50} ║[/green]")
        console.print("[green]║                                                              ║[/green]")
        console.print("[green]║  [dim]@MaiHuAryan | t.me/MaiHuAryan[/dim]                            ║[/green]")
        console.print("[green]╚══════════════════════════════════════════════════════════════╝[/green]")
        
        console.print("\n[cyan]Run Health Check to verify restored accounts.[/cyan]")
        
    except json.JSONDecodeError:
        console.print("[red]❌ Invalid backup file format![/red]")
    except Exception as e:
        console.print(f"[red]❌ Restore failed: {e}[/red]")
        console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
    
    wait_for_enter()


async def feature_settings(db: DatabaseManager, config: ConfigManager) -> None:
    """
    Settings feature
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    while True:
        clear_screen()
        console.print(Panel(
            "[bold cyan]⚙️  SETTINGS[/bold cyan]\n\n"
            "[dim]Configure application settings[/dim]",
            subtitle="@MaiHuAryan",
            border_style="cyan"
        ))
        
        console.print("""
[bold]Options:[/bold]

[1] 🔑 View API Credentials
[2] 🔐 Update 2FA Password for Account
[3] 📝 Edit Account Label
[4] 📋 Add Notes to Account
[5] 💾 Database Information
[6] 🧹 Clear Logs
[7] 📱 About
[0] ← Back to Main Menu
""")
        
        choice = Prompt.ask(
            "[cyan]Choice[/cyan]",
            choices=["0", "1", "2", "3", "4", "5", "6", "7"],
            default="0"
        )
        
        if choice == "0":
            break
            
        elif choice == "1":
            # View API credentials
            api_id, api_hash = config.get_api_credentials()
            console.print("\n[bold]API Credentials:[/bold]")
            console.print(f"  API ID: {api_id}")
            console.print(f"  API Hash: {api_hash[:8]}{'*' * 20}{api_hash[-4:]}")
            console.print(f"\n[dim]Edit config.yaml to change these.[/dim]")
            console.print(f"[dim]Get from: https://my.telegram.org/apps[/dim]")
            wait_for_enter()
            
        elif choice == "2":
            # Update 2FA password
            accounts = db.get_all_accounts()
            if not accounts:
                console.print("[yellow]No accounts found![/yellow]")
                wait_for_enter()
                continue
            
            show_account_table(accounts)
            
            try:
                acc_id = IntPrompt.ask("\n[cyan]Enter account ID[/cyan]")
                account = db.get_account_by_id(acc_id)
                
                if not account:
                    console.print("[red]❌ Account not found![/red]")
                    wait_for_enter()
                    continue
                
                console.print(f"\n[bold]Account: {account['label']}[/bold]")
                console.print(f"[dim]Phone: {mask_phone(account['phone'])}[/dim]")
                
                current_tfa = "Set" if account.get('tfa_password') else "Not set"
                console.print(f"[dim]Current 2FA: {current_tfa}[/dim]")
                
                new_password = Prompt.ask(
                    "\n[cyan]Enter new 2FA password (or leave empty to remove)[/cyan]",
                    password=True,
                    default=""
                )
                
                encryptor = Encryptor()
                if new_password:
                    encrypted = encryptor.encrypt(new_password)
                    db.update_tfa_password(account['id'], encrypted)
                    console.print("[green]✅ 2FA password updated![/green]")
                else:
                    db.update_tfa_password(account['id'], "")
                    console.print("[yellow]2FA password removed.[/yellow]")
                    
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
            
            wait_for_enter()
            
        elif choice == "3":
            # Edit label
            accounts = db.get_all_accounts()
            if not accounts:
                console.print("[yellow]No accounts found![/yellow]")
                wait_for_enter()
                continue
            
            show_account_table(accounts)
            
            try:
                acc_id = IntPrompt.ask("\n[cyan]Enter account ID[/cyan]")
                account = db.get_account_by_id(acc_id)
                
                if not account:
                    console.print("[red]❌ Account not found![/red]")
                    wait_for_enter()
                    continue
                
                console.print(f"\n[bold]Current label: {account['label']}[/bold]")
                
                new_label = Prompt.ask(
                    "[cyan]Enter new label[/cyan]",
                    default=account['label']
                )
                
                if new_label and new_label != account['label']:
                    db.update_label(account['id'], new_label)
                    console.print("[green]✅ Label updated![/green]")
                else:
                    console.print("[yellow]No changes made.[/yellow]")
                    
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
            
            wait_for_enter()
            
        elif choice == "4":
            # Add notes
            accounts = db.get_all_accounts()
            if not accounts:
                console.print("[yellow]No accounts found![/yellow]")
                wait_for_enter()
                continue
            
            show_account_table(accounts)
            
            try:
                acc_id = IntPrompt.ask("\n[cyan]Enter account ID[/cyan]")
                account = db.get_account_by_id(acc_id)
                
                if not account:
                    console.print("[red]❌ Account not found![/red]")
                    wait_for_enter()
                    continue
                
                console.print(f"\n[bold]Account: {account['label']}[/bold]")
                if account.get('notes'):
                    console.print(f"[dim]Current notes: {account['notes']}[/dim]")
                
                new_notes = Prompt.ask(
                    "[cyan]Enter notes[/cyan]",
                    default=account.get('notes', '')
                )
                
                db.update_notes(account['id'], new_notes)
                console.print("[green]✅ Notes updated![/green]")
                    
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
            
            wait_for_enter()
            
        elif choice == "5":
            # Database info
            db_info = db.get_db_info()
            
            console.print("\n[bold]Database Information:[/bold]")
            console.print(f"  📁 Path: {db_info['db_path']}")
            console.print(f"  💾 Size: {db_info['db_size'] / 1024:.2f} KB")
            console.print(f"  👤 Accounts: {db_info['accounts']}")
            console.print(f"  🏥 Health Logs: {db_info['health_logs']}")
            console.print(f"  📨 OTP Logs: {db_info['otp_logs']}")
            console.print(f"\n[dim]@MaiHuAryan | t.me/MaiHuAryan[/dim]")
            
            wait_for_enter()
            
        elif choice == "6":
            # Clear logs
            console.print("\n[bold]Clear Logs:[/bold]\n")
            console.print("[1] Clear OTP logs only")
            console.print("[2] Clear Health logs only")
            console.print("[3] Clear ALL logs")
            console.print("[0] Cancel")
            
            log_choice = Prompt.ask("\n[cyan]Choice[/cyan]", choices=["0", "1", "2", "3"], default="0")
            
            if log_choice == "0":
                continue
            
            if Confirm.ask("[yellow]Are you sure?[/yellow]", default=False):
                if log_choice == "1":
                    deleted = db.clear_logs('otp')
                elif log_choice == "2":
                    deleted = db.clear_logs('health')
                else:
                    deleted = db.clear_logs('all')
                
                console.print(f"[green]✅ Deleted {deleted} log entries.[/green]")
            
            wait_for_enter()
            
        elif choice == "7":
            # About
            console.print("\n")
            console.print("[bold cyan]╔══════════════════════════════════════════════════════════════╗[/bold cyan]")
            console.print("[bold cyan]║                        ABOUT                                 ║[/bold cyan]")
            console.print("[bold cyan]╠══════════════════════════════════════════════════════════════╣[/bold cyan]")
            console.print("[bold cyan]║                                                              ║[/bold cyan]")
            console.print("[bold cyan]║      ████████╗ ██████╗ ███╗   ███╗                          ║[/bold cyan]")
            console.print("[bold cyan]║      ╚══██╔══╝██╔════╝ ████╗ ████║                          ║[/bold cyan]")
            console.print("[bold cyan]║         ██║   ██║  ███╗██╔████╔██║                          ║[/bold cyan]")
            console.print("[bold cyan]║         ██║   ██║   ██║██║╚██╔╝██║                          ║[/bold cyan]")
            console.print("[bold cyan]║         ██║   ╚██████╔╝██║ ╚═╝ ██║                          ║[/bold cyan]")
            console.print("[bold cyan]║         ╚═╝    ╚═════╝ ╚═╝     ╚═╝                          ║[/bold cyan]")
            console.print("[bold cyan]║                                                              ║[/bold cyan]")
            console.print("[bold cyan]║      TELEGRAM ACCOUNT MANAGER                               ║[/bold cyan]")
            console.print("[bold cyan]║                                                              ║[/bold cyan]")
            console.print(f"[bold cyan]║      Version: {VERSION:<45} ║[/bold cyan]")
            console.print(f"[bold cyan]║      Author: {AUTHOR:<46} ║[/bold cyan]")
            console.print(f"[bold cyan]║      Telegram: {TELEGRAM_LINK:<44} ║[/bold cyan]")
            console.print("[bold cyan]║                                                              ║[/bold cyan]")
            console.print("[bold cyan]║      Features:                                              ║[/bold cyan]")
            console.print("[bold cyan]║      • Multi-account session management                     ║[/bold cyan]")
            console.print("[bold cyan]║      • OTP listener for login codes                         ║[/bold cyan]")
            console.print("[bold cyan]║      • Auto session refresh (no manual OTP!)                ║[/bold cyan]")
            console.print("[bold cyan]║      • Health monitoring & status tracking                  ║[/bold cyan]")
            console.print("[bold cyan]║      • Encrypted backup/restore                             ║[/bold cyan]")
            console.print("[bold cyan]║                                                              ║[/bold cyan]")
            console.print("[bold cyan]║      Support: t.me/MaiHuAryan                               ║[/bold cyan]")
            console.print("[bold cyan]║                                                              ║[/bold cyan]")
            console.print("[bold cyan]╚══════════════════════════════════════════════════════════════╝[/bold cyan]")
            
            wait_for_enter()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 10: MAIN APPLICATION CLASS
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

class Application:
    """
    Main application class - orchestrates all features
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    
    def __init__(self):
        """Initialize the application"""
        self.config = ConfigManager()
        self.db = DatabaseManager()
        
        # Get API credentials
        api_id, api_hash = self.config.get_api_credentials()
        self.tg = TelegramManager(api_id, api_hash)
        
        # Setup signal handlers for graceful shutdown
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self) -> None:
        """Setup handlers for graceful shutdown"""
        def signal_handler(sig, frame):
            console.print("\n\n[yellow]👋 Shutting down gracefully...[/yellow]")
            console.print(f"[dim]Thanks for using TGM by @MaiHuAryan[/dim]")
            sys.exit(0)
        
        try:
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        except (OSError, AttributeError):
            # Signal handling not available on all platforms
            pass
    
    def run(self) -> None:
        """
        Main application loop
        Author: @MaiHuAryan | t.me/MaiHuAryan
        """
        while True:
            try:
                clear_screen()
                show_banner()
                
                # Show stats if we have accounts
                stats = self.db.get_stats()
                if stats['total'] > 0:
                    show_stats_bar(stats)
                
                # Show menu and get choice
                choice = show_main_menu()
                
                # Handle choice
                if choice == "0":
                    # Exit
                    clear_screen()
                    console.print("\n[bold cyan]╔══════════════════════════════════════════════════════════════╗[/bold cyan]")
                    console.print("[bold cyan]║                                                              ║[/bold cyan]")
                    console.print("[bold cyan]║                👋 GOODBYE! STAY SAFE!                       ║[/bold cyan]")
                    console.print("[bold cyan]║                                                              ║[/bold cyan]")
                    console.print("[bold cyan]║           Thanks for using Telegram Account Manager         ║[/bold cyan]")
                    console.print("[bold cyan]║                                                              ║[/bold cyan]")
                    console.print("[bold cyan]║                  Created by @MaiHuAryan                     ║[/bold cyan]")
                    console.print("[bold cyan]║                  Telegram: t.me/MaiHuAryan                  ║[/bold cyan]")
                    console.print("[bold cyan]║                                                              ║[/bold cyan]")
                    console.print("[bold cyan]╚══════════════════════════════════════════════════════════════╝[/bold cyan]\n")
                    break
                
                elif choice == "1":
                    asyncio.run(feature_add_account(self.db, self.tg))
                
                elif choice == "2":
                    asyncio.run(feature_view_accounts(self.db))
                
                elif choice == "3":
                    asyncio.run(feature_otp_listener(self.db, self.tg))
                
                elif choice == "4":
                    asyncio.run(feature_health_check(self.db, self.tg))
                
                elif choice == "5":
                    asyncio.run(feature_refresh_sessions(self.db, self.tg))
                
                elif choice == "6":
                    feature_backup(self.db)
                
                elif choice == "7":
                    feature_restore(self.db)
                
                elif choice == "8":
                    asyncio.run(feature_settings(self.db, self.config))
                    
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully in menu
                continue
            except Exception as e:
                console.print(f"\n[red]❌ Unexpected error: {e}[/red]")
                console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
                wait_for_enter()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 11: COMMAND LINE INTERFACE
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

def print_cli_help() -> None:
    """Print CLI help message"""
    help_text = """
╔══════════════════════════════════════════════════════════════════╗
║                TELEGRAM ACCOUNT MANAGER                          ║
║                Created by: @MaiHuAryan                           ║
║                Telegram: t.me/MaiHuAryan                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Usage: python tgm.py [options]                                  ║
║                                                                  ║
║  Options:                                                        ║
║    --help, -h       Show this help message                       ║
║    --version, -v    Show version                                 ║
║    --backup         Quick backup (will prompt for password)      ║
║    --health         Quick health check                           ║
║                                                                  ║
║  Normal usage:                                                   ║
║    python tgm.py                                                 ║
║                                                                  ║
║  Support: t.me/MaiHuAryan                                       ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(help_text)


def print_version() -> None:
    """Print version information"""
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  Telegram Account Manager v{VERSION}                              ║
║  Created by: {AUTHOR}                                         ║
║  Telegram: {TELEGRAM_LINK}                                     ║
╚══════════════════════════════════════════════════════════════════╝
""")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 12: ENTRY POINT
# Author: @MaiHuAryan | t.me/MaiHuAryan
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """
    Application entry point
    Author: @MaiHuAryan | t.me/MaiHuAryan
    """
    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ('--help', '-h'):
            print_cli_help()
            return
        
        if arg in ('--version', '-v'):
            print_version()
            return
        
        if arg == '--backup':
            # Quick backup
            db = DatabaseManager()
            feature_backup(db)
            return
        
        if arg == '--health':
            # Quick health check
            config = ConfigManager()
            api_id, api_hash = config.get_api_credentials()
            db = DatabaseManager()
            tg = TelegramManager(api_id, api_hash)
            asyncio.run(feature_health_check(db, tg))
            return
    
    # Normal startup
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted![/yellow]")
        console.print(f"[dim]@MaiHuAryan | t.me/MaiHuAryan[/dim]")
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]")
        console.print(f"[dim]Support: t.me/MaiHuAryan[/dim]")
        sys.exit(1)


# ══════════════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()


# ══════════════════════════════════════════════════════════════════════════════
#
#                              END OF FILE
#
#                    Created by: @MaiHuAryan
#                    Telegram: t.me/MaiHuAryan
#
#                    Thank you for using TGM!
#
# ══════════════════════════════════════════════════════════════════════════════
