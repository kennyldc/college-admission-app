# College Admission — Simulación interactiva

App web interactiva para explorar **fairness y admisión universitaria** en un modelo simplificado con dos grupos (advantaged / disadvantaged) y características probabilísticas.

---

## De dónde sale este proyecto

Este repositorio es parte del trabajo del **Proyecto 1** de la materia **DCDS 8991 — Computational and Data Sciences Research Exploration**, Washington University in St. Louis. La app ilustra conceptos de equidad en algoritmos de decisión (admisión) mediante una simulación visual.

---

## Qué hace la app

- **Dos grupos:** Grupo A (advantaged) y Grupo D (disadvantaged), con distintas probabilidades base de tener ciertas características (x₁, x₂).
- **Regla de decisión:** Se usa una regla simple (por ejemplo f = x₁ ∧ x₂) para simular “admisión”.
- **Visualización:** Secciones con transiciones tipo scroll (estilo Apple), círculo con iconos por grupo, grid de personas, controles de velocidad y botón de replay.
- **Probabilidades:** Se muestran P(x₁=1), P(x₂=1) y P(f=1) por grupo para ver cómo la disparidad en recursos se traduce en disparidad en resultados.

La idea es ver de forma intuitiva cómo **desigualdad en las probabilidades de las características** puede llevar a **desigualdad en la tasa de admisión** entre grupos, incluso con la misma regla “ciega” a la raza/grupo.

---

## Cómo ejecutarla en tu máquina

### Requisitos

- Python 3.9+
- Dependencias en `requirements.txt`

### Pasos

1. **Clonar el repo** (o descargar y descomprimir):

   ```bash
   git clone <url-del-repo>
   cd college-admission-app
   ```

2. **Crear entorno virtual (recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Lanzar la app:**

   ```bash
   streamlit run app.py
   ```

   Se abrirá en el navegador (por defecto `http://localhost:8501`).

---

## Requisitos (requirements.txt)

- `numpy`
- `pandas`
- `streamlit`
- `plotly`

---

## Desplegar en la nube (Streamlit Community Cloud)

1. Haz fork o sube este repo a tu cuenta de GitHub.
2. Entra en [share.streamlit.io](https://share.streamlit.io), inicia sesión con GitHub.
3. “New app” → elige este repositorio.
4. **Main file path:** `app.py`
5. Deploy. Obtendrás una URL pública para compartir con quien quieras.

---

## Licencia y uso

Proyecto educativo para DCDS 8991. Si reutilizas o adaptas el código, cita el curso y el proyecto.
