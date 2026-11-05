import streamlit as st
import os
import zipfile
import base64
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="Buscador y Visor Integrado",
    page_icon="📌",
    layout="wide"
)

# Estilos idénticos al formato de visor corporativo
st.markdown("""
    <style>
    .main-title { color: #0F4C81; font-family: sans-serif; font-weight: bold; margin-bottom: 5px; }
    .subtitle { color: #666666; font-size: 1rem; margin-bottom: 25px; }
    .viewer-title { background-color: #F4F7F9; padding: 12px; border-radius: 6px; border-left: 5px solid #0F4C81; font-weight: bold; font-size: 1.2rem; color: #1C3D5A; margin-top: 15px; margin-bottom: 15px; }
    .document-body { background-color: #ffffff; padding: 40px; border-radius: 8px; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); font-family: 'Segoe UI', Arial, sans-serif; color: #2D3748; line-height: 1.7; overflow-y: auto; max-height: 700px; }
    .document-body h1 { color: #1A202C; font-size: 1.6rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; margin-bottom: 15px; text-transform: uppercase; font-weight: bold; }
    .document-body p { margin-bottom: 12px; font-size: 1.05rem; }
    
    /* Estilos para tablas de Word extraídas */
    .word-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 0.95rem; }
    .word-table td, .word-table th { border: 1px solid #CBD5E1; padding: 10px; vertical-align: top; }
    .word-table th { background-color: #F8FAFC; font-weight: bold; text-align: left; }
    </style>
""", unsafe_allow_html=True)

# Extractor avanzado XML capaz de leer párrafos Y tablas de Word (.docx)
def convertir_docx_a_html_nativo(datos_bytes):
    try:
        from io import BytesIO
        with zipfile.ZipFile(BytesIO(datos_bytes)) as docx_zip:
            xml_content = docx_zip.read('word/document.xml')
            root = ET.fromstring(xml_content)
            namespaces = {
                'w': 'http://openxmlformats.org'
            }
            
            html_output = []
            
            # Recorremos el cuerpo del documento elemento por elemento (párrafos y tablas)
            body = root.find('.//w:body', namespaces)
            if body is not None:
                for el in body:
                    # 1. Si el elemento es un PÁRRAFO
                    if el.tag.endswith('p'):
                        textos_parrafo = [t.text for t in el.findall('.//w:t', namespaces) if t.text]
                        texto_completo = "".join(textos_parrafo).strip()
                        if texto_completo:
                            if len(texto_completo) < 100 and (texto_completo.isupper() or "SERVICIO" in texto_completo or "MANTENIMIENTO" in texto_completo or "FABRICACIÓN" in texto_completo):
                                html_output.append(f"<h1>{texto_completo}</h1>")
                            else:
                                html_output.append(f"<p>{texto_completo}</p>")
                    
                    # 2. Si el elemento es una TABLA (Muy común en planos y registros)
                    elif el.tag.endswith('tbl'):
                        html_output.append('<table class="word-table">')
                        for row in el.findall('.//w:tr', namespaces):
                            html_output.append('<tr>')
                            for cell in row.findall('.//w:tc', namespaces):
                                # Extraemos el texto de cada celda de la tabla
                                textos_celda = [t.text for t in cell.findall('.//w:t', namespaces) if t.text]
                                texto_celda_completo = "".join(textos_celda).strip()
                                html_output.append(f'<td>{texto_celda_completo}</td>')
                            html_output.append('</tr>')
                        html_output.append('</table>')
            
            if html_output:
                return "".join(html_output)
            return "<p style='color: #718096; font-style: italic;'>El documento de Word no contiene texto ni tablas legibles estructuradas.</p>"
    except Exception as e:
        return f"<p style='color: #E53E3E;'>Error al procesar la estructura interna del documento Word: {e}</p>"

def mostrar_pdf_seguro(datos_bytes):
    base64_pdf = base64.b64encode(datos_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def explorar_y_renderizar_panel(nombre_zip, titulo_seccion, clave_unica):
    st.markdown(f'<h2 class="main-title">📌 {titulo_seccion}</h2>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Explora las subcarpetas de forma automatizada desde el panel de selección.</p>', unsafe_allow_html=True)
    
    if os.path.exists(nombre_zip):
        try:
            with zipfile.ZipFile(nombre_zip, 'r') as z:
                lista_archivos = [f for f in z.namelist() if not f.endswith('/') and not f.startswith('__MACOSX')]
                
                if lista_archivos:
                    archivo_interno = st.selectbox(
                        "🔍 Selecciona un archivo para desplegar en el visor:",
                        ["-- Seleccionar documento --"] + lista_archivos,
                        key=f"select_{clave_unica}"
                    )
                    
                    if archivo_interno != "-- Seleccionar documento --":
                        nombre_limpio = os.path.basename(archivo_interno)
                        
                        with z.open(archivo_interno) as archivo_leido:
                            datos_archivo = archivo_leido.read()
                        
                        st.markdown(f'<div class="viewer-title">👁️ Vista Previa de: {nombre_limpio}</div>', unsafe_allow_html=True)
                        
                        st.download_button(
                            label="📥 Descargar archivo original",
                            data=datos_archivo,
                            file_name=nombre_limpio,
                            mime="application/octet-stream",
                            key=f"dl_btn_{clave_unica}_{nombre_limpio}"
                        )
                        
                        ext = archivo_interno.lower()
                        
                        if ext.endswith('.docx'):
                            html_documento = convertir_docx_a_html_nativo(datos_archivo)
                            st.markdown(f'<div class="document-body">{html_documento}</div>', unsafe_allow_html=True)
                        
                        elif ext.endswith('.pdf'):
                            mostrar_pdf_seguro(datos_archivo)
                        
                        elif ext.endswith(('.png', '.jpg', '.jpeg')):
                            st.image(datos_archivo, use_container_width=True)
                            
                        else:
                            st.info("La vista previa en pantalla no está disponible para este formato, pero puedes descargarlo.")
                else:
                    st.info("El archivo comprimido está vacío.")
        except Exception as e:
            st.error(f"Error al abrir el paquete de archivos: {e}")
    else:
        st.error(f"El archivo '{nombre_zip}' no está disponible en el servidor.")

# Estructura de pestañas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔴 Anillos", "🟠 Prioridad 2", "🟡 Prioridad 3", "🟢 Prioridad 4", "🟣 Prioridad 5", "⚙️ Mecanizado"
])

with tab1: explorar_y_renderizar_panel("FABRICACIÓN DE ANILLOS.zip", "Fabricación de Anillos", "p1")
with tab2: explorar_y_renderizar_panel("PRIORIDAD 2.zip", "Prioridad 2", "p2")
with tab3: explorar_y_renderizar_panel("PRIORIDAD 3.zip", "Prioridad 3", "p3")
with tab4: explorar_y_renderizar_panel("PRIORIDAD 4.zip", "Prioridad 4", "p4")
with tab5: explorar_y_renderizar_panel("PRIORIDAD 5.zip", "Prioridad 5", "p5")
with tab6: explorar_y_renderizar_panel("SERVICIO DE EMBOCINADO Y MECANIZADO D....zip", "Embocinado y Mecanizado", "p6")
