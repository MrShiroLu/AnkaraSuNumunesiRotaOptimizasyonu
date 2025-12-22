"""
Karınca Kolonisi Optimizasyonu (ACO) Algoritması
Ant Colony Optimization for Traveling Salesman Problem (TSP)
"""

import numpy as np


class AntColonyOptimizer:
    """
    Karınca Kolonisi Algoritması ile TSP Çözümü
    
    Karıncalar, feromon izleri bırakarak en kısa yolu keşfeder.
    Kısa yollar daha fazla kullanıldığı için daha fazla feromon birikir.
    """
    
    def __init__(self, distance_matrix, n_ants=30, n_iterations=100,
                 alpha=1.0, beta=2.0, evaporation_rate=0.5, Q=100):
        """
        Args:
            distance_matrix: NxN mesafe matrisi
            n_ants: Karınca sayısı
            n_iterations: İterasyon sayısı
            alpha: Feromon önem katsayısı (α)
            beta: Mesafe önem katsayısı (β)
            evaporation_rate: Feromon buharlaşma oranı (ρ)
            Q: Feromon yoğunluğu sabiti
        """
        self.distance_matrix = distance_matrix
        self.n_cities = len(distance_matrix)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.Q = Q
        
        # Feromon matrisi (başlangıçta tüm yollar eşit feromon içerir)
        self.pheromone = np.ones((self.n_cities, self.n_cities)) / self.n_cities
        
        # En iyi çözüm
        self.best_route = None
        self.best_distance = float('inf')
        self.best_distance_history = []
    
    def calculate_route_distance(self, route):
        """
        Verilen rota için toplam mesafeyi hesapla
        
        Args:
            route: Şehir indekslerinin listesi
        
        Returns:
            float: Toplam mesafe
        """
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distance_matrix[route[i]][route[i+1]]
        
        # Başlangıca dön
        distance += self.distance_matrix[route[-1]][route[0]]
        
        return distance
    
    def construct_solution(self, start_city=0):
        """
        Bir karınca için rota oluştur (olasılıksal seçim)
        
        Args:
            start_city: Başlangıç şehri indeksi
        
        Returns:
            list: Oluşturulan rota
        """
        route = [start_city]
        unvisited = set(range(self.n_cities)) - {start_city}
        
        while unvisited:
            current_city = route[-1]
            
            # Her ziyaret edilmemiş şehir için olasılık hesapla
            probabilities = []
            for city in unvisited:
                # Feromon seviyesi ^ alpha
                pheromone_value = self.pheromone[current_city][city] ** self.alpha
                
                # Mesafe heuristik (1/mesafe) ^ beta
                # Yakın şehirler daha yüksek değer alır
                distance_value = (1.0 / self.distance_matrix[current_city][city]) ** self.beta
                
                probabilities.append(pheromone_value * distance_value)
            
            # Olasılıkları normalize et
            probabilities = np.array(probabilities)
            probabilities = probabilities / probabilities.sum()
            
            # Olasılıklara göre bir şehir seç
            next_city = np.random.choice(list(unvisited), p=probabilities)
            
            route.append(next_city)
            unvisited.remove(next_city)
        
        return route
    
    def update_pheromones(self, all_routes, all_distances):
        """
        Feromon matrisini güncelle
        
        1. Önce tüm feromonları buharlaştır
        2. Sonra karıncaların rotalarına göre yeni feromon ekle
        
        Args:
            all_routes: Tüm karıncaların rotaları
            all_distances: Tüm rotaların mesafeleri
        """
        # Buharlaşma (evaporation)
        self.pheromone *= (1 - self.evaporation_rate)
        
        # Her karınca için feromon ekle
        for route, distance in zip(all_routes, all_distances):
            # Daha kısa rotalar daha fazla feromon bırakır
            pheromone_deposit = self.Q / distance
            
            # Rota boyunca feromon bırak
            for i in range(len(route) - 1):
                self.pheromone[route[i]][route[i+1]] += pheromone_deposit
                self.pheromone[route[i+1]][route[i]] += pheromone_deposit  # Simetrik
            
            # Başlangıca dönüş
            self.pheromone[route[-1]][route[0]] += pheromone_deposit
            self.pheromone[route[0]][route[-1]] += pheromone_deposit
    
    def optimize(self, start_city=0, progress_callback=None):
        """
        ACO algoritmasını çalıştır
        
        Args:
            start_city: Başlangıç şehri indeksi
            progress_callback: İlerleme callback fonksiyonu (opsiyonel)
                               callback(iteration, total, best_distance)
        
        Returns:
            tuple: (best_route, best_distance)
        """
        for iteration in range(self.n_iterations):
            all_routes = []
            all_distances = []
            
            # Her karınca bir rota oluşturur
            for ant in range(self.n_ants):
                route = self.construct_solution(start_city)
                distance = self.calculate_route_distance(route)
                
                all_routes.append(route)
                all_distances.append(distance)
                
                # En iyi rotayı güncelle
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_route = route[:]
            
            # Feromonları güncelle
            self.update_pheromones(all_routes, all_distances)
            
            # Geçmişi kaydet
            self.best_distance_history.append(self.best_distance)
            
            # Progress callback
            if progress_callback:
                progress_callback(iteration + 1, self.n_iterations, self.best_distance)
        
        # Başlangıca dönüşü ekle
        final_route = self.best_route + [start_city]
        
        return final_route, self.best_distance

