import streamlit as st
import os
import base64
from io import BytesIO
from PIL import Image
import pandas as pd

def _logo_base64(path, width=70):

    """
    Convierte una imagen de logo a formato Base64 para embeberla en HTML.

    Esta función lee un archivo de imagen, lo redimensiona, lo codifica en Base64
    y lo retorna como una etiqueta HTML img. Esto permite mostrar las imágenes
    directamente en las tarjetas de la aplicación sin necesidad de rutas de archivo
    relativas, lo cual es útil en entornos de despliegue.

    Args:
        path (str): La ruta del archivo de imagen del logo.
        width (int, opcional): El ancho deseado para la imagen. Por defecto es 70px.

    Returns:
        Optional[str]: Una cadena HTML con la etiqueta <img> o None si ocurre un error.
    """


    if not os.path.exists(path):
        return None
    try:
        img = Image.open(path)
        img.thumbnail((width, width), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"<img src='data:image/png;base64,{b64}' width='{width}' style='margin-bottom:10px;'/>"
    except Exception:
        return None

def _render_single_card_html(row):

    """
    Genera el código HTML para mostrar una tarjeta de moto.

    Esta función crea una tarjeta con los detalles de una moto, incluyendo
    la marca, modelo, precio y otras especificaciones. También gestiona
    la visualización del logo de la marca.

    Args:
        row (pd.Series): Una fila del DataFrame de motos, representando una única moto.
        favs (Set[str]): El conjunto de modelos de motos que el usuario ha marcado como favoritos.

    Returns:
        str: Una cadena de texto con el código HTML de la tarjeta.
    """

    marca_key = str(row.MARCA).lower().replace(" ", "_")
    logo_path = os.path.join("assets", "logos", f"{marca_key}.png")
    logo_tag = _logo_base64(logo_path) or f"<b>{row.MARCA}</b>"

    modelo = row.MODELO
    precio = f"€{int(row.PRECIO):,}" if not pd.isna(row.PRECIO) else "N/A"
    potencia = f"{row.POTENCIA} cv" if not pd.isna(row.POTENCIA) else "N/A"
    altura = f"{row.ALTURA_ASIENTO} mm" if not pd.isna(row.ALTURA_ASIENTO) else "N/A"
    peso = f"{row.PESO_VACIO} kg" if not pd.isna(row.PESO_VACIO) else "N/A"

    return f"""
    <div style="
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.4);
        color: #f0f0f0;
        text-align: center;
        min-height: 280px;
        margin-bottom: 20px;">
        {logo_tag}
        <h4 style='color:#00cc99; margin:10px 0;'>{modelo}</h4>
        <ul style='list-style:none; padding:0; text-align:left; font-size:0.9em;'>
            <li>💰 <b>Precio:</b> {precio}</li>
            <li>🏍️ <b>Potencia:</b> {potencia}</li>
            <li>📏 <b>Altura:</b> {altura}</li>
            <li>⚖️ <b>Peso:</b> {peso}</li>
        </ul>
    </div>
    """

def _toggle_fav(modelo_key, checkbox_key):

    
    """
    Callback para gestionar el estado de los favoritos en `st.session_state`.

    Esta función se ejecuta cada vez que el usuario marca o desmarca una moto
    como favorita. Actualiza el conjunto de favoritos y provoca un `rerun` de
    la aplicación para que los cambios se reflejen inmediatamente.

    Args:
        modelo_key (str): El identificador único de la moto (su modelo).
        checkbox_key (str): La clave única del widget checkbox en la sesión.
    """

    checked = st.session_state.get(checkbox_key, False)
    if checked:
        st.session_state.favs.add(modelo_key)
    else:
        st.session_state.favs.discard(modelo_key)

    # Rerender inmediatamente tras el cambio, se implementaron las dos opciones para evitar la caída de la app por incompatibilidad.
    if hasattr(st, "rerun"):
        st.rerun()  # versiones nuevas
    else:
        st.experimental_rerun()  # compatibilidad con versiones antiguas

