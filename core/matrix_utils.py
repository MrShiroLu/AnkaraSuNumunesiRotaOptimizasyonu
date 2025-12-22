"""
Mesafe Matrisi Oluşturma ve Koordinat İşlemleri
Google Maps API ve Haversine formülü kullanımı
"""

import numpy as np
import googlemaps
from .haversine import haversine_distance


def get_coordinates(gmaps_client, address):
    """
    Google Maps Geocoding API ile adresin koordinatlarını al
    
    Args:
        gmaps_client: Google Maps client
        address: Aranacak adres (str)
    
    Returns:
        tuple: (lat, lng) veya None
    """
    try:
        result = gmaps_client.geocode(address)
        if result:
            location = result[0]['geometry']['location']
            return (location['lat'], location['lng'])
        return None
    except Exception as e:
        print(f"Koordinat alma hatası ({address}): {e}")
        return None


def get_coordinates_batch(gmaps_client, addresses):
    """
    Birden fazla adres için toplu koordinat alma
    
    Args:
        gmaps_client: Google Maps client
        addresses: Adres listesi
    
    Returns:
        list: [(lat, lng), ...] koordinat listesi
    """
    coordinates = []
    
    for i, address in enumerate(addresses, 1):
        print(f"Koordinat alınıyor {i}/{len(addresses)}: {address}")
        coord = get_coordinates(gmaps_client, address)
        
        if coord:
            coordinates.append(coord)
        else:
            raise ValueError(f"Koordinat alınamadı: {address}")
    
    return coordinates


def create_distance_matrix(coordinates, gmaps_client=None, use_api=True):
    """
    Koordinatlar arası mesafe matrisi oluştur
    
    Args:
        coordinates: [(lat, lng), ...] koordinat listesi
        gmaps_client: Google Maps client (opsiyonel)
        use_api: True ise Google Maps API kullan, False ise Haversine
    
    Returns:
        tuple: (distance_matrix, time_matrix)
            - distance_matrix: NxN numpy array (km)
            - time_matrix: NxN numpy array (dakika)
    """
    n = len(coordinates)
    distance_matrix = np.zeros((n, n))
    time_matrix = np.zeros((n, n))
    
    if use_api and gmaps_client:
        # Google Maps Distance Matrix API kullan
        print("Google Maps Distance Matrix API ile mesafeler hesaplanıyor...")
        
        for i in range(n):
            print(f"Nokta {i+1}/{n} için mesafeler hesaplanıyor...")
            
            try:
                result = gmaps_client.distance_matrix(
                    origins=[coordinates[i]],
                    destinations=coordinates,
                    mode="driving",
                    language="tr",
                    units="metric"
                )
                
                if result['status'] == 'OK':
                    for j, element in enumerate(result['rows'][0]['elements']):
                        if element['status'] == 'OK':
                            # Gerçek yol mesafesi ve süresi
                            distance_matrix[i][j] = element['distance']['value'] / 1000  # km
                            time_matrix[i][j] = element['duration']['value'] / 60  # dakika
                        else:
                            # API hatası durumunda Haversine kullan
                            distance_matrix[i][j] = haversine_distance(
                                coordinates[i], coordinates[j]
                            )
                            time_matrix[i][j] = distance_matrix[i][j] * 1.5  # Tahmini süre
                else:
                    raise Exception(f"API hatası: {result['status']}")
                    
            except Exception as e:
                print(f"Hata (nokta {i}): {e}")
                # Tüm satır için Haversine kullan
                for j in range(n):
                    distance_matrix[i][j] = haversine_distance(
                        coordinates[i], coordinates[j]
                    )
                    time_matrix[i][j] = distance_matrix[i][j] * 1.5
    else:
        # Haversine formülü kullan (kuş uçuşu)
        print("Haversine formülü ile mesafeler hesaplanıyor...")
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    distance_matrix[i][j] = haversine_distance(
                        coordinates[i], coordinates[j]
                    )
                    time_matrix[i][j] = distance_matrix[i][j] * 1.5  # Tahmini süre
    
    print("Mesafe matrisi oluşturuldu!")
    return distance_matrix, time_matrix


def get_route_details(route_indices, distance_matrix, time_matrix, locations):
    """
    Rota detaylarını hesapla
    
    Args:
        route_indices: Rota indeksleri listesi
        distance_matrix: Mesafe matrisi
        time_matrix: Süre matrisi
        locations: Lokasyon isimleri
    
    Returns:
        dict: Rota detayları
    """
    total_distance = 0.0
    total_time = 0.0
    route_details = []
    
    for i in range(len(route_indices) - 1):
        idx_from = route_indices[i]
        idx_to = route_indices[i + 1]
        
        distance = distance_matrix[idx_from][idx_to]
        time = time_matrix[idx_from][idx_to]
        
        total_distance += distance
        total_time += time
        
        route_details.append({
            'from': locations[idx_from],
            'to': locations[idx_to],
            'distance': distance,
            'time': time
        })
    
    return {
        'total_distance': total_distance,
        'total_time': total_time,
        'details': route_details
    }

