import streamlit as st
import os
import zipfile
import base64
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="Visor Dual de Documentos",
    page_icon="📌",
    layout="wide"
)

# Estilos corporativos profesionales con fondos limpios
st.markdown("""
    <style>
    .main-title { color: #0F4C81; font-family: sans-serif; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #555555; text-align: center; font-size: 1rem; margin-bottom: 25px; }
    .viewer-title { background-color: #F4F7F9; padding: 10px; border-radius: 6px; border-left: 5px solid #0F4C81; font-weight: bold; font-size: 1.1rem; color: #1C3D5A; margin-bottom: 15px; }
    .word-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 0.95rem; }
    .word-table td, .word-table th { border: 1px solid #CBD5E1; padding: 10px; vertical-align: top; }
    .word-table th { background-color: #F8FAFC; font-weight: bold; }
    .document-body { background-color: #ffffff; padding: 30px; border-radius: 8px; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); font-family: 'Segoe UI', Arial, sans-serif; color: #2D3748; line-height: 1.7; overflow-y: auto; max-height: 750px; }
    .document-body h1 { color: #1A202C; font-size: 1.4rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; margin-bottom: 15px; text-transform: uppercase; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📌 Panel Interactivo Dual</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Visualiza tus documentos de Word y PDF de forma simultánea en la misma pantalla</p>', unsafe_allow_html=True)

# Lector XML avanzado para extraer textos y tablas de Word (.docx)
def convertir_docx_a_html_nativo(datos_bytes):
    try:
        from io import BytesIO
        with zipfile.ZipFile(BytesIO(datos_bytes)) as docx_zip:
            xml_content = docx_zip.read('word/document.xml')
            root = ET.fromstring(xml_content)
            namespaces = {'w': 'http://openxmlformats.org'}
            html_output = []
            body = root.find('.//w:body', namespaces)
            if body is not None:
                for el in body:
                    if el.tag.endswith('p'):
                        textos_parrafo = [t.text for t in el.findall('.//w:t', namespaces) if t.text]
                        texto_completo = "".join(textos_parrafo).strip()
                        if texto_completo:
                            if len(texto_completo) < 120 and (texto_completo.isupper() or "SERVICIO" in texto_completo or "MANTENIMIENTO" in texto_completo or "FABRICACIÓN" in texto_completo or "COT" in texto_completo):
                                html_output.append(f"<h1>{texto_completo}</h1>")
                            else:
                                html_output.append(f"<p>{texto_completo}</p>")
                    elif el.tag.endswith('tbl'):
                        html_output.append('<table class="word-table">')
                        for row in el.findall('.//w:tr', namespaces):
                            html_output.append('<tr>')
                            for cell in row.findall('.//w:tc', namespaces):
                                textos_celda = [t.text for t in cell.findall('.//w:t', namespaces) if t.text]
                                html_output.append(f'<td>{"".join(textos_celda).strip()}</td>')
                            html_output.append('</tr>')
                        html_output.append('</table>')
            return "".join(html_output) if html_output else "<p style='color: #718096; font-style: italic;'>Este archivo no contiene párrafos de texto plano o tablas editables estándar (podría contener solo imágenes pegadas).</p>"
    except Exception as e:
        return f"<p style='color:red;'>Error al procesar el archivo Word internamente: {e}</p>"

# Visor de PDFs optimizado usando el componente HTML dinámico de Streamlit
def mostrar_pdf_seguro(datos_bytes):
    try:
        base64_pdf = base64.b64encode(datos_bytes).decode('utf-8')
        pdf_html = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" 
                    width="100%" height="730px" 
                    style="border:none; border-radius:8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);" 
                    allowfullscreen>
            </iframe>
        """
        st.components.v1.html(pdf_html, height=750, scrolling=False)
    except Exception as e:
        st.error(f"Error al proyectar el PDF: {e}")

def explorar_y_renderizar_dual(nombre_zip, titulo_seccion, clave_unica):
    if os.path.exists(nombre_zip):
        try:
            with zipfile.ZipFile(nombre_zip, 'r') as z:
                # Filtrar solo archivos verdaderos ignorando carpetas del sistema Mac o basura oculta
                lista_archivos = [f for f in z.namelist() if not f.endswith('/') and not f.startswith('__MACOSX') and not os.path.basename(f).startswith('.')]
                
                if lista_archivos:
                    col_sel_word, col_sel_pdf = st.columns(2)
                    
                    with col_sel_word:
                        archivos_word = [f for f in lista_archivos if f.lower().endswith('.docx')]
                        # Formateamos el menú para que muestre una visualización más cómoda del nombre del archivo largo
                        word_seleccionado = st.selectbox(
                            "📝 Selecciona el documento WORD:", 
                            ["-- Seleccionar Word --"] + archivos_word, 
                            key=f"w_{clave_unica}",
                            format_func=lambda x: os.path.basename(x) if x != "-- Seleccionar Word --" else x
                        )
                    
                    with col_sel_pdf:
                        archivos_pdf = [f for f in lista_archivos if f.lower().endswith('.pdf')]
                        pdf_seleccionado = st.selectbox(
                            "📄 Selecciona el documento PDF:", 
                            ["-- Seleccionar PDF --"] + archivos_pdf, 
                            key=f"p_{clave_unica}",
                            format_func=lambda x: os.path.basename(x) if x != "-- Seleccionar PDF --" else x
                        )
                    
                    col_visor_word, col_visor_pdf = st.columns(2)
                    
                    # Columna Izquierda: Visor del Word
                    with col_visor_word:
                        st.markdown('<div class="viewer-title">👁️ Vista Previa del Word</div>', unsafe_allow_html=True)
                        if word_seleccionado != "-- Seleccionar Word --":
                            with z.open(word_seleccionado) as f_word:
                                html_word = convertir_docx_a_html_nativo(f_word.read())
                            st.markdown(f'<div class="document-body">{html_word}</div>', unsafe_allow_html=True)
                            
                            # Agregamos botón de descarga por si quieren conservar el original
                            st.download_button("📥 Descargar Word original", z.read(word_seleccionado), file_name=os.path.basename(word_seleccionado), key=f"dl_w_{clave_unica}")
                        else:
                            st.info("Selecciona un archivo Word en el menú de arriba para leerlo aquí.")
                            
                    # Columna Derecha: Visor del PDF
                    with col_visor_pdf:
                        st.markdown('<div class="viewer-title">👁️ Vista Previa del PDF</div>', unsafe_allow_html=True)
                        if pdf_seleccionado != "-- Seleccionar PDF --":
                            with z.open(pdf_seleccionado) as f_pdf:
                                mostrar_pdf_seguro(f_pdf.read())
                                
                            # Agregamos botón de descarga por si quieren conservar el original
                            st.download_button("📥 Descargar PDF original", z.read(pdf_seleccionado), file_name=os.path.basename(pdf_seleccionado), key=f"dl_p_{clave_unica}")
                        else:
                            st.info("Selecciona un archivo PDF en el menú de arriba para proyectarlo aquí.")
                else:
                    st.info("El archivo comprimido está vacío.")
        except Exception as e:
            st.error(f"Error al abrir el paquete comprimido: {e}")
    else:
        st.error(f"El paquete '{nombre_zip}' no está disponible.")

# Estructura de Pestañas Principales por áreas de prioridad
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔴 Anillos", "🟠 Prioridad 2", "🟡 Prioridad 3", "🟢 Prioridad 4", "🟣 Prioridad 5", "⚙️ Mecanizado"
])

with tab1: explorar_y_renderizar_dual("FABRICACIÓN DE ANILLOS.zip", "Fabricación de Anillos", "p1")
with tab2: explorar_y_renderizar_dual("PRIORIDAD 2.zip", "Prioridad 2", "p2")
with tab3: explorar_y_renderizar_dual("PRIORIDAD 3.zip", "Prioridad 3", "p3")
with tab4: explorar_y_renderizar_dual("PRIORIDAD 4.zip", "Prioridad 4", "p4")
with tab5: explorar_y_renderizar_dual("PRIORIDAD 5.zip", "Prioridad 5", "p5")
with tab6: explorar_y_renderizar_dual("SERVICIO DE EMBOCINADO Y MECANIZADO D....zip", "Embocinado y Mecanizado", "p6")
