import streamlit as st
import pandas as pd
import os

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="SI-DAMA | Dashboard", 
    layout="wide", 
    page_icon="📊"
)

# --- CUSTOM CSS dengan warna soft ---
st.markdown("""
    <style>
    /* Background utama yang soft */
    .stApp { 
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
    }
    
    /* Teks dengan warna soft */
    h1, h2, h3, h4, p, span, .stMarkdown { 
        color: #495057 !important; 
    }
    
    /* Header dengan warna lebih gelap untuk kontras */
    h1 {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    h3 {
        color: #4a5568 !important;
        font-weight: 500 !important;
    }
    
    .st-caption {
        color: #6c757d !important;
    }
    
    /* Metric cards dengan warna soft */
    [data-testid="stMetricValue"] { 
        color: #2c5282 !important; 
        font-weight: 600;
        font-size: 1.8rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4a5568 !important;
        font-weight: 500;
    }
    
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #4299e1;
        transition: transform 0.2s;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar dengan warna soft */
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #334155 !important;
    }
    
    /* Button dengan warna soft */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 500;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Link button di sidebar */
    .stLinkButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
    }
    
    /* Divider dengan warna soft */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #e2e8f0 0%, #cbd5e0 50%, #e2e8f0 100%);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Selectbox styling */
    .stSelectbox, .stMultiSelect {
        background: white;
        border-radius: 8px;
    }
    
    /* Warning/info boxes */
    .stAlert {
        background: #fff3cd !important;
        color: #856404 !important;
        border-left: 4px solid #ffc107 !important;
        border-radius: 8px !important;
    }
    
    /* Progress bar atau status colors yang soft */
    .status-selesai {
        color: #2f855a !important;
        font-weight: 500;
    }
    
    .status-proses {
        color: #c05621 !important;
        font-weight: 500;
    }
    
    .status-ditolak {
        color: #c53030 !important;
        font-weight: 500;
    }
    
    /* Footer atau copyright */
    .footer {
        text-align: center;
        color: #a0aec0;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI LOAD LOGO AMAN ---
def display_logo(width_size=140):
    if os.path.exists("logosainsdata.png"):
        st.image("logosainsdata.png", width=width_size)
    else:
        st.warning("📸 Logo tidak ditemukan - menggunakan placeholder")
        # Placeholder dengan warna soft
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        width: {width_size}px; 
                        height: {width_size}px; 
                        border-radius: 20px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        margin: 10px 0;">
                <span style="color: white; font-size: {width_size//4}px; font-weight: bold;">SD</span>
            </div>
        """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_text = st.columns([1, 4])
with col_logo:
    display_logo(120)

with col_text:
    st.title("📋 SI-DAMA")
    st.markdown("### *Sistem Informasi Data Administrasi Mahasiswa*")
    st.markdown("📌 **Program Studi Sains Data ITERA**")
    st.caption("🔄 Monitoring real-time status pengajuan surat")

st.divider()

# --- KONEKSI DATA ---
SHEET_ID = "1zfToe3nlb4AlkqhEtL42KRhepuTXEDlVl9V6DbF-C_Y"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=10)
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"⚠️ Gagal memuat data: {str(e)}")
        return None

try:
    df = load_data(URL)
    if df is None:
        st.stop()
        
    df.columns = df.columns.str.strip()
    
    # Hapus Timestamp
    cols_to_drop = [c for c in df.columns if 'timestamp' in c.lower()]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
    
    # Rename Status
    original_status_col = "Status (Isi Belum diterima)"
    if original_status_col in df.columns:
        df = df.rename(columns={original_status_col: "Status"})
        
    # Tambahkan timestamp jika ada untuk sorting
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df = df.sort_values('Timestamp', ascending=False)
        
except Exception as e:
    st.error("⚠️ Gagal memproses data. Silakan cek koneksi.")
    st.stop()

# --- METRIK dengan warna soft ---
status_col = "Status"
if status_col in df.columns:
    df[status_col] = df[status_col].fillna('Belum Diproses')
    
    # Hitung metrik
    total = len(df)
    selesai = len(df[df[status_col].str.contains('Selesai|Diterima', case=False, na=False)])
    proses = len(df[df[status_col].str.contains('Proses|Belum', case=False, na=False)])
    ditolak = len(df[df[status_col].str.contains('Ditolak', case=False, na=False)])
    
    # Tampilkan metrics dalam grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Total Pengajuan", 
            value=total,
            delta=None
        )
    
    with col2:
        st.metric(
            label="✅ Selesai", 
            value=selesai,
            delta=f"{((selesai/total)*100):.1f}%" if total > 0 else "0%"
        )
    
    with col3:
        st.metric(
            label="⏳ Dalam Proses", 
            value=proses,
            delta=f"{((proses/total)*100):.1f}%" if total > 0 else "0%"
        )
    
    with col4:
        st.metric(
            label="❌ Ditolak", 
            value=ditolak,
            delta=f"{((ditolak/total)*100):.1f}%" if total > 0 else "0%"
        )

st.divider()

# --- SIDEBAR dengan warna soft ---
with st.sidebar:
    st.markdown("### 📊 **Panel Kontrol**")
    st.markdown("---")
    
    display_logo(80)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Perbaikan: Mengubah st.mark menjadi st.markdown
    st.markdown("### 🔍 Filter Data")
    
    jenis_col = "Jenis Surat"
    df_display = df.copy()
    
    if jenis_col in df.columns:
        # Bersihkan data null
        df[jenis_col] = df[jenis_col].fillna('Tidak Diketahui')
        
        # Filter multiselect dengan default semua
        semua_jenis = sorted(df[jenis_col].unique())
        pilihan = st.multiselect(
            "Pilih Kategori Surat:",
            options=semua_jenis,
            default=semua_jenis,
            help="Pilih satu atau lebih jenis surat"
        )
        
        if pilihan:
            df_display = df[df[jenis_col].isin(pilihan)]
    
    # Tambahkan filter pencarian
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔎 Pencarian")
    search_term = st.text_input("Cari berdasarkan Nama/NIM:", placeholder="Ketik keyword...")
    
    if search_term:
        # Cari di semua kolom string
        mask = df_display.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        df_display = df_display[mask]
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Statistik Filter")
    
    # Tampilkan statistik filter
    if status_col in df_display.columns:
        st.info(f"""
        **Data yang ditampilkan:**  
        - Total: {len(df_display)} dari {len(df)} data
        - Selesai: {len(df_display[df_display[status_col].str.contains('Selesai|Diterima', case=False, na=False)])}
        - Proses: {len(df_display[df_display[status_col].str.contains('Proses|Belum', case=False, na=False)])}
        - Ditolak: {len(df_display[df_display[status_col].str.contains('Ditolak', case=False, na=False)])}
        """)
    else:
        st.info(f"**Data yang ditampilkan:** {len(df_display)} dari {len(df)} data")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    
    # Form button dengan warna soft
    st.markdown("### 📝 Formulir Pengajuan")
    st.link_button(
        "✨ Buat Pengajuan Baru", 
        "https://forms.gle/Uakf34AifyZGvmW69", 
        use_container_width=True
    )
    
    # Export data button
    if st.button("📥 Export Data ke CSV", use_container_width=True):
        csv = df_display.to_csv(index=False)
        st.download_button(
            label="📎 Download CSV",
            data=csv,
            file_name="data_administrasi.csv",
            mime="text/csv",
            use_container_width=True
        )

# --- TABEL UTAMA ---
st.subheader("📋 **Detail Status Administrasi**")
st.caption(f"Menampilkan {len(df_display)} dari {len(df)} data")

# Format dataframe untuk tampilan lebih baik
if not df_display.empty:
    # Definisikan fungsi untuk styling
    def highlight_status(val):
        if pd.isna(val):
            return ''
        if isinstance(val, str):
            if 'selesai' in val.lower() or 'diterima' in val.lower():
                return 'background-color: #e6f7e6'
            elif 'proses' in val.lower() or 'belum' in val.lower():
                return 'background-color: #fff3e0'
            elif 'ditolak' in val.lower():
                return 'background-color: #ffe6e6'
        return ''
    
    # Apply styling jika kolom status ada
    if status_col in df_display.columns:
        styled_df = df_display.style.applymap(highlight_status, subset=[status_col])
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Nama": st.column_config.TextColumn("Nama Lengkap", width="medium"),
                "NIM": st.column_config.TextColumn("NIM", width="small"),
                "Jenis Surat": st.column_config.TextColumn("Jenis Surat", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            }
        )
    else:
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
else:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter")

st.divider()

# --- FOOTER dan REFRESH ---
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button('🔄 Refresh Data', use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with col3:
    st.markdown(f"<p style='text-align: right; color: #a0aec0;'>Update terakhir: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}</p>", 
                unsafe_allow_html=True)

# Copyright
st.markdown("""
    <div class="footer">
        © 2024 Program Studi Sains Data ITERA | SI-DAMA v2.0
    </div>
""", unsafe_allow_html=True)