# Veritabanı Kullanım Kılavuzu

Bu kılavuz, ERD'ye göre oluşturulan SQLite veritabanını nasıl kullanacağınızı açıklar.

## 📋 Veritabanı Yapısı

Veritabanı şu tablolardan oluşur:

- **users** - Kullanıcı bilgileri
- **tips** - Tarım ipuçları
- **news_categories** - Haber kategorileri
- **news** - Haberler
- **search_history** - Arama geçmişi
- **chat_log** - Chat logları
- **favorite_news** - Favori haberler

## 🚀 Veritabanını Başlatma

Veritabanı zaten oluşturulmuş durumda. Eğer sıfırdan oluşturmak isterseniz:

```bash
python backend/init_db.py
```

Bu script:
- Tüm tabloları oluşturur
- İlişkileri (foreign keys) kurar
- İndeksleri oluşturur
- Örnek kategoriler ve tips ekler

## 📝 Manuel Veri Ekleme

### Yöntem 1: İnteraktif Script (Önerilen)

En kolay yöntem, interaktif script kullanmaktır:

```bash
python backend/add_data.py
```

Bu script size şu seçenekleri sunar:
1. **Haber Ekle** - Yeni haber ekleyebilirsiniz
2. **Tip Ekle** - Yeni tarım ipucu ekleyebilirsiniz
3. **Kategori Ekle** - Yeni haber kategorisi ekleyebilirsiniz
4. **Tüm Verileri Listele** - Mevcut verileri görüntüleyebilirsiniz

### Yöntem 2: Python Kodu ile

Doğrudan Python kodunda `database` modülünü kullanabilirsiniz:

```python
from backend import database

# Kategori ekle
category_id = database.add_category(
    name="Tarım Haberleri",
    description="Genel tarım haberleri"
)

# Haber ekle
news_id = database.add_news(
    title="Yeni Tarım Teknolojileri",
    summary="Tarım sektöründe yeni teknolojiler",
    content="Detaylı haber içeriği buraya gelir...",
    category_id=category_id,
    image_url="https://example.com/image.jpg"  # Opsiyonel
)

# Tip ekle
tip_id = database.add_tip(
    title="Domates Yetiştirme",
    content="Domates bitkileri için düzenli sulama önemlidir.",
    difficulty="Kolay"  # Opsiyonel: Kolay, Orta, Zor
)
```

### Yöntem 3: API Endpoint'leri ile

Backend çalışırken API endpoint'lerini kullanabilirsiniz:

```bash
# Kategori ekle
curl -X POST "http://localhost:8000/api/categories" \
  -H "Content-Type: application/json" \
  -d '{"name": "Tarım Haberleri", "description": "Genel tarım haberleri"}'

# Haber ekle
curl -X POST "http://localhost:8000/api/news" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Yeni Tarım Teknolojileri",
    "summary": "Tarım sektöründe yeni teknolojiler",
    "content": "Detaylı haber içeriği...",
    "category_id": 1,
    "image_url": "https://example.com/image.jpg"
  }'

# Tip ekle
curl -X POST "http://localhost:8000/api/tips" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Domates Yetiştirme",
    "content": "Domates bitkileri için düzenli sulama önemlidir.",
    "difficulty": "Kolay"
  }'
```

## 📊 Veri Sorgulama

### Python ile

```python
from backend import database

# Tüm haberleri getir
news = database.get_all_news(limit=10)

# Kategoriye göre haberleri getir
news = database.get_all_news(category_id=1)

# Tüm tips'leri getir
tips = database.get_all_tips(difficulty="Kolay")

# Kategorileri getir
categories = database.get_all_categories()
```

### API ile

```bash
# Tüm haberler
curl "http://localhost:8000/api/news"

# Belirli kategorideki haberler
curl "http://localhost:8000/api/news?category_id=1"

# Tüm tips'ler
curl "http://localhost:8000/api/tips"

# Kolay tips'ler
curl "http://localhost:8000/api/tips?difficulty=Kolay"

# Kategoriler
curl "http://localhost:8000/api/categories"
```

## 🔧 Veri Güncelleme ve Silme

### Python ile

```python
# Haber güncelle
database.update_news(
    news_id=1,
    title="Güncellenmiş Başlık",
    summary="Güncellenmiş özet"
)

# Haber sil
database.delete_news(news_id=1)

# Tip güncelle
database.update_tip(
    tip_id=1,
    title="Güncellenmiş Tip Başlığı"
)

# Tip sil
database.delete_tip(tip_id=1)
```

### API ile

```bash
# Haber güncelle
curl -X PUT "http://localhost:8000/api/news/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Güncellenmiş Başlık"}'

# Haber sil
curl -X DELETE "http://localhost:8000/api/news/1"
```

## 📍 Veritabanı Dosyası

Veritabanı dosyası proje kök dizininde `database.db` olarak saklanır.

## 🔍 Veritabanını İnceleme

SQLite veritabanını doğrudan incelemek için:

```bash
# SQLite CLI ile
sqlite3 database.db

# SQLite komutları
.tables          # Tüm tabloları listele
.schema news     # news tablosunun yapısını göster
SELECT * FROM news;  # Tüm haberleri göster
SELECT * FROM tips;  # Tüm tips'leri göster
```

## 📚 API Dokümantasyonu

Backend çalışırken API dokümantasyonuna şu adresten erişebilirsiniz:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ⚠️ Notlar

1. **Foreign Key İlişkileri**: Haber eklerken mevcut bir `category_id` kullanmalısınız
2. **Unique Constraints**: `favorite_news` tablosunda aynı kullanıcı aynı haberi birden fazla kez favorileyemez
3. **Timestamps**: `created_at` alanları otomatik olarak eklenir
4. **Veri Yedekleme**: Düzenli olarak `database.db` dosyasını yedekleyin

## 🎯 Örnek Kullanım Senaryosu

1. **Kategori Oluştur**:
   ```python
   cat_id = database.add_category("Teknoloji", "Tarım teknolojileri")
   ```

2. **Haber Ekle**:
   ```python
   news_id = database.add_news(
       title="Yapay Zeka ile Tarım",
       summary="AI teknolojisi tarımda devrim yaratıyor",
       content="Detaylı içerik...",
       category_id=cat_id
   )
   ```

3. **Tip Ekle**:
   ```python
   tip_id = database.add_tip(
       title="Akıllı Sulama",
       content="Sensörlerle otomatik sulama sistemi kurun",
       difficulty="Orta"
   )
   ```

4. **Verileri Görüntüle**:
   ```python
   news = database.get_all_news()
   tips = database.get_all_tips()
   ```

