"""
SQLite Veritabanı Başlatma Scripti
ERD'ye göre tüm tabloları oluşturur
"""

import sqlite3
import os
from datetime import datetime

# Veritabanı dosya yolu
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database.db")

def init_database():
    """Veritabanını oluştur ve tüm tabloları kur"""
    
    # Veritabanı bağlantısı oluştur
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. users tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. tips tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                difficulty VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 3. news_categories tablosu (news tablosundan önce oluşturulmalı)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                description VARCHAR(500)
            )
        """)
        
        # 4. news tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                summary VARCHAR(500),
                content TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                image_url VARCHAR(500),
                FOREIGN KEY (category_id) REFERENCES news_categories(id)
            )
        """)
        
        # 5. search_history tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                query VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # 6. chat_log tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # 7. favorite_news tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorite_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                news_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (news_id) REFERENCES news(id),
                UNIQUE(user_id, news_id)
            )
        """)
        
        # İndeksler oluştur (performans için)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_category ON news(category_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_user ON search_history(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_user ON chat_log(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fav_user ON favorite_news(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fav_news ON favorite_news(news_id)")
        
        # Değişiklikleri kaydet
        conn.commit()
        
        print(f"✅ Veritabanı başarıyla oluşturuldu: {DB_PATH}")
        print("📋 Oluşturulan tablolar:")
        print("   - users")
        print("   - tips")
        print("   - news_categories")
        print("   - news")
        print("   - search_history")
        print("   - chat_log")
        print("   - favorite_news")
        
        # Örnek veri ekleme (opsiyonel - test için)
        add_sample_data(cursor, conn)
        
    except sqlite3.Error as e:
        print(f"❌ Veritabanı hatası: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def add_sample_data(cursor, conn):
    """Örnek veri ekle (opsiyonel)"""
    
    # Örnek haber kategorileri
    categories = [
        ("Tarım Haberleri", "Genel tarım haberleri ve gelişmeler"),
        ("Teknoloji", "Tarım teknolojileri ve yenilikler"),
        ("Pazar", "Tarım ürünleri fiyatları ve pazar haberleri"),
        ("İklim", "Hava durumu ve iklim değişiklikleri")
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO news_categories (name, description) 
        VALUES (?, ?)
    """, categories)
    
    # Örnek tips
    sample_tips = [
        ("Domates Yetiştirme", "Domates bitkileri için düzenli sulama ve güneş ışığı çok önemlidir. Toprağın nemli kalmasına dikkat edin.", "Kolay"),
        ("Gübreleme Zamanı", "Bitkileriniz için en iyi gübreleme zamanı ilkbahar başlangıcıdır. Organik gübre kullanmayı tercih edin.", "Orta"),
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO tips (title, content, difficulty) 
        VALUES (?, ?, ?)
    """, sample_tips)
    
    conn.commit()
    print("📝 Örnek veriler eklendi (kategoriler ve tips)")

if __name__ == "__main__":
    print("🚀 Veritabanı başlatılıyor...")
    init_database()
    print("✨ Tamamlandı!")

