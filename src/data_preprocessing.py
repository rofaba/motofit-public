# src/data_preprocessing.py
import streamlit as st
import pandas as pd
import io

@st.cache_data
def cargar_datos(path_local="data/motofit_demo.csv"):
    """
    Carga y preprocesa los datos de las motos.
    Prioriza la carga desde Streamlit Secrets (para producción)
    y usa una ruta local como fallback (para desarrollo).
    """
    df = None

    # Intenta cargar el DataFrame desde la URL en Streamlit Secrets (alojado por ahora en Google Drive).
    # Esta es la lógica correcta para el despliegue en la nube.
    url = st.secrets.get("DATA_URL", "").strip() if hasattr(st, "secrets") else ""
    if url:
        try:
            # Lee directamente el CSV desde la URL
            return pd.read_csv(url)
        except Exception as e:
            st.error(f"Error al cargar los datos desde la URL: {e}")
            return pd.DataFrame()

    # Si no hay URL, usa el archivo local de demostración
    # Esta es la lógica para el desarrollo local.
    try:
        df = pd.read_csv(path_local)
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo de datos en {path_local}.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al cargar el archivo de datos local: {e}")
        return pd.DataFrame()

    # --- Preprocesamiento de los datos ---
    
    # 1. Conversión de tipos numéricos
    cols_numericas = ['PRECIO', 'ALTURA_ASIENTO', 'POTENCIA', 'PESO_VACIO', 'CILINDRADA']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 2. Conversión de tipos de texto
    cols_texto = ['CARNET_MINIMO', 'MARCA', 'TIPO_SIMPLIFICADO', 'MODELO']
    for col in cols_texto:
        if col in df.columns:
            df[col] = df[col].astype(str)
            
    # 3. Eliminar filas con valores nulos en columnas esenciales
    columnas_esenciales = ['PRECIO', 'ALTURA_ASIENTO', 'CARNET_MINIMO', 'MARCA', 'TIPO_SIMPLIFICADO', 'CILINDRADA']
    df.dropna(subset=columnas_esenciales, inplace=True)
    
    # 4. Limpiar los índices
    df.reset_index(drop=True, inplace=True)

    return df