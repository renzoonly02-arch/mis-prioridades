import os
import streamlit as st
import zipfile
import mammoth

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="CARVIMSA - PLANTA MOLINO",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS REFORZADOS (ESTILO CARVIMSA ORIGINAL) ---
st.markdown("""
    <style>
    /* Fondo general azul oscuro de CARVIMSA */
    .stApp {
        background-color: #0d1b2a !important;
        color: #ffffff !important;
    }
    /* Panel Lateral Izquierdo */
    [data-testid="stSidebar"] {
        background-color: #1b263b !important;
        border-right: 1px solid #415a77;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* Estilo para los botones de la lista de archivos */
    .stButton > button {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid #415a77 !important;
        text-align: left !important;
        display: block !important;
        width: 100% !important;
        padding: 10px !important;
        font-size: 13px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        border-radius: 6px !important;
    }
    .stButton > button:hover {
        border-color: #38bdf8 !important;
        background-color: #0f172a !important;
        color: #38bdf8 !important;
    }
    
    /* Banner Superior Azul */
    .banner-principal {
        background: linear-gradient(135deg, #0077b6, #0096c7);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Caja de la Vista Previa (Máxima legibilidad) */
    .contenedor-vista-previa {
        background-color: #ffffff !important;
        color: #1e293b !important;
        padding: 30px;
        border-radius: 10px;
        border: 3px solid #0077b6;
        min-height: 500px;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-top: 15px;
        overflow-y: auto;
        max-height: 750px;
    }
    .contenedor-vista-previa h1, .contenedor-vista-previa h2, .contenedor-vista-previa h3 {
        color: #0f172a !important;
        border-bottom: 2px solid #cbd5e1;
        padding-bottom: 8px;
        margin-top: 15px;
    }
    .contenedor-vista-previa p, .contenedor-vista-previa li, .contenedor-vista-previa td, .contenedor-vista-previa tr {
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #1e293b !important;
    }
    .contenedor-vista-previa table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 15px;
    }
    .contenedor-vista-previa th, .contenedor-vista-previa td {
        border: 1px solid #cbd5e1;
        padding: 8px;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. SELECCIÓN DE PESTAÑA DE PRIORIDAD ---
# Definición de mapeo entre pestañas y los archivos ZIP reales que ya tienes arriba
opciones_zip = {
    "🔴 Anillos": "FABRICACIÓN DE ANILLOS.zip",
    "🟠 Prioridad 2": "PRIORIDAD 2.zip",
    "🟡 Prioridad 3": "PRIORIDAD 3.zip",
    "🟢 Prioridad 4": "PRIORIDAD 4.zip",
    "🟣 Prioridad 5": "PRIORIDAD 5.zip",
    "⚙️ Mecanizado": "SERVICIO DE EMBOCINADO Y MECANIZADO D....zip"
}

pestanas = list(opciones_zip.keys())
pestana_seleccionada = st.radio("📁 SELECCIONA LA PRIORIDAD A CONSULTAR:", pestanas, horizontal=True)
archivo_zip_actual = opciones_zip[pestana_seleccionada]

# --- VARIABLES DE MEMORIA EN SESIÓN ---
if "archivo_activo_zip" not in st.session_state:
    st.session_state.archivo_activo_zip = None

# --- OBTENER LOS ARCHIVOS DEL ZIP SELECCIONADO ---
archivos_disponibles = []
if os.path.exists(archivo_zip_actual):
    try:
        with zipfile.ZipFile(archivo_zip_actual, 'r') as z:
            # Extrae todos los documentos de Word ignorando archivos temporales basura de Mac o Windows
            archivos_disponibles = [
                f for f in z.namelist() 
                if f.lower().endswith('.docx') and not f.startswith('__MACOSX') and not os.path.basename(f).startswith('.') and not os.path.basename(f).startswith('~$')
            ]
            archivos_disponibles.sort()
            
            # Si cambiamos de pestaña o no hay archivo activo, selecciona el primero
            if archivos_disponibles:
                if st.session_state.archivo_activo_zip not in archivos_disponibles:
                    st.session_state.archivo_activo_zip = archivos_disponibles[0]
    except Exception as e:
        st.sidebar.error(f"Error al abrir el paquete ZIP: {str(e)}")

# --- 2. PANEL LATERAL IZQUIERDO (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; margin-bottom:0;'>CARVIMSA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; color:#94a3b8; text-align:center; margin-top:0;'>GRUPO COMECA - PERÚ</p>", unsafe_allow_html=True)
    st.write("---")
    
    buscar = st.text_input("🔍 Filtrar archivos de la lista:", placeholder="Escribe aquí para buscar...")
    st.write("---")
    
    if buscar:
        archivos_mostrar = [f for f in archivos_disponibles if buscar.strip().lower() in f.lower()]
    else:
        archivos_mostrar = archivos_disponibles

    st.markdown(f"### 📂 DOCUMENTOS ({len(archivos_mostrar)})")
    
    for f_path in archivos_mostrar:
        f_name_clean = os.path.basename(f_path)
        marca = "▶️ " if f_path == st.session_state.archivo_activo_zip else "📄 "
        if st.button(f"{marca}{f_name_clean}", key=f"btn_lista_{f_path}", use_container_width=True):
            st.session_state.archivo_activo_zip = f_path
            st.rerun()

# --- 3. ÁREA PRINCIPAL (PANEL DE VISTA PREVIA) ---
st.markdown("""
    <div class="banner-principal">
        <span style="background-color:#ffffff; color:#0077b6; padding:4px 10px; border-radius:20px; font-size:11px; font-weight:bold;">📌 CATÁLOGO DE PLANTA • VISTA PREVIA</span>
        <h1 style="color:white; margin-top:10px; margin-bottom:0; font-size:32px;">CARVIMSA - PLANTA MOLINO</h1>
        <p style="color:#e0e1dd; margin-top:5px; font-size:14px;">Consulta en tiempo real de documentos técnicos en pantalla.</p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.archivo_activo_zip and os.path.exists(archivo_zip_actual):
    archivo_actual = st.session_state.archivo_activo_zip
    nombre_limpio_pantalla = os.path.basename(archivo_actual)
    
    st.markdown(f"<h3 style='color: #38bdf8;'>👁️ Vista Previa Activa: <span style='color: white;'>{nombre_limpio_pantalla}</span></h3>", unsafe_allow_html=True)
    
    # --- PROCESAR CON MAMMOTH DESDE LA MEMORIA VIRTUAL DEL ZIP ---
    try:
        with zipfile.ZipFile(archivo_zip_actual, 'r') as z:
            with z.open(archivo_actual) as docx_file:
                # El truco: mammoth lee los bytes crudos directamente de la descompresión en memoria
                resultado = mammoth.convert_to_html(docx_file, ignore_empty_paragraphs=True)
                html_contenido = resultado.value
                
                # Formatear subniveles de listas conflictivas
                html_contenido = html_contenido.replace("<li>1. ", "<li style='list-style-type: none; margin-left: -15px;'>🔹 <b>")
                
                if not html_contenido.strip():
                    html_contenido = "<p style='color: #64748b; font-style: italic;'>El documento seleccionado está vacío o no contiene texto legible.</p>"
                
                # Botón opcional de descarga por si el usuario desea guardarse el original
                st.download_button(
                    label="📥 Descargar Word original",
                    data=z.read(archivo_actual),
                    file_name=nombre_limpio_pantalla,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                
                st.markdown(f"""
                    <div class="contenedor-vista-previa">
                        {html_contenido}
                    </div>
                """, unsafe_allow_html=True)
                
    except Exception as err_lectura:
        st.error(f"No se pudo cargar la vista previa con Mammoth: {str(err_lectura)}")
else:
    if not archivos_disponibles:
        st.error(f"❌ No se detectan archivos de Word (.docx) dentro del paquete '{archivo_zip_actual}'.")
    else:
        st.info("👈 Selecciona un archivo de la lista lateral izquierda para ver su contenido.")
