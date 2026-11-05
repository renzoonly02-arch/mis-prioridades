import streamlit as st
import os
import zipfile

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
    .action-container { background-color: #ffffff; padding: 25px; border-radius: 8px; border: 1px solid #E0E0E0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); text-align: center; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📌 Panel Interactivo de Documentos</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explora y abre tus documentos de forma segura en una nueva pestaña del navegador</p>', unsafe_allow_html=True)

def explorar_y_visualizar_zip(nombre_zip, titulo_seccion, clave_unica):
    st.markdown(f'<div class="prioridad-header"><h3 style="margin:0; color:#0F4C81;">{titulo_seccion}</h3></div>', unsafe_allow_html=True)
    
    if os.path.exists(nombre_zip):
        try:
            with zipfile.ZipFile(nombre_zip, 'r') as z:
                lista_archivos = [f for f in z.namelist() if not f.endswith('/') and not f.startswith('__MACOSX')]
                
                if lista_archivos:
                    archivo_interno = st.selectbox(
                        "📄 Selecciona un documento interno para visualizarlo:",
                        ["-- Seleccionar archivo --"] + lista_archivos,
                        key=f"select_{clave_unica}"
                    )
                    
                    if archivo_interno != "-- Seleccionar archivo --":
                        nombre_limpio = os.path.basename(archivo_interno)
                        st.write(f"**Documento seleccionado:** `{nombre_limpio}`")
                        
                        with z.open(archivo_interno) as archivo_leido:
                            datos_archivo = archivo_leido.read()
                        
                        ext = archivo_interno.lower()
                        # Determinar el tipo de contenido adecuado para el navegador
                        if ext.endswith('.pdf'):
                            tipo_mime = "application/pdf"
                        elif ext.endswith('.docx'):
                            tipo_mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        elif ext.endswith('.xlsx'):
                            tipo_mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        elif ext.endswith('.png'):
                            tipo_mime = "image/png"
                        elif ext.endswith(('.jpg', '.jpeg')):
                            tipo_mime = "image/jpeg"
                        else:
                            tipo_mime = "application/octet-stream"
                        
                        st.markdown('<div class="action-container">', unsafe_allow_html=True)
                        st.success(f"¡Archivo '{nombre_limpio}' procesado exitosamente!")
                        
                        # Botón nativo de apertura y descarga segura (salta todos los bloqueos de Chrome)
                        st.download_button(
                            label=f"👁️ Ver / Descargar: {nombre_limpio}",
                            data=datos_archivo,
                            file_name=nombre_limpio,
                            mime=tipo_mime,
                            key=f"btn_open_{clave_unica}_{nombre_limpio}"
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("El archivo ZIP se encuentra vacío.")
        except Exception as e:
            st.error(f"Error al intentar abrir el archivo comprimido: {e}")
    else:
        st.error(f"No se encontró el archivo '{nombre_zip}' en el servidor.")

# Pestañas del Panel Corporativo
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔴 Anillos", "🟠 Prioridad 2", "🟡 Prioridad 3", "🟢 Prioridad 4", "🟣 Prioridad 5", "⚙️ Mecanizado"
])

with tab1: explorar_y_visualizar_zip("FABRICACIÓN DE ANILLOS.zip", "Fabricación de Anillos", "p1")
with tab2: explorar_y_visualizar_zip("PRIORIDAD 2.zip", "Prioridad 2", "p2")
with tab3: explorar_y_visualizar_zip("PRIORIDAD 3.zip", "Prioridad 3", "p3")
with tab4: explorar_y_visualizar_zip("PRIORIDAD 4.zip", "Prioridad 4", "p4")
with tab5: explorar_y_visualizar_zip("PRIORIDAD 5.zip", "Prioridad 5", "p5")
with tab6: explorar_y_visualizar_zip("SERVICIO DE EMBOCINADO Y MECANIZADO D....zip", "Embocinado y Mecanizado", "p6")
