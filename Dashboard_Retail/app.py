import streamlit as st
import pandas as pd
import plotly.express as px

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Dashboard Plan - Week 11", layout="wide")
st.title("📊 Retail Sales & Warehouse Dashboard")
st.markdown("Dashboard ini dirancang untuk memenuhi **Week 11 - Dashboard Plan**.")

# --- Fungsi Memuat Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Retail and wherehouse Sale.csv")
    df['TOTAL SALES'] = df['RETAIL SALES'].fillna(0) + df['WAREHOUSE SALES'].fillna(0)
    df = df[df['TOTAL SALES'] > 0]
    df['DATE'] = pd.to_datetime(df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-01')
    return df

df = load_data()

# --- Membuat Tab Navigasi (Tombol Interaktif) ---
tab1, tab2, tab3 = st.tabs([
    "📂 1. Deskripsi & Preview Data", 
    "📝 2. Pertanyaan Bisnis & Grafik", 
    "📈 3. Dashboard Interaktif (Wireframe)"
])

# ==========================================
# TAB 1: DESKRIPSI & PREVIEW DATA
# ==========================================
with tab1:
    st.header("1. Sumber Dataset & Deskripsi")
    st.write("""
    * **Sumber Dataset:** Kaggle (Retail Sales Data with Seasonal Trends & Marketing).
    * **Deskripsi:** Dataset ini berisi catatan penjualan ritel dan gudang dari berbagai pemasok (supplier) dan kategori produk (seperti Wine, Beer, Liquor) dari bulan Januari hingga September tahun 2020. Data ini digunakan untuk melacak volume penjualan dan pergerakan barang.
    """)
    
    st.header("5. Pratinjau Data (5 Baris Pertama)")
    # Menampilkan 5 baris pertama sesuai instruksi
    st.dataframe(df.head(5), use_container_width=True)

# ==========================================
# TAB 2: PERTANYAAN BISNIS & PILIHAN GRAFIK
# ==========================================
with tab2:
    st.header("2 & 3. Pertanyaan Bisnis dan Pemilihan Grafik")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Q1: Apa saja 10 produk yang terjual paling banyak?**")
        st.success("**Grafik Pilihan:** Grafik Batang Horizontal (*Bar Chart*).")
        st.write("*Alasan:* Sangat efektif untuk membandingkan volume antar produk dan mudah membaca nama produk yang panjang pada sumbu Y.")
        
    with col2:
        st.info("**Q2: Bagaimana tren penjualan dari bulan ke bulan?**")
        st.success("**Grafik Pilihan:** Grafik Garis (*Line Chart*).")
        st.write("*Alasan:* Grafik garis adalah standar terbaik untuk menunjukkan pergerakan atau tren data seiring berjalannya waktu (time-series).")
        
    with col3:
        st.info("**Q3: Kategori produk apa yang menyumbang penjualan terbesar?**")
        st.success("**Grafik Pilihan:** Grafik Lingkaran (*Pie/Donut Chart*).")
        st.write("*Alasan:* Ideal untuk melihat proporsi atau persentase pangsa pasar dari setiap kategori terhadap total keseluruhan.")

# ==========================================
# TAB 3: DASHBOARD INTERAKTIF (WIREFRAME)
# ==========================================
with tab3:
    st.header("4. Wireframe Layout & Visualisasi")
    st.write("Gunakan **tombol filter di bawah** untuk berinteraksi dengan data. Angka ditampilkan langsung pada grafik.")
    
    # --- Tombol Filter Interaktif ---
    selected_kategori = st.radio(
        "Pilih Filter Kategori (Tombol Interaktif):",
        options=["Semua Kategori"] + list(df['ITEM TYPE'].dropna().unique()),
        horizontal=True
    )
    
    # Filter data berdasarkan tombol yang ditekan
    if selected_kategori == "Semua Kategori":
        filtered_df = df
    else:
        filtered_df = df[df['ITEM TYPE'] == selected_kategori]
        
    st.markdown("---")

    # --- Layout Atas: 2 Grafik Bersebelahan ---
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Top 10 Produk Terlaris")
        top_prod = filtered_df.groupby('ITEM DESCRIPTION', as_index=False)['TOTAL SALES'].sum()
        top_prod = top_prod.sort_values(by='TOTAL SALES', ascending=True).tail(10)
        
        # Bar Chart dengan angka yang jelas
        fig1 = px.bar(
            top_prod, x='TOTAL SALES', y='ITEM DESCRIPTION', orientation='h',
            text='TOTAL SALES', color='TOTAL SALES', color_continuous_scale='Viridis'
        )
        fig1.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig1.update_layout(height=400, coloraxis_showscale=False, margin=dict(l=0, r=50, t=30, b=0))
        st.plotly_chart(fig1, use_container_width=True)

    with col_chart2:
        st.subheader("Proporsi Penjualan per Kategori")
        if selected_kategori == "Semua Kategori":
            cat_sales = filtered_df.groupby('ITEM TYPE', as_index=False)['TOTAL SALES'].sum().sort_values(by='TOTAL SALES', ascending=False)
            if len(cat_sales) > 5:
                top_5 = cat_sales.head(5)
                others_val = cat_sales.iloc[5:]['TOTAL SALES'].sum()
                others_df = pd.DataFrame({'ITEM TYPE': ['Lainnya'], 'TOTAL SALES': [others_val]})
                cat_sales = pd.concat([top_5, others_df], ignore_index=True)
            
            fig2 = px.pie(
                cat_sales, values='TOTAL SALES', names='ITEM TYPE', hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            fig2.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning(f"Grafik proporsi kategori disembunyikan karena Anda sedang memfilter khusus kategori **{selected_kategori}**.")

    # --- Layout Bawah: 1 Grafik Memanjang ---
    st.subheader("Tren Total Penjualan Bulanan")
    monthly = filtered_df.groupby('DATE', as_index=False)['TOTAL SALES'].sum().sort_values('DATE')
    monthly['BULAN_STR'] = monthly['DATE'].dt.strftime('%b %Y')
    
    fig3 = px.line(
        monthly, x='DATE', y='TOTAL SALES', markers=True, text='TOTAL SALES'
    )
    # Angka yang tercetak langsung pada titik garis
    fig3.update_traces(
        texttemplate='%{text:,.0f}', textposition="top center",
        line=dict(color='#ff7f0e', width=4), marker=dict(size=12)
    )
    fig3.update_layout(
        height=350, margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="Bulan", yaxis_title="Total Penjualan"
    )
    st.plotly_chart(fig3, use_container_width=True)
    
