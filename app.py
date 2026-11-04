import streamlit as st
import os

# Configuración de la pestaña del navegador
st.set_page_config(
    page_title="Panel de Prioridades",
    page_icon="📌",
    layout="wide"
)

# Estilos visuales con colores corporativos profesionales
st.markdown("""
    <style>
    .main-title { color: #0F4C81; font-family: sans-serif; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #555555; text-align: center; font-size: 1.1rem; margin-bottom: 30px; }
    .prioridad-box { padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 6px solid; background-color: #ffffff; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    
    .b1 { border-left-color: #E74C3C; } .b2 { border-left-color: #E67E22; } .b3 { border-left-color: #F1C40F; } 
    .b4 { border-left-color: #2ECC71; } .b5 { border-left-color: #9B59B6; } .b6 { border-left-color: #34495E; }
    
    .titulo-p { font-weight: bold; font-size: 1.3rem; margin: 0 0 5px 0; }
    .t1 { color: #c0392b; } .t2 { color: #d35400; } .t3 { color: #f39c12; } 
    .t4 { color: #27ae60; } .t5 { color: #8e44ad; } .t6 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📌 Panel Interactivo de Documentos</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Haz clic en los botones para descargar los paquetes de archivos directamente a tu computadora</p>', unsafe_allow_html=True)

# Crear 6 bloques ordenados
def crear_bloque_descarga(nombre_archivo, titulo, descripcion, estilo_c, estilo_t, llave):
    st.markdown(f"""
        <div class="prioridad-box {estilo_c}">
            <p class="titulo-p {estilo_t}">{titulo}</p>
            <p style="color:#7F8C8D; margin-bottom: 10px;">{descripcion}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Comprobar si el archivo ZIP existe en el repositorio y habilitar su descarga
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rb") as f:
            bytes_archivo = f.read()
        st.download_button(
            label=f"📥 Descargar {nombre_archivo}",
            data=bytes_archivo,
            file_name=nombre_archivo,
            mime="application/zip",
            key=llave
        )
    else:
        st.error(f"El archivo {nombre_archivo} no se encuentra en el servidor.")

# Renderizar los 6 bloques en la página web
crear_bloque_descarga("FABRICACIÓN DE ANILLOS.zip", "Fabricación de Anillos", "Planos, guías y especificaciones técnicas para la fabricación.", "b1", "t1", "btn1")
crear_bloque_descarga("PRIORIDAD 2.zip", "Prioridad 2", "Documentos operativos e informes asignados a la prioridad 2.", "b2", "t2", "btn2")
crear_bloque_descarga("PRIORIDAD 3.zip", "Prioridad 3", "Formatos y registros técnicos del área para la prioridad 3.", "b3", "t3", "btn3")
crear_bloque_descarga("PRIORIDAD 4.zip", "Prioridad 4", "Bases de datos y controles diarios de la prioridad 4.", "b4", "t4", "btn4")
crear_bloque_descarga("PRIORIDAD 5.zip", "Prioridad 5", "Documentación histórica y archivos generales de soporte.", "b5", "t5", "btn5")
crear_bloque_descarga("SERVICIO DE EMBOCINADO Y MECANIZADO D....zip", "Embocinado y Mecanizado", "Planillas y seguimientos del servicio de embocinado mecánico.", "b6", "t6", "btn6")
