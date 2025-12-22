"""
Yol ve Yakınsama Grafiklerinin Görselleştirilmesi
"""

import matplotlib.pyplot as plt
import folium
from config import VisualizationConfig


def plot_convergence(aco_optimizer):
    """
    ACO algoritması yakınsama grafiği çiz
    
    Args:
        aco_optimizer: AntColonyOptimizer nesnesi
    
    Returns:
        matplotlib.figure.Figure: Grafik objesi
    """
    history = aco_optimizer.best_distance_history
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=VisualizationConfig.FIGURE_SIZE)
    
    # Sol grafik: En iyi mesafe değişimi
    ax1.plot(history, linewidth=2, color=VisualizationConfig.COLOR_CONVERGENCE)
    ax1.set_xlabel('İterasyon', fontsize=12, fontweight='bold')
    ax1.set_ylabel('En İyi Mesafe (km)', fontsize=12, fontweight='bold')
    ax1.set_title('ACO Yakınsama Grafiği', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=history[-1], color='red', linestyle='--', 
                label=f'Optimal: {history[-1]:.2f} km')
    ax1.legend()
    
    # Sağ grafik: İyileşme yüzdesi
    improvement = [(history[0] - d) / history[0] * 100 for d in history]
    ax2.plot(improvement, linewidth=2, color=VisualizationConfig.COLOR_IMPROVEMENT)
    ax2.set_xlabel('İterasyon', fontsize=12, fontweight='bold')
    ax2.set_ylabel('İyileşme (%)', fontsize=12, fontweight='bold')
    ax2.set_title('İyileşme Oranı', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=improvement[-1], color='green', linestyle='--',
                label=f'Toplam: {improvement[-1]:.1f}%')
    ax2.legend()
    
    plt.tight_layout()
    
    return fig


def create_interactive_map(optimal_route, coordinates, distance_matrix, time_matrix,
                           goletler, baslangic):
    """
    İnteraktif Folium haritası oluştur
    
    Args:
        optimal_route: Optimal rota indeksleri
        coordinates: Koordinat listesi
        distance_matrix: Mesafe matrisi
        time_matrix: Süre matrisi
        goletler: Gölet isimleri
        baslangic: Başlangıç noktası ismi
    
    Returns:
        folium.Map: Harita objesi
    """
    from config import ACOConfig
    
    # Harita oluştur
    m = folium.Map(
        location=ACOConfig.MAP_CENTER,
        zoom_start=ACOConfig.MAP_ZOOM,
        tiles='OpenStreetMap'
    )
    
    # Rota koordinatları
    route_coords = []
    
    for i, idx in enumerate(optimal_route):
        coord = coordinates[idx]
        route_coords.append([coord[0], coord[1]])
        
        # Marker ekleme
        if idx == 0:
            # Başlangıç/Bitiş noktası
            if i == 0:
                color = VisualizationConfig.COLOR_START
                icon = 'play'
                label = 'BAŞLANGIÇ'
                popup_text = f"<b>{label}</b><br>{baslangic}"
            else:
                color = VisualizationConfig.COLOR_END
                icon = 'stop'
                label = 'BİTİŞ'
                popup_text = f"<b>{label}</b><br>{baslangic}"
            
            folium.Marker(
                location=[coord[0], coord[1]],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=label,
                icon=folium.Icon(color=color, icon=icon, prefix='fa')
            ).add_to(m)
        else:
            # Gölet
            golet_name = goletler[idx - 1]
            
            # Önceki noktadan mesafe bilgisi
            if i > 0:
                prev_idx = optimal_route[i-1]
                distance = distance_matrix[prev_idx][idx]
                time = time_matrix[prev_idx][idx]
                distance_info = f"<br><b>Mesafe:</b> {distance:.2f} km<br><b>Süre:</b> {time:.0f} dk"
            else:
                distance_info = ""
            
            popup_text = f"<b>Durak {i}</b><br>{golet_name}{distance_info}"
            
            folium.Marker(
                location=[coord[0], coord[1]],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f"Durak {i}: {golet_name}",
                icon=folium.Icon(color=VisualizationConfig.COLOR_LAKE, 
                               icon='tint', prefix='fa')
            ).add_to(m)
            
            # Durak numarası
            folium.Marker(
                location=[coord[0], coord[1]],
                icon=folium.DivIcon(html=f'''
                    <div style="
                        font-size: 12pt;
                        color: white;
                        background-color: #2E86AB;
                        border: 2px solid white;
                        border-radius: 50%;
                        width: 25px;
                        height: 25px;
                        text-align: center;
                        line-height: 25px;
                        font-weight: bold;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
                    ">{i}</div>
                ''')
            ).add_to(m)
    
    # Rota çizgisi
    folium.PolyLine(
        route_coords,
        color=VisualizationConfig.COLOR_ROUTE,
        weight=4,
        opacity=0.8,
        popup='Optimal Rota'
    ).add_to(m)
    
    return m


def save_figure(fig, filename, dpi=None):
    """
    Matplotlib figürünü dosyaya kaydet
    
    Args:
        fig: Matplotlib figure objesi
        filename: Dosya adı
        dpi: DPI değeri (opsiyonel)
    """
    if dpi is None:
        dpi = VisualizationConfig.DPI
    
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    print(f"Grafik kaydedildi: {filename}")

