"""
ACO Algoritması Parametreleri ve Yapılandırma Dosyası
"""

class ACOConfig:
    """Karınca Kolonisi Algoritması Parametreleri"""
    
    # Karınca sayısı (her iterasyonda kaç karınca rota oluşturacak)
    N_ANTS = 30
    
    # İterasyon sayısı (algoritma kaç kez tekrar edecek)
    N_ITERATIONS = 100
    
    # Alpha: Feromon önem katsayısı
    # Yüksek değer -> Feromon daha önemli (karıncalar birbirini takip eder)
    # Düşük değer -> Mesafe daha önemli
    ALPHA = 1.0
    
    # Beta: Mesafe önem katsayısı (heuristic)
    # Yüksek değer -> Yakın yerleri tercih eder (greedy)
    # Düşük değer -> Daha fazla keşif yapar
    BETA = 3.0
    
    # Buharlaşma oranı (0-1 arası)
    # Yüksek değer -> Feromon hızlı buharlaşır (daha fazla keşif)
    # Düşük değer -> Feromon uzun süre kalır (daha fazla sömürme)
    EVAPORATION_RATE = 0.3
    
    # Feromon yoğunluğu sabiti
    # Karıncaların bırakacağı feromon miktarını belirler
    Q = 100
    
    # Harita merkezi (Ankara koordinatları)
    MAP_CENTER = [39.9334, 32.8597]
    MAP_ZOOM = 10


class VisualizationConfig:
    """Görselleştirme Ayarları"""
    
    # Grafik boyutları
    FIGURE_SIZE = (14, 6)
    
    # Renkler
    COLOR_CONVERGENCE = '#2E86AB'
    COLOR_IMPROVEMENT = '#A23B72'
    COLOR_ROUTE = '#E63946'
    
    # Marker renkleri
    COLOR_START = 'green'
    COLOR_END = 'red'
    COLOR_LAKE = 'blue'
    
    # Grafik DPI
    DPI = 300

