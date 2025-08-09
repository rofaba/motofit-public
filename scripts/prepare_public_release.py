# scripts/prepare_public_release.py
from pathlib import Path
import pandas as pd
import re, shutil, os, random

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets" / "logos"
DATA.mkdir(parents=True, exist_ok=True)

# 1) Borrar CSVs por-marca y catálogos completos (ajusta patrones si necesitas)
patrones_borrar = [
    "cf_moto.csv","bmw.csv","honda.csv","harley_davidson.csv","benelli.csv",
    "husqvarna.csv","indian.csv","ducati.csv","aprilia.csv","kawasaki.csv",
    "keeway.csv","kymco.csv","morbidelli.csv","peugeot.csv","suzuki.csv",
    "royal_enfield.csv","moto_guzzi.csv","ktm.csv","piaggio.csv","mitt.csv",
    "motofit_limpio_con_vespa.csv"  # dataset completo
]
for nombre in patrones_borrar:
    p = DATA / nombre
    if p.exists():
        p.unlink()

# 2) Cargar dataset original (ajusta si tu archivo final tiene otro nombre)
ORIG = ROOT / "data" / "motofit_limpio_con_vespa_LOCAL.csv"  # copia local no versionada
if not ORIG.exists():
    raise FileNotFoundError(f"Falta {ORIG}. Pon aquí TU CSV completo (no se sube).")

cols = ["MARCA","MODELO","PRECIO","POTENCIA","ALTURA_ASIENTO","PESO_VACIO",
        "TIPO_SIMPLIFICADO","CARNET_MINIMO"]
df = pd.read_csv(ORIG, usecols=cols)

# 3) Demo balanceado (15–30 filas)
marcas_demo = ["Yamaha","Honda","BMW","Kawasaki","KTM"]
df_demo = (
    df[df["MARCA"].isin(marcas_demo)]
    .groupby(["MARCA","TIPO_SIMPLIFICADO"], group_keys=False)
    .apply(lambda g: g.sample(min(len(g), 3), random_state=42))
    .reset_index(drop=True)
)
df_demo = df_demo.head(25)  # cap a 25

# 4) (Opcional) Anonimizar MODELO levemente
def soft_mask_modelo(x: str) -> str:
    if not isinstance(x, str): return x
    # quita números largos y sufijos comerciales muy específicos
    x = re.sub(r"\b(ABS|SP|PRO|RR|R|S|SE|X|ADV|LTD)\b", "", x, flags=re.I)
    x = re.sub(r"\s+", " ", x).strip()
    return x

df_demo["MODELO"] = df_demo["MODELO"].apply(soft_mask_modelo)

# 5) Guardar demo
OUT = DATA / "motofit_demo.csv"
df_demo.to_csv(OUT, index=False)
print(f"Demo guardado: {OUT} ({len(df_demo)} filas)")

# 6) Limpiar logos inexistentes (opcional: dejar solo los de marcas_demo)
if ASSETS.exists():
    for logo in ASSETS.glob("*.png"):
        brand = logo.stem.replace("_", " ").title()
        if brand not in marcas_demo:
            logo.unlink()
