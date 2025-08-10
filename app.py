# app.py
import math
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

from src.utils import _render_single_card_html
from src.utils import _toggle_fav
from src.data_preprocessing import cargar_datos
from src.recommender_logic import recomendar_motos

# ── Config base ──
st.set_page_config(page_title="MotoFit", page_icon="🏍️", layout="centered")

# ── Estado de sesión ──
if "resultados" not in st.session_state:
    st.session_state.resultados = None
if "pagina" not in st.session_state:
    st.session_state.pagina = 1
if "favs" not in st.session_state:
    st.session_state.favs = set()

# ── Datos ──
@st.cache_data
def get_data():
    return cargar_datos("data/motofit_limpio.csv")

df = get_data()

# ── CSS ──
st.markdown(
    """
<style>
.block-container { max-width: 1080px; padding: 2rem; margin:auto; }
@media (prefers-color-scheme: dark){
  body, .stApp { background-color:#0d1117; color:#f0f2f6; }
  h1 { color:#e6e6e6; text-align:center; font-size:2.2rem; }
  h4 { color:#bcbcbc; text-align:center; margin-top:-8px; }
}
@media (prefers-color-scheme: light){
  h1 { color:#1a1a1a; text-align:center; font-size:2.2rem; }
  h4 { color:#444; text-align:center; margin-top:-8px; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Cabecera ──
st.title("🏍️ MotoFit")
st.markdown(
    "<h4>Una app basada en datos para encontrar tu moto ideal. Explora el dashboard interactivo y guarda tus favoritas con ❤️</h4>",
    unsafe_allow_html=True,
)

# ── Pestañas ──
tab_rec, tab_dash = st.tabs(["🏍 Recomendador", "📊 Dashboard"])


#  TAB: RECOMENDADOR
       
with tab_rec:
    st.subheader("Datos para la recomendación")

    colp1, colp2 = st.columns(2)
    with colp1:
        presupuesto_min = st.slider("💰 Mínimo (€)", 0, 20000, 0, 100)
    with colp2:
        presupuesto_max = st.slider("💰 Máximo (€)", 1000, 50000, 7000, 500)

    if presupuesto_min >= presupuesto_max:
        st.error("El mínimo no puede ser ≥ al máximo.")
        st.stop()

    st.subheader("Cilindrada")
    
    colc1, colc2 = st.columns(2)
    with colc1:
        cc_min = st.slider("Min. CC", 0, 1500, 0, 50)
    with colc2:
        cc_max = st.slider("Max. CC", 50, 2000, 750, 50)

    if cc_min >= cc_max:
        st.error("El mínimo de cilindrada no puede ser ≥ al máximo.")
        st.stop()
    colf1, colf2, colf3 = st.columns(3)

    with colf1:
        carnet = st.selectbox("🎫 Carnet", ["AM", "B", "A1", "A2", "A"])
    with colf2:
        altura = st.slider("📏 Estatura (cm)", 140, 200, 175)
    with colf3:
        marcas = sorted(df["MARCA"].dropna().unique())
        marca_sel = st.selectbox("🏷️ Marca (opcional)", ["Todas"] + marcas)

    tipos = sorted(df["TIPO_SIMPLIFICADO"].dropna().unique())
    tipo_sel = st.multiselect("🛵 Tipo de moto", tipos, default=tipos)

    st.subheader("Orden")
    colo1, colo2 = st.columns(2)
    with colo1:
        ordenar_opts = {
            "Precio": "PRECIO",
            "Potencia": "POTENCIA",
            "Altura asiento": "ALTURA_ASIENTO",
            "Peso": "PESO_VACIO",
        }
        orden_key = st.selectbox("Ordenar por:", list(ordenar_opts.keys()))
        ordenar_por = ordenar_opts[orden_key]
    with colo2:
        asc = st.selectbox("Dirección:", ["Ascendente", "Descendente"]) == "Ascendente"

    st.markdown("---")

    if st.button("🔍 Buscar motos"):
        marca_para = None if marca_sel == "Todas" else [marca_sel]
        st.session_state.resultados = recomendar_motos(
            df,
            presupuesto_max,
            carnet,
            altura,
            precio_min=presupuesto_min,
            marca=marca_para,
            tipos=tipo_sel,
            ordenar_por=ordenar_por,
            ascendente=asc,
            cilindrada_min=cc_min, 
            cilindrada_max=cc_max, 
        )
        st.session_state.pagina = 1

    # --- Función para mostrar tarjetas  ---
    def display_cards_from_df(data_frame_to_display, key_prefix):
        """
        Renderiza las motos en tarjetas con su información y un checkbox de favorito.
        
        Args:
            data_frame_to_display (pd.DataFrame): DataFrame con las motos a mostrar.
            key_prefix (str): Prefijo para las claves de los widgets para evitar colisiones.
        """
        num_col = 3
        for i in range(0, len(data_frame_to_display), num_col):
            cols = st.columns(num_col)
            for j, col in enumerate(cols):
                if i + j < len(data_frame_to_display):
                    with col:
                        row = data_frame_to_display.iloc[i + j]
                        modelo_key = str(row.MODELO)  # clave estable
                        st.markdown(_render_single_card_html(row), unsafe_allow_html=True)

                        checkbox_key = f"{key_prefix}_fav_{i}_{j}_{hash(modelo_key)}"
                        st.checkbox(
                            "Guardar ❤️",
                            value=(modelo_key in st.session_state.favs),
                            key=checkbox_key,
                            on_change=_toggle_fav,
                            args=(modelo_key, checkbox_key),
                        )

    # --- Render de resultados  ---
    if st.session_state.resultados is not None:
        resultados = st.session_state.resultados
        if resultados.empty:
            st.warning("❌ No se encontraron motos con esos filtros.")
        else:
            total = len(resultados)
            por_pagina = 9
            total_paginas = max(1, math.ceil(total / por_pagina))
            
            if 'pagina' not in st.session_state:
                st.session_state.pagina = 1
            st.session_state.pagina = max(1, min(st.session_state.pagina, total_paginas))

            start = (st.session_state.pagina - 1) * por_pagina
            end = start + por_pagina
            st.caption(f"Mostrando {start + 1}–{min(end, total)} de {total} resultados.")
            col1, col2, col3 = st.columns(3)
            if col1.button("⬅️ Anterior", use_container_width=True, disabled=(st.session_state.pagina <= 1)):
                st.session_state.pagina -= 1
                st.rerun()
            col2.markdown(f"<div style='text-align: center; font-size: 1.1em; margin-top: 0.3rem;'>{st.session_state.pagina} / {total_paginas}</div>", unsafe_allow_html=True,)
            if col3.button("Siguiente ➡️", use_container_width=True, disabled=(st.session_state.pagina >= total_paginas)):
                st.session_state.pagina += 1
                st.rerun()
            st.markdown("---")
            subset = resultados.iloc[start:end]
            display_cards_from_df(subset, "main_results")

    # --- Favoritas  ---
    if st.session_state.favs:
        st.markdown("---")
        st.subheader("🗂️ Tus favoritas")
        df_favs = df[df["MODELO"].isin(st.session_state.favs)]
        display_cards_from_df(df_favs, "fav_section")

    st.markdown("---")
    st.caption("Desarrollado por @rofaba")


# TAB: DASHBOARD    

with tab_dash:
    st.subheader("Distribuciones y comparativas")


    # Filtros
    cflt1, cflt2 = st.columns(2)
    tipos_dash = ["Todos"] + sorted(df["TIPO_SIMPLIFICADO"].unique().tolist())
    marcas_dash = ["Todas"] + sorted(df["MARCA"].unique().tolist())
    with cflt1:
        tipo_dash = st.selectbox("Filtrar por tipo", tipos_dash, key="dash_tipo")
    with cflt2:
        marca_dash = st.selectbox("Filtrar por marca", marcas_dash, key="dash_marca")

    df_dash = df.copy()
    if tipo_dash != "Todos":
        df_dash = df_dash[df_dash["TIPO_SIMPLIFICADO"] == tipo_dash]
    if marca_dash != "Todas":
        df_dash = df_dash[df_dash["MARCA"] == marca_dash]

    if df_dash.empty:
        st.info("No hay datos para esos filtros.")
        st.stop()

    # KPIs
    c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
    precio_med = pd.to_numeric(df_dash["PRECIO"], errors="coerce").median()
    altura_med = pd.to_numeric(df_dash["ALTURA_ASIENTO"], errors="coerce").median()
    c_kpi1.metric("Modelos", int(len(df_dash)))
    c_kpi2.metric("Precio mediano", f"€{precio_med:,.0f}" if pd.notna(precio_med) else "—")
    c_kpi3.metric(
        "Altura asiento (mediana)", f"{altura_med:.0f} mm" if pd.notna(altura_med) else "—"
    )

    st.markdown("---")

    # Fila 1
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Altura de asiento por tipo**")
        orden_tipos = [
            "Adventure",
            "Custom",
            "Naked",
            "Off-road",
            "Otro",
            "Scooter",
            "Sport",
            "Tourer",
        ]
        base_altura = df_dash.dropna(
            subset=["ALTURA_ASIENTO", "TIPO_SIMPLIFICADO"]
        ).copy()
        base_altura["ALTURA_ASIENTO"] = pd.to_numeric(
            base_altura["ALTURA_ASIENTO"], errors="coerce"
        )
        base_altura = base_altura.dropna(subset=["ALTURA_ASIENTO"])

        if base_altura.empty:
            st.info("Sin datos de altura con los filtros actuales.")
        else:
            q02 = base_altura["ALTURA_ASIENTO"].quantile(0.02)
            q98 = base_altura["ALTURA_ASIENTO"].quantile(0.98)
            vmin = float(base_altura["ALTURA_ASIENTO"].min())
            vmax = float(base_altura["ALTURA_ASIENTO"].max())
            lo = max(600.0, min(q02 - 20, vmin - 15))
            hi = max(q98 + 20, vmax + 20)  # evita cortar outliers
            y_scale = alt.Scale(domain=[lo, hi])

            box = (
                alt.Chart(base_altura)
                .mark_boxplot(size=28)
                .encode(
                    x=alt.X("TIPO_SIMPLIFICADO:N", sort=orden_tipos, title="Tipo"),
                    y=alt.Y("ALTURA_ASIENTO:Q", scale=y_scale, title="Altura asiento (mm)"),
                    tooltip=["TIPO_SIMPLIFICADO", "ALTURA_ASIENTO"],
                )
            )
            puntos = (
                alt.Chart(base_altura)
                .mark_circle(size=40, opacity=0.25)
                .encode(
                    x=alt.X("TIPO_SIMPLIFICADO:N", sort=orden_tipos, title=None),
                    y=alt.Y("ALTURA_ASIENTO:Q", scale=y_scale),
                    color=alt.Color("TIPO_SIMPLIFICADO:N", legend=None),
                    tooltip=["MARCA", "MODELO", "ALTURA_ASIENTO", "TIPO_SIMPLIFICADO"],
                )
            )
            st.altair_chart((box + puntos).properties(height=360), use_container_width=True)
            st.caption(f"Nota: eje Y auto‑ajustado (~{lo:.0f}–{hi:.0f} mm).")

    with c2:
        st.markdown("**Precio vs Potencia**")
        base_scatter = df_dash[["PRECIO", "POTENCIA", "MARCA", "MODELO", "TIPO_SIMPLIFICADO"]].copy()
        base_scatter["PRECIO"] = pd.to_numeric(base_scatter["PRECIO"], errors="coerce")
        base_scatter["POTENCIA"] = pd.to_numeric(base_scatter["POTENCIA"], errors="coerce")
        base_scatter = base_scatter.dropna(subset=["PRECIO", "POTENCIA"])

        if base_scatter.empty:
            st.info("Sin datos para Precio/Potencia con los filtros actuales.")
        else:
            fig = px.scatter(
                base_scatter,
                x="POTENCIA",
                y="PRECIO",
                color="TIPO_SIMPLIFICADO",
                hover_data=["MARCA", "MODELO"],
            )
            fig.update_yaxes(tickprefix="€", separatethousands=True)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Fila 2
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("**Precio por tipo**")
        base_precio = df_dash.dropna(subset=["PRECIO", "TIPO_SIMPLIFICADO"]).copy()
        base_precio["PRECIO"] = (
            base_precio["PRECIO"]
            .astype(str)
            .str.replace(r"[^\d.,]", "", regex=True)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        base_precio["PRECIO"] = pd.to_numeric(base_precio["PRECIO"], errors="coerce")
        base_precio = base_precio.dropna(subset=["PRECIO"])

        if base_precio.empty:
            st.info("Sin datos de precio para los filtros actuales.")
        else:
            fig_box = px.box(
                base_precio,
                x="TIPO_SIMPLIFICADO",
                y="PRECIO",
                category_orders={"TIPO_SIMPLIFICADO": orden_tipos},
            )
            fig_box.update_yaxes(tickprefix="€", separatethousands=True)
            st.plotly_chart(fig_box, use_container_width=True)

    with c4:
        st.markdown("**Licencias por tipo**")
        base_lic = df_dash.dropna(subset=["CARNET_MINIMO", "TIPO_SIMPLIFICADO"]).copy()
        orden_carnet = ["AM", "B", "A1", "A2", "A"]
        base_lic["CARNET_MINIMO"] = pd.Categorical(
            base_lic["CARNET_MINIMO"], categories=orden_carnet, ordered=True
        )

        if base_lic.empty:
            st.info("Sin datos de licencias con los filtros actuales.")
        else:
            chart_lic = (
                alt.Chart(base_lic)
                .mark_bar()
                .encode(
                    x=alt.X("TIPO_SIMPLIFICADO:N", sort=orden_tipos, title="Tipo"),
                    y=alt.Y("count():Q", stack="normalize", title="Proporción"),
                    color=alt.Color(
                        "CARNET_MINIMO:N",
                        sort=orden_carnet,
                        legend=alt.Legend(title="Carnet"),
                    ),
                    tooltip=[
                        alt.Tooltip("TIPO_SIMPLIFICADO:N", title="Tipo"),
                        alt.Tooltip("CARNET_MINIMO:N", title="Carnet"),
                        alt.Tooltip("count():Q", title="Modelos"),
                    ],
                )
                .properties(height=360)
            )
            st.altair_chart(chart_lic, use_container_width=True)
