# src/recommender_logic.py
import pandas as pd

def recomendar_motos(
    df,
    presupuesto_max,
    carnet,
    altura,
    precio_min=0,
    marca=None,
    tipos=None,
    ordenar_por='PRECIO',
    ascendente=True,
    cilindrada_min=0,
    cilindrada_max=2000,
):
    df_filtrado = df.copy()

    # --- Convertir tipos de datos y manejar N/A una sola vez al inicio ---
    df_filtrado["CILINDRADA"] = pd.to_numeric(df_filtrado["CILINDRADA"], errors="coerce")
    df_filtrado["PRECIO"] = pd.to_numeric(df_filtrado["PRECIO"], errors="coerce")
    df_filtrado["ALTURA_ASIENTO"] = pd.to_numeric(df_filtrado["ALTURA_ASIENTO"], errors="coerce")
    
    # --- Aplicar todos los filtros en secuencia sobre el mismo DataFrame ---
    
    # 1. Filtro de Precio
    df_filtrado = df_filtrado[
        (df_filtrado['PRECIO'] <= presupuesto_max) &
        (df_filtrado['PRECIO'] >= precio_min)
    ]
    
    # 2. Filtro de Cilindrada
    df_filtrado = df_filtrado[
        (df_filtrado["CILINDRADA"] >= cilindrada_min) &
        (df_filtrado["CILINDRADA"] <= cilindrada_max)
    ]

    # 3. Filtro de Carnet
    carnet_orden = {'AM': 0, 'B': 1, 'A1': 1, 'A2': 2, 'A': 3}
    carnet_usuario = carnet_orden.get(str(carnet).upper())
    
    if carnet_usuario is None:
        return pd.DataFrame()

    df_filtrado = df_filtrado[
        df_filtrado['CARNET_MINIMO'].map(carnet_orden) <= carnet_usuario
    ]
    
    # 4. Filtro de Altura (regla simple + buffer)
    altura_max_calculada = (altura * 0.46 - 3) * 10  # mm
    BUFFER_ALTURA_MM = 80
    df_filtrado = df_filtrado[
        df_filtrado['ALTURA_ASIENTO'] <= altura_max_calculada + BUFFER_ALTURA_MM
    ]

    # 5. Filtro de Marca (si se seleccionó)
    if marca and marca != ["Todas"]:
        df_filtrado = df_filtrado[df_filtrado['MARCA'].isin(marca)]
        
    # 6. Filtro de Tipo (si se seleccionó)
    if tipos:
        df_filtrado = df_filtrado[df_filtrado['TIPO_SIMPLIFICADO'].isin(tipos)]
    
    # --- Preparar y ordenar el resultado ---
    
    # Eliminar filas con N/A de las columnas clave para una ordenación limpia
    df_filtrado = df_filtrado.dropna(subset=[ordenar_por])
    
    # Ordenar
    df_resultado = df_filtrado.sort_values(by=ordenar_por, ascending=ascendente)

    # Columnas a mostrar
    columnas_a_mostrar = [
        'MARCA', 'MODELO', 'TIPO_SIMPLIFICADO',
        'PRECIO', 'ALTURA_ASIENTO', 'POTENCIA', 'PESO_VACIO'
    ]
    columnas_existentes = [c for c in columnas_a_mostrar if c in df_resultado.columns]

    return df_resultado[columnas_existentes].reset_index(drop=True)