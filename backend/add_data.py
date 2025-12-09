"""
Manuel Veri Ekleme Scripti
Haberler ve tips eklemek için kullanılabilir
"""

import sys
import os

# Backend modülünü import edebilmek için path ekle
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

import database

def add_news_interactive():
    """İnteraktif olarak haber ekle"""
    print("\n=== YENİ HABER EKLE ===")
    
    # Kategorileri listele
    categories = database.get_all_categories()
    if not categories:
        print("⚠️  Henüz kategori yok! Önce kategori ekleyin.")
        return
    
    print("\nMevcut Kategoriler:")
    for cat in categories:
        print(f"  {cat['id']}. {cat['name']}")
    
    # Kullanıcıdan bilgileri al
    try:
        category_id = int(input("\nKategori ID: "))
        
        # Kategori var mı kontrol et
        category = database.get_category_by_id(category_id)
        if not category:
            print("❌ Geçersiz kategori ID!")
            return
        
        title = input("Başlık: ")
        summary = input("Özet: ")
        print("İçerik (Çok satırlı, bitirmek için boş satır + Enter):")
        content_lines = []
        while True:
            line = input()
            if line == "":
                break
            content_lines.append(line)
        content = "\n".join(content_lines)
        
        image_url = input("Resim URL (opsiyonel, Enter ile geç): ").strip()
        image_url = image_url if image_url else None
        
        # Haberi ekle
        news_id = database.add_news(
            title=title,
            summary=summary,
            content=content,
            category_id=category_id,
            image_url=image_url
        )
        
        print(f"\n✅ Haber başarıyla eklendi! ID: {news_id}")
        
    except ValueError:
        print("❌ Geçersiz kategori ID!")
    except Exception as e:
        print(f"❌ Hata: {e}")

def add_tip_interactive():
    """İnteraktif olarak tip ekle"""
    print("\n=== YENİ TİP EKLE ===")
    
    try:
        title = input("Başlık: ")
        print("İçerik (Çok satırlı, bitirmek için boş satır + Enter):")
        content_lines = []
        while True:
            line = input()
            if line == "":
                break
            content_lines.append(line)
        content = "\n".join(content_lines)
        
        difficulty = input("Zorluk (Kolay/Orta/Zor, opsiyonel, Enter ile geç): ").strip()
        difficulty = difficulty if difficulty else None
        
        # Tipi ekle
        tip_id = database.add_tip(
            title=title,
            content=content,
            difficulty=difficulty
        )
        
        print(f"\n✅ Tip başarıyla eklendi! ID: {tip_id}")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def add_category_interactive():
    """İnteraktif olarak kategori ekle"""
    print("\n=== YENİ KATEGORİ EKLE ===")
    
    try:
        name = input("Kategori Adı: ")
        description = input("Açıklama (opsiyonel, Enter ile geç): ").strip()
        description = description if description else None
        
        # Kategoriyi ekle
        category_id = database.add_category(
            name=name,
            description=description
        )
        
        print(f"\n✅ Kategori başarıyla eklendi! ID: {category_id}")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def list_all_data():
    """Tüm verileri listele"""
    print("\n=== VERİTABANI İÇERİĞİ ===\n")
    
    # Kategoriler
    categories = database.get_all_categories()
    print(f"📁 Kategoriler ({len(categories)}):")
    for cat in categories:
        print(f"  [{cat['id']}] {cat['name']} - {cat.get('description', '')}")
    
    # Haberler
    news = database.get_all_news()
    print(f"\n📰 Haberler ({len(news)}):")
    for n in news:
        print(f"  [{n['id']}] {n['title']} (Kategori: {n.get('category_name', 'N/A')})")
    
    # Tips
    tips = database.get_all_tips()
    print(f"\n💡 Tips ({len(tips)}):")
    for t in tips:
        print(f"  [{t['id']}] {t['title']} (Zorluk: {t.get('difficulty', 'N/A')})")

def main():
    """Ana menü"""
    while True:
        print("\n" + "="*50)
        print("VERİTABANI VERİ YÖNETİMİ")
        print("="*50)
        print("1. Haber Ekle")
        print("2. Tip Ekle")
        print("3. Kategori Ekle")
        print("4. Tüm Verileri Listele")
        print("5. Çıkış")
        
        choice = input("\nSeçiminiz (1-5): ").strip()
        
        if choice == "1":
            add_news_interactive()
        elif choice == "2":
            add_tip_interactive()
        elif choice == "3":
            add_category_interactive()
        elif choice == "4":
            list_all_data()
        elif choice == "5":
            print("\n👋 Çıkılıyor...")
            break
        else:
            print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    main()

