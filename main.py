"""
Karınca Kolonisi Algoritması ile Ankara Gölet Rota Optimizasyonu
Streamlit Ana Uygulama Dosyası
"""

import streamlit as st
import os
from dotenv import load_dotenv
import googlemaps
import folium
from streamlit_folium import st_folium

from config import ACOConfig
from data.coordinates import goletler, baslangic_noktasi, get_all_locations
from core.haversine import haversine_distance
from core.matrix_utils import create_distance_matrix, get_coordinates_batch
from core.ant_algorithm import AntColonyOptimizer
from visual.plotting import plot_convergence, create_interactive_map

# Sayfa yapılandırması
st.set_page_config(
    page_title="ACO Rota Optimizasyonu",
    page_icon="🗺️",
    layout="wide"
)

# API Key yükleme
load_dotenv()
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Ana başlık
st.title("Karınca Kolonisi Algoritması ile Rota Optimizasyonu")
st.markdown("**Ankara Göletleri Su Numunesi Toplama - En Kısa Rota**")
st.markdown("---")

# Sidebar - Ayarlar
with st.sidebar:
    st.header("Ayarlar")
    
    # API Key input
    api_key_input = st.text_input(
        "Google Maps API Anahtarı", 
        value=API_KEY if API_KEY else "",
        type="password",
        help="API anahtarı .env dosyasından veya buradan girilebilir"
    )
    
    st.subheader("ACO Parametreleri")
    
    # ACO parametreleri
    n_ants = st.slider("Karınca Sayısı", 10, 100, ACOConfig.N_ANTS, 5)
    n_iterations = st.slider("İterasyon Sayısı", 50, 500, ACOConfig.N_ITERATIONS, 10)
    
    with st.expander("Gelişmiş Parametreler"):
        alpha = st.slider("Alpha (α) - Feromon", 0.1, 5.0, ACOConfig.ALPHA, 0.1)
        beta = st.slider("Beta (β) - Mesafe", 0.1, 10.0, ACOConfig.BETA, 0.1)
        evaporation = st.slider("Buharlaşma (ρ)", 0.1, 0.9, ACOConfig.EVAPORATION_RATE, 0.05)
        Q = st.number_input("Q Sabiti", 10, 500, ACOConfig.Q, 10)
    
    st.markdown("---")
    run_btn = st.button("Optimizasyonu Başlat", type="primary", use_container_width=True)

# Ana içerik - Sekmeler
tab1, tab2, tab3, tab4 = st.tabs(["Göletler", "Optimizasyon", "Harita", "Sonuçlar"])

# Sekme 1: Göletler
with tab1:
    st.subheader("Ankara'daki Göletler")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info(f"""
        **Başlangıç Noktası:**  
        {baslangic_noktasi}
        
        **Toplam Gölet Sayısı:**  
        {len(goletler)} adet
        """)
    
    with col2:
        st.markdown("**Gölet Listesi:**")
        for i, golet in enumerate(goletler, 1):
            st.write(f"{i}. {golet}")

# Sekme 2: Optimizasyon
with tab2:
    st.subheader("Algoritma Bilgileri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Karınca Kolonisi Algoritması (ACO)
        
        **Doğadan İlham:**
        - Karıncalar feromon bırakarak yol bulur
        - Kısa yollar daha fazla feromon içerir
        - Diğer karıncalar yüksek feromonlu yolları tercih eder
        
        **Algoritma Adımları:**
        1. Karıncalar rastgele rota oluşturur
        2. Kısa rotalar daha fazla feromon bırakır
        3. Feromon zamanla buharlaşır
        4. En iyi rota zamanla ortaya çıkar
        """)
    
    with col2:
        st.markdown("""
        ### Seçilen Parametreler
        
        | Parametre | Değer | Açıklama |
        |-----------|-------|----------|
        | Karınca | {} | Her iterasyonda rota sayısı |
        | İterasyon | {} | Algoritma tekrar sayısı |
        | Alpha (α) | {} | Feromon etkisi |
        | Beta (β) | {} | Mesafe etkisi |
        | Buharlaşma | {} | Feromon azalma oranı |
        | Q | {} | Feromon miktarı |
        """.format(n_ants, n_iterations, alpha, beta, evaporation, Q))

# Optimizasyon çalıştırma
if run_btn:
    if not api_key_input:
        st.error("Lütfen Google Maps API anahtarını girin!")
    else:
        with st.spinner("Optimizasyon yapılıyor..."):
            try:
                # Google Maps client
                gmaps = googlemaps.Client(key=api_key_input)
                
                # Koordinatları al
                with st.status("Koordinatlar alınıyor...", expanded=True) as status:
                    st.write("Gölet koordinatları Google Maps API'den alınıyor...")
                    coordinates = get_coordinates_batch(gmaps, get_all_locations())
                    status.update(label="Koordinatlar alındı!", state="complete")
                
                # Mesafe matrisi
                with st.status("Mesafeler hesaplanıyor...", expanded=True) as status:
                    st.write("Noktalar arası mesafeler hesaplanıyor...")
                    distance_matrix, time_matrix = create_distance_matrix(coordinates, gmaps)
                    status.update(label="Mesafe matrisi oluşturuldu!", state="complete")
                
                # ACO optimizasyonu
                with st.status("ACO algoritması çalışıyor...", expanded=True) as status:
                    progress_bar = st.progress(0)
                    progress_text = st.empty()
                    
                    def progress_callback(iteration, total, best_dist):
                        progress_bar.progress(iteration / total)
                        progress_text.text(f"İterasyon {iteration}/{total} - En İyi: {best_dist:.2f} km")
                    
                    aco = AntColonyOptimizer(
                        distance_matrix=distance_matrix,
                        n_ants=n_ants,
                        n_iterations=n_iterations,
                        alpha=alpha,
                        beta=beta,
                        evaporation_rate=evaporation,
                        Q=Q
                    )
                    
                    optimal_route, total_distance = aco.optimize(
                        start_city=0, 
                        progress_callback=progress_callback
                    )
                    
                    progress_bar.empty()
                    progress_text.empty()
                    status.update(label="Optimizasyon tamamlandı!", state="complete")
                
                # Sonuçları session state'e kaydet
                st.session_state.optimized = True
                st.session_state.optimal_route = optimal_route
                st.session_state.total_distance = total_distance
                st.session_state.coordinates = coordinates
                st.session_state.distance_matrix = distance_matrix
                st.session_state.time_matrix = time_matrix
                st.session_state.aco = aco
                
                st.success(f"Optimizasyon tamamlandı! Toplam mesafe: {total_distance:.2f} km")
                
            except Exception as e:
                st.error(f"Hata: {str(e)}")
                st.exception(e)

# Sekme 3: Harita
with tab3:
    st.subheader("İnteraktif Rota Haritası")
    
    if st.session_state.get('optimized'):
        # Harita oluştur
        route_map = create_interactive_map(
            optimal_route=st.session_state.optimal_route,
            coordinates=st.session_state.coordinates,
            distance_matrix=st.session_state.distance_matrix,
            time_matrix=st.session_state.time_matrix,
            goletler=goletler,
            baslangic=baslangic_noktasi
        )
        
        # Haritayı göster
        st_folium(route_map, width=1200, height=600)
        
        # Metrikler
        col1, col2, col3, col4 = st.columns(4)
        
        # Toplam süre hesapla
        total_time = 0
        for i in range(len(st.session_state.optimal_route) - 1):
            idx_from = st.session_state.optimal_route[i]
            idx_to = st.session_state.optimal_route[i + 1]
            total_time += st.session_state.time_matrix[idx_from][idx_to]
        
        col1.metric("Toplam Mesafe", f"{st.session_state.total_distance:.2f} km")
        col2.metric("Tahmini Süre", f"{total_time:.0f} dk")
        col3.metric("Gölet Sayısı", len(goletler))
        col4.metric("Ort. Mesafe", f"{st.session_state.total_distance/len(goletler):.2f} km")
    else:
        st.info("Haritayı görmek için önce optimizasyonu çalıştırın.")

# Sekme 4: Sonuçlar
with tab4:
    st.subheader("Sonuçlar ve Analizler")
    
    if st.session_state.get('optimized'):
        # Yakınsama grafiği
        st.markdown("### Algoritma Yakınsama Grafiği")
        fig = plot_convergence(st.session_state.aco)
        st.pyplot(fig)
        
        # İstatistikler
        col1, col2, col3 = st.columns(3)
        
        history = st.session_state.aco.best_distance_history
        improvement = (history[0] - history[-1]) / history[0] * 100
        
        col1.metric("İlk İterasyon", f"{history[0]:.2f} km")
        col2.metric("Son İterasyon", f"{history[-1]:.2f} km")
        col3.metric("İyileşme", f"{improvement:.1f}%")
        
        # Rota tablosu
        st.markdown("### Rota Detayları")
        
        import pandas as pd
        
        rota_data = []
        for i, idx in enumerate(st.session_state.optimal_route[:-1], 1):
            if idx == 0:
                lokasyon = baslangic_noktasi
            else:
                lokasyon = goletler[idx - 1]
            
            next_idx = st.session_state.optimal_route[i]
            mesafe = st.session_state.distance_matrix[idx][next_idx]
            sure = st.session_state.time_matrix[idx][next_idx]
            
            rota_data.append({
                'Sıra': i,
                'Lokasyon': lokasyon,
                'Mesafe (km)': round(mesafe, 2),
                'Süre (dk)': round(sure, 0)
            })
        
        df_rota = pd.DataFrame(rota_data)
        st.dataframe(df_rota, use_container_width=True, hide_index=True)
        
        # CSV indirme
        csv = df_rota.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Rota Detaylarını İndir (CSV)",
            data=csv,
            file_name="ankara_golet_rota.csv",
            mime="text/csv"
        )
    else:
        st.info("Sonuçları görmek için önce optimizasyonu çalıştırın.")

# Footer
st.markdown("---")
st.markdown(
    "<center>Karınca Kolonisi Algoritması ile Rota Optimizasyonu | "
    "Google Maps API + Streamlit</center>",
    unsafe_allow_html=True
)

