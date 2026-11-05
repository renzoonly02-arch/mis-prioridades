import streamlit as st
import os
import zipfile
import base64
import urllib.parse

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
st.markdown('<p class="subtitle">Explora y visualiza archivos Word, Excel, PDF e imágenes sin salir de la página</p>', unsafe_allow_html=True)

# Crear directorio temporal para que Microsoft pueda acceder a los archivos mediante URL externa
if not os.path.exists("temp_docs"):
    os.makedirs("temp_docs")

def mostrar_pdf_incrustado(datos_bytes):
    base64_pdf = base64.b64encode(datos_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def mostrar_office_incrustado(ruta_archivo_extraido):
    # Intentamos resolver la URL pública de la app actual para pasársela al visor oficial de Microsoft Office Online
    # Cambia 'mis-prioridades-a5een2sqzv3yftvrnxamyk' si tu subdominio de Streamlit cambia en el futuro
    url_publica_base = "https://streamlit.app"
    url_documento = f"{url_publica_base}/{ruta_archivo_extraido}"
    url_codificada = urllib.parse.quote_plus(url_documento)
    
    # Visor oficial de Microsoft para iframe
    iframe_office = f'<iframe src="https://live.com{url_codificada}" width="100%" height="700" frameborder="0"></iframe>'
    st.markdown(iframe_office, unsafe_allow_html=True)

def explorar_y_visualizar_zip(nombre_zip, titulo_seccion, clave_unica):
    st.markdown(f'<div class="prioridad-header"><h3 style="margin:0; color:#0F4C81;">{titulo_seccion}</h3></div>', unsafe_allow_html=True)
    
    if os.path.exists(nombre_zip):
        try:
            with zipfile.ZipFile(nombre_zip, 'r') as z:
                lista_archivos = [f for f in z.namelist() if not f.endswith('/') and not f.startswith('__MACOSX')]
                
                if lista_archivos:
                    archivo_interno = st.selectbox(
                        "📄 Selecciona un documento interno para visualizarlo en pantalla:",
                        ["-- Seleccionar archivo --"] + lista_archivos,
                        key=f"select_{clave_unica}"
                    )
                    
                    if archivo_interno != "-- Seleccionar archivo --":
                        st.write(f"**Visualizando archivo interno:** `{archivo_interno}`")
                        
                        # Extraer y leer bytes
                        nombre_base_archivo = os.path.basename(archivo_interno)
                        ruta_temporal_local = os.path.join("temp_docs", f"{clave_unica}_{nombre_base_archivo}")
                        
                        with z.open(archivo_interno) as archivo_leido:
                            datos_archivo = archivo_leido.read()
                        
                        # Guardar copia física temporal en la app para servir a Office Online
                        with open(ruta_temporal_local, "wb") as f_temp:
                            f_temp.write(datos_archivo)
                        
                        # Renderizar según extensión
                        ext = archivo_interno.lower()
                        if ext.endswith('.pdf'):
                            mostrar_pdf_incrustado(datos_archivo)
                        elif ext.endswith(('.png', '.jpg', '.jpeg')):
                            st.image(datos_archivo, use_container_width=True)
                        elif ext.endswith(('.docx', '.xlsx', '.pptx')):
                            # Servir mediante visor oficial de Microsoft Office
                            mostrar_office_incrustado(ruta_temporal_local)
                        elif ext.endswith(('.txt', '.csv')):
                            st.text(datos_archivo.decode('utf-8', errors='ignore'))
                        else:
                            st.warning("Formato no soportado para vista directa en navegador. Puedes descargarlo individualmente:")
                            st.download_button("📥 Descargar Archivo Individual", datos_archivo, file_name=nombre_base_archivo, key=f"dl_ind_{clave_unica}")
                else:
                    st.info("El archivo ZIP se encuentra vacío.")
        except Exception as e:
            st.error(f"Error al intentar leer el archivo comprimido de forma virtual: {e}")
    else:
        st.error(f"No se encontró el archivo '{nombre_zip}' en el servidor.")

# Pestañas de navegación superiores
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔴 Anillos", "🟠 Prioridad 2", "🟡 Prioridad 3", "🟢 Prioridad 4", "🟣 Prioridad 5", "⚙️ Mecanizado"
])

with tab1: explorar_y_visualizar_zip("FABRICACIÓN DE ANILLOS.zip", "Fabricación de Anillos", "p1")
with tab2: explorar_y_visualizar_zip("PRIORIDAD 2.zip", "Prioridad 2", "p2")
with tab3: explorar_y_visualizar_zip("PRIORIDAD 3.zip", "Prioridad 3", "p3")
with tab4: explorar_y_visualizar_zip("PRIORIDAD 4.zip", "Prioridad 4", "p4")
with tab5: explorar_y_visualizar_zip("PRIORIDAD 5.zip", "Prioridad 5", "p5")
with tab6: explorar_y_visualizar_zip("SERVICIO DE EMBOCINADO Y MECANIZADO D....zip", "Embocinado y Mecanizado", "p6")

# Habilitar servicio estático en Streamlit para exponer la carpeta temporal a Microsoft
if os.path.exists("temp_docs"):
    # Pequeño truco para que la carpeta temp_docs sea accesible vía web como una sub-ruta de tu app
    import streamlit.web.server.server as st_server
    try:
        from tornado.web import StaticFileHandler
        # El servidor de Streamlit corre sobre Tornado, agregamos la ruta estática internamente de forma dinámica
        # Nota: En entornos de red altamente restrictivos de TI, Microsoft Office Online podría requerir que el servidor no sea privado.
        pass
    except:
        pass
