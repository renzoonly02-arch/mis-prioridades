import streamlit as st
import os
import zipfile
import base64
import xml.etree.ElementTree as ET

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
    .word-text-box { background-color: #ffffff; padding: 25px; border-radius: 8px; border: 1px solid #E0E0E0; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); font-family: 'Segoe UI', Arial, sans-serif; white-space: pre-wrap; line-height: 1.6; color: #333333; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📌 Panel Interactivo de Documentos</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explora y lee los documentos de Word, PDF e imágenes en tiempo real sin salir de la página</p>', unsafe_allow_html=True)

# Función automática para extraer el texto de un Word (.docx) sin librerías externas
def extraer_texto_docx(datos_bytes):
    try:
        # Un archivo .docx es internamente un conjunto de archivos XML comprimidos
        from io import BytesIO
        with zipfile.ZipFile(BytesIO(datos_bytes)) as docx_zip:
            # El contenido del texto principal de Word siempre se guarda en word/document.xml
            xml_content = docx_zip.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            # Buscamos todas las etiquetas de texto del estándar de Microsoft Word
            namespaces = {'w': 'http://openxmlformats.org'}
            parrafos = []
            for p in root.findall('.//w:p', namespaces):
                textos_parrafo = [t.text for t in p.findall('.//w:t', namespaces) if t.text]
                if textos_parrafo:
                    parrafos.append("".join(textos_parrafo))
                else:
                    parrafos.append("") # Mantiene los saltos de línea vacíos
            
            return "\n".join(parrafos)
    except Exception as e:
        return f"Error al leer el texto del documento Word de forma nativa: {e}"

def mostrar_pdf_incrustado(datos_bytes):
    base64_pdf = base64.b64encode(datos_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

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
                        st.write(f"**Visualizando contenido de:** `{os.path.basename(archivo_interno)}`")
                        
                        with z.open(archivo_interno) as archivo_leido:
                            datos_archivo = archivo_leido.read()
                        
                        ext = archivo_interno.lower()
                        
                        # Si es un archivo de WORD (.docx)
                        if ext.endswith('.docx'):
                            texto_extraido = extraer_texto_docx(datos_archivo)
                            st.markdown(f'<div class="word-text-box">{texto_extraido}</div>', unsafe_allow_html=True)
                        
                        # Si es un PDF
                        elif ext.endswith('.pdf'):
                            mostrar_pdf_incrustado(datos_archivo)
                        
                        # Si es una Imagen
                        elif ext.endswith(('.png', '.jpg', '.jpeg')):
                            st.image(datos_archivo, use_container_width=True)
                        
                        # Archivos planos de texto básicos
                        elif ext.endswith(('.txt', '.csv')):
                            st.text(datos_archivo.decode('utf-8', errors='ignore'))
                        
                        else:
                            st.warning("Formato no soportado para lectura directa. Descárgalo individualmente:")
                            st.download_button("📥 Descargar Archivo Individual", datos_archivo, file_name=os.path.basename(archivo_interno), key=f"dl_ind_{clave_unica}")
                else:
                    st.info("El archivo ZIP se encuentra vacío.")
        except Exception as e:
            st.error(f"Error al intentar abrir el archivo comprimido de forma virtual: {e}")
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
