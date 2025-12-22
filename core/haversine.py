"""
Haversine Formülü ile Mesafe Hesaplama
İki koordinat arası kuş uçuşu mesafe hesabı
"""

from math import radians, sin, cos, sqrt, atan2


def haversine_distance(coord1, coord2):
    """
    İki koordinat arası kuş uçuşu mesafe hesaplama (Haversine formülü)
    
    Args:
        coord1: (lat, lng) tuple - İlk koordinat
        coord2: (lat, lng) tuple - İkinci koordinat
    
    Returns:
        float: Mesafe (kilometre)
    
    Örnek:
        >>> coord1 = (39.9334, 32.8597)  # Ankara
        >>> coord2 = (41.0082, 28.9784)  # İstanbul
        >>> distance = haversine_distance(coord1, coord2)
        >>> print(f"{distance:.2f} km")
        279.18 km
    """
    # Dünya yarıçapı (kilometre)
    R = 6371.0
    
    # Koordinatları ayrıştır
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Radyan'a çevir
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    # Farkları hesapla
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formülü
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Mesafe
    distance = R * c
    
    return distance


def calculate_total_route_distance(route_coords):
    """
    Rota boyunca toplam mesafe hesapla
    
    Args:
        route_coords: Liste of (lat, lng) tuples
    
    Returns:
        float: Toplam mesafe (km)
    """
    total_distance = 0.0
    
    for i in range(len(route_coords) - 1):
        distance = haversine_distance(route_coords[i], route_coords[i + 1])
        total_distance += distance
    
    return total_distance

