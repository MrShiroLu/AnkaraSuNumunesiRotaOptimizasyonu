"""
Ankara Göletleri ve Başlangıç Noktası Verileri
"""

import googlemaps

# Başlangıç noktası (Çevre Bakanlığı)
baslangic_noktasi = "Çevre, Şehircilik ve İklim Değişikliği Bakanlığı, Ankara"

# Ankara'daki 10 gölet
goletler = [
    "Eymir Gölü, Ankara",
    "Mogan Gölü, Gölbaşı, Ankara",
    "Çubuk Barajı, Çubuk, Ankara",
    "Kurtboğazı Barajı, Kızılcahamam, Ankara",
    "Bayındır Barajı, Ankara",
    "Kesikköprü Barajı, Ankara",
    "İmrahor Vadisi Göleti, Ankara",
    "Altınpark Gölü, Altındağ, Ankara",
    "Harikalar Diyarı Göleti, Keçiören, Ankara",
    "Göksu Parkı Göleti, Eryaman, Ankara"
]


def get_all_locations():
    """Tüm lokasyonları döndür (başlangıç + göletler)"""
    return [baslangic_noktasi] + goletler


def get_location_info(index):
    """
    Index'e göre lokasyon bilgisini döndür
    
    Args:
        index: Lokasyon indeksi (0 = başlangıç, 1-10 = göletler)
    
    Returns:
        str: Lokasyon ismi
    """
    if index == 0:
        return baslangic_noktasi
    else:
        return goletler[index - 1]

