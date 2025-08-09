# 🏍️ MotoFit – Buscador y Recomendador de Motos

**MotoFit** es una aplicación interactiva desarrollada en **Python + Streamlit** que permite filtrar, explorar y guardar motos favoritas según presupuesto, altura, licencia y tipo. Incluye un panel **Dashboard** con visualizaciones dinámicas para analizar el mercado de motos.

![MotoFit Demo](assets/demo_screenshot.png) <!-- CAPTURAS -->

---

## 📌 Características principales

- **Filtrado avanzado** por:
  - Presupuesto mínimo y máximo
  - Tipo de licencia (AM, B, A1, A2, A)
  - Altura del asiento
  - Marca y tipo de moto
  - Orden ascendente o descendente por precio, potencia, altura o peso
- **Sistema de favoritos** persistente durante la sesión
- **Visualización en tarjetas** con datos clave y logos de cada marca
- **Dashboard interactivo** con:
  - Distribución de alturas por tipo de moto
  - Relación precio-potencia
  - Distribución de precios por tipo
  - Proporción de licencias requeridas por tipo de moto
- **Modo claro y oscuro** automático según preferencias del usuario
- Preparado para funcionar con **dataset local** o desde **URL privada en Streamlit Cloud**

---

## 📂 Estructura del proyecto

```bash
MotoFit/
│
├── app.py                     # Aplicación principal Streamlit
├── requirements.txt           # Dependencias del proyecto
├── LICENSE.md                 # Licencia CC BY-NC 4.0
├── README.md                  # Este archivo
│
├── data/
│   ├── motofit_demo.csv        # Dataset reducido de ejemplo (uso en GitHub)
│   └── motofit_limpio.csv      # Dataset completo (NO incluir en repositorio público)
│
├── assets/
│   └── logos/                  # Logos PNG de las marcas
│
└── src/
    ├── utils.py                # Funciones auxiliares (tarjetas, favoritos, logos)
    ├── data_preprocessing.py   # Carga y limpieza de datos
    └── recommender_logic.py    # Lógica de filtrado/recomendación

## Instalación y uso local.
# 1. Clonar el repositorio

git clone https://github.com/usuario/motofit.git
cd motofit

# 2. Crear un entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# 3. Ejecutar la app
streamlit run app.py

# 4. Abrir el navegador
http://localhost:8501



📊 Dataset
El dataset incluye información de cada moto:

Marca

Modelo

Tipo simplificado (Adventure, Naked, Sport, etc.)

Potencia (cv)

Precio (€)

Altura del asiento (mm)

Peso en vacío (kg)

Licencia mínima requerida

⚠️ Importante: El dataset completo es privado y no se incluye en este repositorio.
Solo se publica una versión reducida (motofit_demo.csv) para fines de demostración.

🧪 Testing
El proyecto incluye un breve documento de testing manual que valida:

Carga de datos desde CSV local y remoto

Filtrado correcto por cada criterio

Ordenamiento ascendente y descendente

Funcionamiento del sistema de favoritos

Renderizado correcto de las tarjetas y logos

Comportamiento esperado de las visualizaciones del Dashboard

🛠 Tecnologías utilizadas
Python 3.10+

Streamlit

Pandas

Altair (visualizaciones)

Plotly Express (visualizaciones interactivas)

Pillow (procesamiento de imágenes)

Base64 (logos embebidos en HTML)

📄 Licencia
Este proyecto está bajo la Licencia Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
No se permite su uso con fines comerciales. Más información en el archivo LICENSE.md.

👤 Autor
Desarrollado por Rodrigo Faba
📍 Málaga, España
💼 LinkedIn | 🐙 GitHub

💡 Ideas futuras
Añadir pseudo-recomendador con mensajes personalizados según filtros (sin ML real)

Mejorar compatibilidad móvil

Soporte multi-idioma

Integración de modelos de Machine Learning para recomendaciones inteligentes