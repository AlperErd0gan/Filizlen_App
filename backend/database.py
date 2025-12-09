"""
Veritabanı bağlantısı ve yardımcı fonksiyonlar
"""

import sqlite3
import os
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

# Veritabanı dosya yolu
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database.db")

@contextmanager
def get_db_connection():
    """Veritabanı bağlantısı context manager"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Sözlük benzeri erişim için
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def dict_factory(cursor, row):
    """Satırları sözlük olarak döndür"""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# ========== NEWS (Haberler) Fonksiyonları ==========

def get_all_news(limit: Optional[int] = None, category_id: Optional[int] = None) -> List[Dict]:
    """Tüm haberleri getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT n.*, nc.name as category_name 
            FROM news n
            LEFT JOIN news_categories nc ON n.category_id = nc.id
        """
        params = []
        
        if category_id:
            query += " WHERE n.category_id = ?"
            params.append(category_id)
        
        query += " ORDER BY n.published_at DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_news_by_id(news_id: int) -> Optional[Dict]:
    """ID'ye göre haber getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT n.*, nc.name as category_name 
            FROM news n
            LEFT JOIN news_categories nc ON n.category_id = nc.id
            WHERE n.id = ?
        """, (news_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def add_news(title: str, summary: str, content: str, category_id: int, 
             image_url: Optional[str] = None) -> int:
    """Yeni haber ekle"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO news (title, summary, content, category_id, image_url)
            VALUES (?, ?, ?, ?, ?)
        """, (title, summary, content, category_id, image_url))
        return cursor.lastrowid

def update_news(news_id: int, title: Optional[str] = None, 
                summary: Optional[str] = None, content: Optional[str] = None,
                category_id: Optional[int] = None, image_url: Optional[str] = None) -> bool:
    """Haber güncelle"""
    updates = []
    params = []
    
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if summary is not None:
        updates.append("summary = ?")
        params.append(summary)
    if content is not None:
        updates.append("content = ?")
        params.append(content)
    if category_id is not None:
        updates.append("category_id = ?")
        params.append(category_id)
    if image_url is not None:
        updates.append("image_url = ?")
        params.append(image_url)
    
    if not updates:
        return False
    
    params.append(news_id)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE news SET {', '.join(updates)} WHERE id = ?
        """, params)
        return cursor.rowcount > 0

def delete_news(news_id: int) -> bool:
    """Haber sil"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM news WHERE id = ?", (news_id,))
        return cursor.rowcount > 0

# ========== TIPS Fonksiyonları ==========

def get_all_tips(limit: Optional[int] = None, difficulty: Optional[str] = None) -> List[Dict]:
    """Tüm tips'leri getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM tips WHERE 1=1"
        params = []
        
        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty)
        
        query += " ORDER BY created_at DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_tip_by_id(tip_id: int) -> Optional[Dict]:
    """ID'ye göre tip getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tips WHERE id = ?", (tip_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def add_tip(title: str, content: str, difficulty: Optional[str] = None) -> int:
    """Yeni tip ekle"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tips (title, content, difficulty)
            VALUES (?, ?, ?)
        """, (title, content, difficulty))
        return cursor.lastrowid

def update_tip(tip_id: int, title: Optional[str] = None, 
               content: Optional[str] = None, difficulty: Optional[str] = None) -> bool:
    """Tip güncelle"""
    updates = []
    params = []
    
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if content is not None:
        updates.append("content = ?")
        params.append(content)
    if difficulty is not None:
        updates.append("difficulty = ?")
        params.append(difficulty)
    
    if not updates:
        return False
    
    params.append(tip_id)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE tips SET {', '.join(updates)} WHERE id = ?
        """, params)
        return cursor.rowcount > 0

def delete_tip(tip_id: int) -> bool:
    """Tip sil"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tips WHERE id = ?", (tip_id,))
        return cursor.rowcount > 0

# ========== NEWS CATEGORIES Fonksiyonları ==========

def get_all_categories() -> List[Dict]:
    """Tüm kategorileri getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news_categories ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]

def get_category_by_id(category_id: int) -> Optional[Dict]:
    """ID'ye göre kategori getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news_categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def add_category(name: str, description: Optional[str] = None) -> int:
    """Yeni kategori ekle"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO news_categories (name, description)
            VALUES (?, ?)
        """, (name, description))
        return cursor.lastrowid

# ========== USERS Fonksiyonları ==========

def get_user_by_email(email: str) -> Optional[Dict]:
    """Email'e göre kullanıcı getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """ID'ye göre kullanıcı getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

# ========== CHAT LOG Fonksiyonları ==========

def add_chat_log(user_id: int, user_message: str, bot_response: str) -> int:
    """Chat log ekle"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_log (user_id, user_message, bot_response)
            VALUES (?, ?, ?)
        """, (user_id, user_message, bot_response))
        return cursor.lastrowid

def get_user_chat_logs(user_id: int, limit: Optional[int] = None) -> List[Dict]:
    """Kullanıcının chat loglarını getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM chat_log WHERE user_id = ? ORDER BY created_at DESC"
        params = [user_id]
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

# ========== SEARCH HISTORY Fonksiyonları ==========

def add_search_history(user_id: int, query: str) -> int:
    """Arama geçmişi ekle"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO search_history (user_id, query)
            VALUES (?, ?)
        """, (user_id, query))
        return cursor.lastrowid

def get_user_search_history(user_id: int, limit: Optional[int] = None) -> List[Dict]:
    """Kullanıcının arama geçmişini getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM search_history WHERE user_id = ? ORDER BY created_at DESC"
        params = [user_id]
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

# ========== FAVORITE NEWS Fonksiyonları ==========

def add_favorite_news(user_id: int, news_id: int) -> int:
    """Favori haber ekle"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO favorite_news (user_id, news_id)
                VALUES (?, ?)
            """, (user_id, news_id))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Zaten favori olarak eklenmiş
            return -1

def remove_favorite_news(user_id: int, news_id: int) -> bool:
    """Favori haberden çıkar"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM favorite_news WHERE user_id = ? AND news_id = ?
        """, (user_id, news_id))
        return cursor.rowcount > 0

def get_user_favorites(user_id: int) -> List[Dict]:
    """Kullanıcının favori haberlerini getir"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT n.*, nc.name as category_name, fn.created_at as favorited_at
            FROM favorite_news fn
            JOIN news n ON fn.news_id = n.id
            LEFT JOIN news_categories nc ON n.category_id = nc.id
            WHERE fn.user_id = ?
            ORDER BY fn.created_at DESC
        """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]

def is_news_favorited(user_id: int, news_id: int) -> bool:
    """Haber favori mi kontrol et"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM favorite_news 
            WHERE user_id = ? AND news_id = ?
        """, (user_id, news_id))
        return cursor.fetchone()[0] > 0

