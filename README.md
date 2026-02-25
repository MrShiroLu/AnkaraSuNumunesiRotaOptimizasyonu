# Karınca Kolonisi Algoritması ile Ankara Gölet Rota Optimizasyonu

Çevre Bakanlığı birimlerinin Ankara'daki 10 farklı göletten su numunesi toplaması için **Ant Colony Optimization (ACO)** algoritması ile en kısa rotayı bulan Streamlit web uygulaması.

## Proje Açıklaması

Bu proje, doğadaki karıncaların feromon bırakarak en kısa yolu bulma davranışından esinlenen **Karınca Kolonisi Algoritması** kullanarak:

- Ankara'daki 10 farklı göletin gerçek koordinatlarını Google Maps API ile alır
- Noktalar arası gerçek yol mesafelerini Distance Matrix API ile hesaplar
- ACO algoritması ile optimal rotayı bulur
- İnteraktif harita ve görselleştirmelerle sonuçları gösterir

## Özellikler

- **Google Maps Entegrasyonu**: Gerçek koordinatlar ve yol mesafeleri
- **ACO Algoritması**: 30 karınca, 100 iterasyon ile optimizasyon
- **İnteraktif Arayüz**: Streamlit ile kullanıcı dostu web uygulaması
- **Görselleştirme**: Folium haritaları ve yakınsama grafikleri
- **Modüler Yapı**: Temiz kod mimarisi ve yeniden kullanılabilir modüller

## Proje Yapısı

```
aco_ilac_rotasi/
│
├── main.py                    # Streamlit ana uygulama dosyası
├── config.py                  # ACO parametreleri ve ayarlar
├── requirements.txt           # Gerekli Python kütüphaneleri
├── .env.example              # API key şablon dosyası
├── .gitignore                # Git ignore kuralları
│
├── data/
│   └── coordinates.py        # Gölet verileri ve koordinatlar
│
├── core/
│   ├── haversine.py          # Kuş uçuşu mesafe hesaplama
│   ├── matrix_utils.py       # Mesafe matrisi oluşturma
│   └── ant_algorithm.py      # ACO algoritması
│
├── visual/
│   └── plotting.py           # Görselleştirme fonksiyonları
│
├── .streamlit/
│   └── secrets.toml          # Streamlit API key (opsiyonel)
│
├── figure/                   # Çıktı görselleri (otomatik oluşur)
│   ├── rota.png
│   └── convergence.png
│
└── README.md                 # Bu dosya
```

## Kurulum

### 1. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Google Maps API Anahtarı Alın

1. [Google Cloud Console](https://console.cloud.google.com/) adresine gidin
2. Yeni bir proje oluşturun
3. Aşağıdaki API'leri etkinleştirin:
   - **Geocoding API**
   - **Distance Matrix API**
4. Credentials > Create Credentials > API Key ile anahtar oluşturun

### 3. API Anahtarını Yapılandırın

**Seçenek 1: .env dosyası**

`.env.example` dosyasını `.env` olarak kopyalayın ve API anahtarınızı girin:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:
```
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Seçenek 2: Streamlit secrets**

`.streamlit/secrets.toml` dosyasını düzenleyin:
```toml
GOOGLE_MAPS_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

**Seçenek 3: Uygulama içinde**

Uygulamayı çalıştırdıktan sonra sol menüden API anahtarını girebilirsiniz.

## Kullanım

### Uygulamayı Başlatın

```bash
streamlit run main.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` adresinde açılacaktır.

### Uygulama Kullanımı

1. **Sol Menü**: ACO parametrelerini ayarlayın
   - Karınca Sayısı (10-100)
   - İterasyon Sayısı (50-500)
   - Alpha, Beta, Buharlaşma oranı (gelişmiş ayarlar)

2. **Göletler Sekmesi**: Ankara'daki 10 göletin listesini görün

3. **Optimizasyon Sekmesi**: ACO algoritması hakkında bilgi

4. **"Optimizasyonu Başlat" Butonu**: Algoritmayı çalıştırın
   - Koordinatlar Google Maps'ten alınır
   - Mesafe matrisi oluşturulur
   - ACO algoritması optimal rotayı bulur

5. **Harita Sekmesi**: İnteraktif harita üzerinde optimal rotayı görün

6. **Sonuçlar Sekmesi**: Yakınsama grafikleri ve rota detayları
   - CSV olarak indirilebilir

## ACO Algoritması

### Nasıl Çalışır?

1. **Başlangıç**: Karıncalar rastgele rotalar oluşturur
2. **Feromon Bırakma**: Her karınca geçtiği yola feromon bırakır
3. **Seçim**: Karıncalar yüksek feromonlu yolları tercih eder
4. **Buharlaşma**: Feromon zamanla azalır (yerel optimumdan kaçınma)
5. **Yakınsama**: En iyi rota zamanla ortaya çıkar

### Parametreler

| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| **Karınca Sayısı** | 30 | Her iterasyonda kaç karınca rota oluşturur |
| **İterasyon** | 100 | Algoritma kaç kez tekrarlar |
| **Alpha (α)** | 1.0 | Feromon önem katsayısı |
| **Beta (β)** | 3.0 | Mesafe önem katsayısı (yüksek = yakın yerleri tercih) |
| **Buharlaşma (ρ)** | 0.3 | Feromon azalma oranı (0-1) |
| **Q** | 100 | Bırakılacak feromon miktarı |

## Google Maps API

### Kullanılan API'ler

1. **Geocoding API**
   - Adres → Koordinat dönüşümü
   - Örnek: "Eymir Gölü, Ankara" → (39.9515, 32.8861)

2. **Distance Matrix API**
   - Noktalar arası gerçek yol mesafeleri
   - Araç ile gidilecek süre ve mesafe

### Maliyet (Ücretsiz Kota)

- **Geocoding API**: Ayda 40,000 istek ücretsiz
- **Distance Matrix API**: Ayda 40,000 element ücretsiz
- **Bu proje**: ~11 geocoding + 121 distance matrix = Tamamen ücretsiz!

## Çıktılar

- **İnteraktif Harita**: Folium ile oluşturulan HTML harita
- **Yakınsama Grafiği**: Algoritma performansı
- **Rota Tablosu**: CSV formatında indirilebilir
- **Metrikler**: Toplam mesafe, süre, ortalama mesafe

## Modüller

### data/coordinates.py
Gölet isimleri ve başlangıç noktası

### core/haversine.py
Haversine formülü ile kuş uçuşu mesafe hesaplama

### core/matrix_utils.py
- Google Maps API ile koordinat alma
- Mesafe matrisi oluşturma
- Rota detayları hesaplama

### core/ant_algorithm.py
ACO algoritması implementasyonu
- `AntColonyOptimizer` sınıfı
- Feromon güncelleme
- Rota oluşturma

### visual/plotting.py
- Yakınsama grafikleri
- İnteraktif harita oluşturma
- Görsel kaydetme

## Örnek Sonuçlar

**Tipik Çalıştırma:**
- Toplam Mesafe: ~250-300 km
- Seyahat Süresi: ~4-5 saat
- Numune Toplama: ~2.5 saat (15 dk/gölet)
- Toplam Operasyon: ~7-8 saat

**Algoritma Performansı:**
- İlk İterasyon: ~350 km
- Son İterasyon: ~280 km
- İyileşme: %20-25

## Geliştirme

### Yeni Gölet Ekleme

`data/coordinates.py` dosyasında `goletler` listesine ekleyin:

```python
goletler = [
    "Eymir Gölü, Ankara",
    "Mogan Gölü, Gölbaşı, Ankara",
    # Yeni gölet ekleyin
    "Yeni Gölet, Ankara"
]
```

### Parametre Optimizasyonu

`config.py` dosyasında `ACOConfig` sınıfını düzenleyin:

```python
class ACOConfig:
    N_ANTS = 50  # Daha fazla karınca
    BETA = 5.0   # Daha greedy
```

