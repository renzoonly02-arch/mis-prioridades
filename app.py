import streamlit as st
import os
import zipfile
import base64

st.set_page_config(
    page_title="Panel de Prioridades",
    page_icon="📌",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title { color: #0F4C81; font-family: sans-serif; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #555555; text-align: center; font-size: 1.1rem; margin-bottom: 30px; }
    .prioridad-header { padding: 10px; border-radius: 8px; background-color: #F4F7F9; border-left: 6px solid #0F4C81; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📌 Panel Interactivo de Documentos</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explora y visualiza los archivos internos de cada prioridad en tiempo real sin salir de la página</p>', unsafe_allow_html=True)

# Función para incrustar PDFs en la interfaz de Streamlit
def mostrar_pdf_incrustado(datos_bytes):
    base64_pdf = base64.b64encode(datos_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Función principal para abrir el ZIP de forma virtual y leer sus componentes internos
def explorar_y_visualizar_zip(nombre_zip, titulo_seccion, clave_unica):
    st.markdown(f'<div class="prioridad-header"><h3 style="margin:0; color:#0F4C81;">{titulo_seccion}</h3></div>', unsafe_allow_html=True)
    
    if os.path.exists(nombre_zip):
        try:
            # Abrimos el archivo comprimido sin extraerlo en el disco duro
            with zipfile.ZipFile(nombre_zip, 'r') as z:
                # Obtenemos la lista de nombres de todos los archivos contenidos
                lista_archivos = [f for f in z.namelist() if not f.endswith('/') and not f.startswith('__MACOSX')]
                
                if lista_archivos:
                    # Menú desplegable para que el usuario seleccione el archivo interno a visualizar
                    archivo_interno = st.selectbox(
                        "📄 Selecciona un documento interno para visualizarlo en pantalla:",
                        ["-- Seleccionar archivo --"] + lista_archivos,
                        key=f"select_{clave_unica}"
                    )
                    
                    if archivo_interno != "-- Seleccionar archivo --":
                        st.write(f"**Visualizando archivo interno:** `{archivo_interno}`")
                        
                        # Leer los bytes del archivo directamente desde la memoria del ZIP
                        with z.open(archivo_interno) as archivo_leido:
                            datos_archivo = archivo_leido.read()
                        
                        # Renderizar visor según el formato detectado
                        if archivo_interno.lower().endswith('.pdf'):
                            mostrar_pdf_incrustado(datos_archivo)
                        elif archivo_interno.lower().endswith(('.png', '.jpg', '.jpeg')):
                            st.image(datos_archivo, use_container_width=True)
                        elif archivo_interno.lower().endswith(('.txt', '.csv')):
                            st.text(datos_archivo.decode('utf-8', errors='ignore'))
                        else:
                            st.warning("Este formato de archivo no soporta previsualización web directa en esta versión. Puedes descargarlo individualmente aquí:")
                            st.download_button("📥 Descargar Archivo Individual", datos_archivo, file_name=os.path.basename(archivo_interno), key=f"dl_ind_{clave_unica}")
                else:
                    st.info("El archivo ZIP se encuentra vacío.")
        except Exception as e:
            st.error(f"Error al intentar leer el archivo comprimido de forma virtual: {e}")
    else:
        st.error(f"No se encontró el archivo '{nombre_zip}' en el servidor.")

# Organización de las pestañas superiores del portal web corporativo
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔴 Anillos", "🟠 Prioridad 2", "🟡 Prioridad 3", "🟢 Prioridad 4", "🟣 Prioridad 5", "⚙️ Mecanizado"
])

with tab1:
    explorar_y_visualizar_zip("FABRICACIÓN DE ANILLOS.zip", "Fabricación de Anillos", "p1")

with tab2:
    explorar_y_visualizar_zip("PRIORIDAD 2.zip", "Prioridad 2", "p2")

with tab3:
    explorar_y_visualizar_zip("PRIORIDAD 3.zip", "Prioridad 3", "p3")

with tab4:
    explorar_y_visualizar_zip("PRIORIDAD 4.zip", "Prioridad 4", "p4")

with tab5:
    explorar_y_visualizar_zip("PRIORIDAD 5.zip", "Prioridad 5", "p5")

with tab6:
    explorar_y_visualizar_zip("SERVICIO DE EMBOCINADO Y MECANIZADO D....zip", "Embocinado y Mecanizado", "p6")
