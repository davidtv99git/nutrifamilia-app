import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="NutriFamilia WebApp", page_icon="🥗", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0f0f13; color: #f1f5f9; font-family: sans-serif; }
    .recipe-card { background: #18181f; border-radius: 12px; padding: 14px; border: 1px solid #272732; margin-bottom: 12px; }
    .profile-card { background: #18181f; border-radius: 12px; padding: 16px; text-align: center; border: 1px solid #272732; }
    .avatar-img { width: 80px; height: 80px; border-radius: 50%; border: 3px solid #10b981; }
    .macro-pill { background: #22222d; padding: 4px 8px; border-radius: 6px; font-weight: 600; font-size: 0.8rem; margin-right: 4px; }
</style>
""", unsafe_allow_html=True)

# FAMILY DATA
if "family_data" not in st.session_state:
    st.session_state.family_data = {
        "David": {"rol": "Padre", "edad": 52, "peso": 83.5, "altura": 178, "meta": "Recomposición Corporal", "kcal": 1925, "prot": 150.3, "gras": 50.1, "hc": 218.2, "agua": 2.9, "historial_peso": [85.0, 84.5, 84.0, 83.5]},
        "Ruth": {"rol": "Madre", "edad": 51, "peso": 80.0, "altura": 165, "meta": "Recomposición Corporal", "kcal": 1500, "prot": 144.0, "gras": 48.0, "hc": 123.0, "agua": 2.8, "historial_peso": [81.5, 81.0, 80.5, 80.0]},
        "Marcos": {"rol": "Hijo (16a)", "edad": 16, "peso": 50.0, "altura": 172, "meta": "Masa Muscular", "kcal": 2350, "prot": 90.0, "gras": 30.0, "hc": 430.0, "agua": 1.8, "historial_peso": [48.0, 49.0, 49.5, 50.0]},
        "Pablo": {"rol": "Hijo (13a)", "edad": 13, "peso": 40.0, "altura": 158, "meta": "Masa Muscular / Baloncesto", "kcal": 2150, "prot": 72.0, "gras": 24.0, "hc": 411.5, "agua": 1.4, "historial_peso": [38.5, 39.0, 39.5, 40.0]}
    }

# RECIPES DATABASE
if "recipes_db" not in st.session_state:
    st.session_state.recipes_db = [
        {"id": 1, "nombre": "Paella Valenciana Tradicional de Pollo y Judías", "categoria": "Comidas", "tipo": "Tradicional Familiar", "origen": "Cocina Tradicional", "equipamiento": "Plancha / Paellera", "tiempo": 40, "dificultad": "Media", "kcal": 540, "prot": 38, "gras": 14, "hc": 65, "ingredientes": "Arroz bomba 80g, Pechuga/Muslo de pollo 180g, Judía verde 80g, Garrofón 30g, Tomate 50g, Azafrán, AOVE 10g", "pasos": "1. Sofreír el pollo sazonado con AOVE. 2. Añadir judías y tomate. 3. Añadir agua, azafrán y arroz. Cocer 18 min."},
        {"id": 2, "nombre": "Crema Proteica de Calabacín con Pechuga al Varoma", "categoria": "Comidas", "tipo": "Saludable / Fit", "origen": "Lara Ibarra (YouTube)", "equipamiento": "Thermomix (Varoma)", "tiempo": 25, "dificultad": "Fácil", "kcal": 420, "prot": 45, "gras": 12, "hc": 32, "ingredientes": "Calabacín 300g, Queso fresco batido 0% 100g, Pechuga de pollo 180g, Cebolla 50g, AOVE 8g", "pasos": "1. Cocinar calabacín y cebolla en TMX. 2. Pollo en Varoma arriba. 3. Triturar crema con queso batido y servir."},
        {"id": 3, "nombre": "Kebab Skewers Fit de Pollo y Especias", "categoria": "Comidas", "tipo": "Saludable / Fit", "origen": "Miguelnaarfit (YouTube)", "equipamiento": "AirFryer", "tiempo": 18, "dificultad": "Muy Fácil", "kcal": 440, "prot": 42, "gras": 11, "hc": 35, "ingredientes": "Pechuga de pollo 180g, Especias kebab, Cebolla 50g, Tortilla trigo integral 1ud", "pasos": "1. Macerar pollo con especias. 2. Ensartar en brochetas. 3. Cocinar en AirFryer 14 min a 190°C."},
        {"id": 4, "nombre": "Lentejas Pardinas Estofadas con Verduras", "categoria": "Comidas", "tipo": "Tradicional / Saludable", "origen": "Mattyzandolo (YouTube)", "equipamiento": "Thermomix (Varoma)", "tiempo": 35, "dificultad": "Fácil", "kcal": 480, "prot": 32, "gras": 9, "hc": 68, "ingredientes": "Lentejas 80g, Zanahoria 60g, Pimiento 50g, Patata 80g, Laurel, Pimentón, AOVE 8g", "pasos": "1. Trocear verduras en TMX. 2. Sofreír con AOVE. 3. Añadir lentejas, patata y cocer 30 min."},
        {"id": 5, "nombre": "Porridge Tiramisú Proteico de Avena y Café", "categoria": "Desayunos", "tipo": "Saludable / Fit", "origen": "Lara Ibarra (YouTube)", "equipamiento": "Microondas", "tiempo": 8, "dificultad": "Fácil", "kcal": 380, "prot": 28, "gras": 7, "hc": 52, "ingredientes": "Avena 60g, Leche 200ml, Café 50ml, Proteína Whey 20g, Cacao 5g", "pasos": "1. Mezclar avena, leche y café. Calentar 2 min. 2. Añadir proteína y cacao."},
        {"id": 6, "nombre": "Salmón al Horno con Patatas Panadera", "categoria": "Cenas", "tipo": "Tradicional / Saludable", "origen": "Cocina Tradicional", "equipamiento": "Horno", "tiempo": 25, "dificultad": "Fácil", "kcal": 510, "prot": 41, "gras": 22, "hc": 36, "ingredientes": "Salmón 180g, Patata 180g, Cebolla 50g, Limón, Eneldo, AOVE 8g", "pasos": "1. Hornear patatas 15 min a 200°C. 2. Colocar salmón encima y hornear 12 min más."},
        {"id": 7, "nombre": "Bacalao sobre Pisto de Verduras al Varoma", "categoria": "Cenas", "tipo": "Saludable / Fit", "origen": "Mattyzandolo (YouTube)", "equipamiento": "Thermomix (Varoma)", "tiempo": 30, "dificultad": "Fácil", "kcal": 390, "prot": 38, "gras": 10, "hc": 28, "ingredientes": "Bacalao 180g, Pimientos 150g, Tomate 150g, Cebolla 80g, AOVE 10g", "pasos": "1. Sofreír verduras en TMX. 2. Bacalao en Varoma arriba 25 min."},
        {"id": 8, "nombre": "Tortilla Española Ligera en AirFryer", "categoria": "Cenas", "tipo": "Tradicional / Saludable", "origen": "Miguelnaarfit (YouTube)", "equipamiento": "AirFryer", "tiempo": 22, "dificultad": "Fácil", "kcal": 360, "prot": 22, "gras": 14, "hc": 36, "ingredientes": "Patata 200g, Cebolla 60g, 3 huevos M, AOVE spray 5g", "pasos": "1. Cocinar patata y cebolla en AirFryer 15 min. 2. Mezclar con huevo y cuajar en sartén o AirFryer."},
        {"id": 9, "nombre": "Albóndigas de Pavo Magro en Salsa de Almendras", "categoria": "Comidas", "tipo": "Tradicional / Saludable", "origen": "Cocina Tradicional", "equipamiento": "Thermomix", "tiempo": 30, "dificultad": "Media", "kcal": 490, "prot": 44, "gras": 18, "hc": 26, "ingredientes": "Pavo picado 180g, Almendras 20g, Cebolla 60g, Ajo, Vino 30ml, Caldo 150ml, AOVE 10g", "pasos": "1. Dorar albóndigas en AirFryer. 2. Sofreír salsa en TMX, triturar y cocer albóndigas 10 min."},
        {"id": 10, "nombre": "Cheesecake Fit Proteico de Vainilla", "categoria": "Snacks", "tipo": "Saludable / Fit", "origen": "Miguelnaarfit (YouTube)", "equipamiento": "Microondas", "tiempo": 6, "dificultad": "Muy Fácil", "kcal": 260, "prot": 26, "gras": 4, "hc": 28, "ingredientes": "Queso batido 200g, 1 huevo M, Vainilla, Edulcorante, Frutos rojos 60g, Maizena 10g", "pasos": "1. Batir ingredientes. 2. Microondas 3 min. 3. Servir con frutos rojos."}
    ]

# PLANNER STATE
if "weekly_plan" not in st.session_state:
    st.session_state.weekly_plan = {
        "Lunes": {"Desayuno": 5, "Comida": 1, "Cena": 7, "Snack": 10, "comensales": 4},
        "Martes": {"Desayuno": 5, "Comida": 2, "Cena": 8, "Snack": 10, "comensales": 4},
        "Miércoles": {"Desayuno": 5, "Comida": 4, "Cena": 6, "Snack": 10, "comensales": 4},
        "Jueves": {"Desayuno": 5, "Comida": 3, "Cena": 8, "Snack": 10, "comensales": 4},
        "Viernes": {"Desayuno": 5, "Comida": 9, "Cena": 7, "Snack": 10, "comensales": 4},
        "Sábado": {"Desayuno": 5, "Comida": 1, "Cena": 6, "Snack": 10, "comensales": 4},
        "Domingo": {"Desayuno": 5, "Comida": 4, "Cena": 8, "Snack": 10, "comensales": 4}
    }

if "active_recipe" not in st.session_state:
    st.session_state.active_recipe = None

# SIDEBAR
st.sidebar.title("🥗 NutriFamilia App")
st.sidebar.caption("iPad Edition • David • Ruth • Marcos • Pablo")
nav = st.sidebar.radio("Navegación:", ["🍿 Biblioteca & Carrusel Netflix", "👨‍👩‍👧‍👦 Dashboard & Perfiles", "📅 Planificador Semanal", "🛒 Lista de la Compra", "🤖 Importador IA YouTube"])

def get_recipe(rid):
    for r in st.session_state.recipes_db:
        if r["id"] == rid: return r
    return st.session_state.recipes_db[0]

if nav == "🍿 Biblioteca & Carrusel Netflix":
    st.title("🍿 Galería & Carrusel Netflix")
    st.caption("Pinchando en cualquier tarjeta se abre la ficha completa con porciones y preparación.")
    c1, c2 = st.columns([1, 1])
    with c1: comensales = st.radio("👥 Comensales:", ["1 Persona", "2 Personas", "4 Personas (Familia)"], index=2, horizontal=True)
    mult = 1.0 if "1" in comensales else (2.0 if "2" in comensales else 4.0)
    with c2: equip = st.selectbox("⚙️ Equipamiento:", ["Todos", "Thermomix (Varoma)", "AirFryer", "Plancha / Paellera", "Horno", "Microondas"])
    
    if st.session_state.active_recipe is not None:
        ar = get_recipe(st.session_state.active_recipe)
        st.markdown("---")
        st.markdown(f"## 🍽️ {ar["nombre"]}")
        st.write(f"**Origen:** {ar["origen"]} | **Equipamiento:** {ar["equipamiento"]} | **Tiempo:** {ar["tiempo"]} min")
        st.success(f"📊 Totales ({mult:.0f} p.): {int(ar["kcal"]*mult)} kcal | 🍗 Prot: {int(ar["prot"]*mult)}g | 🥑 Gras: {int(ar["gras"]*mult)}g | 🍚 HC: {int(ar["hc"]*mult)}g")
        st.markdown("### 🛒 Ingredientes:")
        st.info(ar["ingredientes"])
        st.markdown("### 👩‍🍳 Preparación:")
        st.write(ar["pasos"])
        if st.button("❌ Cerrar Ficha"): st.session_state.active_recipe = None
        st.markdown("---")
    
    f_db = st.session_state.recipes_db
    if equip != "Todos": f_db = [r for r in f_db if equip in r["equipamiento"]]
    
    st.markdown("### 🔥 Recetas Destacadas")
    cols = st.columns(3)
    for idx, r in enumerate(f_db[:3]):
        with cols[idx % 3]:
            st.markdown(f"### 🥘 {r["nombre"]}")
            st.caption(f"{r["equipamiento"]} • {r["origen"]}")
            st.write(f"🔥 {int(r["kcal"]*mult)} kcal | 🍗 {int(r["prot"]*mult)}g P | 🥑 {int(r["gras"]*mult)}g G | 🍚 {int(r["hc"]*mult)}g HC")
            if st.button(f"👁️ Ver Ficha", key=f"f1_{r["id"]}"): st.session_state.active_recipe = r["id"]
    
    st.markdown("### 🥘 Platos Tradicionales Familiares (No Repetitivos)")
    cols2 = st.columns(3)
    trad = [r for r in f_db if "Tradicional" in r["tipo"]]
    for idx, r in enumerate(trad[:3]):
        with cols2[idx % 3]:
            st.markdown(f"### 🍲 {r["nombre"]}")
            st.caption(f"{r["equipamiento"]} • {r["origen"]}")
            st.write(f"🔥 {int(r["kcal"]*mult)} kcal | 🍗 {int(r["prot"]*mult)}g P | 🥑 {int(r["gras"]*mult)}g G | 🍚 {int(r["hc"]*mult)}g HC")
            if st.button(f"👁️ Ver Ficha", key=f"f2_{r["id"]}"): st.session_state.active_recipe = r["id"]
elif nav == "👨‍👩‍👧‍👦 Dashboard & Perfiles":
    st.title("👨‍👩‍👧‍👦 Perfiles & Fichas de Seguimiento")
    pcols = st.columns(4)
    for idx, (name, pdata) in enumerate(st.session_state.family_data.items()):
        with pcols[idx]:
            st.markdown(f"### 👤 {name}")
            st.caption(f"{pdata["rol"]} ({pdata["edad"]}a)")
            st.write(f"🔥 **{pdata["kcal"]} kcal/día**")
            st.write(f"🍗 Prot: {pdata["prot"]}g | 🥑 Gras: {pdata["gras"]}g")
            st.write(f"🍚 HC: {pdata["hc"]}g | 💧 Agua: {pdata["agua"]}L")
    
    st.markdown("---")
    st.markdown("### 📈 Ficha de Seguimiento Corporal")
    sm = st.selectbox("Familiar:", ["David", "Ruth", "Marcos", "Pablo"])
    pd_m = st.session_state.family_data[sm]
    c_a, c_b = st.columns([1, 1])
    with c_a:
        imc = pd_m["peso"] / ((pd_m["altura"]/100)**2)
        st.metric("Peso Actual", f"{pd_m["peso"]} kg", delta=f"IMC: {imc:.1f}")
        st.info(f"Meta: {pd_m["meta"]}")
        with st.form(f"form_{sm}"):
            nw = st.number_input("Registrar Peso (kg):", value=float(pd_m["peso"]), step=0.2)
            nh = st.number_input("Altura (cm):", value=int(pd_m["altura"]), step=1)
            if st.form_submit_button("💾 Guardar Ficha"):
                st.session_state.family_data[sm]["peso"] = nw
                st.session_state.family_data[sm]["altura"] = nh
                st.session_state.family_data[sm]["historial_peso"].append(nw)
                st.success("Guardado correctamente.")
    with c_b:
        st.markdown(f"#### 📉 Evolución de Peso - {sm}")
        st.line_chart(pd.DataFrame({"Semana": [f"Sem {i+1}" for i in range(len(pd_m["historial_peso"]))], "Peso": pd_m["historial_peso"]}), x="Semana", y="Peso")
elif nav == "📅 Planificador Semanal":
    st.title("📅 Planificador Semanal (Lunes a Domingo)")
    ropts = {r["id"]: f"{r["nombre"]} ({r["equipamiento"]})" for r in st.session_state.recipes_db}
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    sd = st.selectbox("Selecciona Día:", days)
    dp = st.session_state.weekly_plan[sd]
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown(f"### Ajustar Menú del {sd}")
        s_d = st.selectbox("Desayuno:", list(ropts.keys()), format_func=lambda x: ropts[x], index=list(ropts.keys()).index(dp["Desayuno"]))
        s_c = st.selectbox("Comida:", list(ropts.keys()), format_func=lambda x: ropts[x], index=list(ropts.keys()).index(dp["Comida"]))
        s_ce = st.selectbox("Cena:", list(ropts.keys()), format_func=lambda x: ropts[x], index=list(ropts.keys()).index(dp["Cena"]))
        s_s = st.selectbox("Snack:", list(ropts.keys()), format_func=lambda x: ropts[x], index=list(ropts.keys()).index(dp["Snack"]))
        nc = st.slider("Comensales:", 1, 4, dp["comensales"])
        if st.button("💾 Guardar Día"):
            st.session_state.weekly_plan[sd] = {"Desayuno": s_d, "Comida": s_c, "Cena": s_ce, "Snack": s_s, "comensales": nc}
            st.success("Menú del día guardado.")
    with col_b:
        st.markdown("### Resumen de la Semana")
        st.dataframe(pd.DataFrame([{"Día": d, "Desayuno": get_recipe(st.session_state.weekly_plan[d]["Desayuno"])["nombre"], "Comida": get_recipe(st.session_state.weekly_plan[d]["Comida"])["nombre"], "Cena": get_recipe(st.session_state.weekly_plan[d]["Cena"])["nombre"], "Comensales": st.session_state.weekly_plan[d]["comensales"]} for d in days]), use_container_width=True)
elif nav == "🛒 Lista de la Compra":
    st.title("🛒 Lista de la Compra Semanal Calculada")
    slist = {"Carnes/Pescados": {}, "Huevos/Lácteos": {}, "Verduras/Granos": {}}
    for d, dp in st.session_state.weekly_plan.items():
        np = dp["comensales"]
        for mt in ["Desayuno", "Comida", "Cena", "Snack"]:
            r = get_recipe(dp[mt])
            txt = r["ingredientes"]
            if "Pollo" in txt or "Pavo" in txt or "Ternera" in txt or "Salmón" in txt or "Bacalao" in txt:
                slist["Carnes/Pescados"]["Proteína Magra (Pollo/Pavo/Salmón/Bacalao)"] = slist["Carnes/Pescados"].get("Proteína Magra (Pollo/Pavo/Salmón/Bacalao)", 0) + (180*np)
            if "huevo" in txt.lower() or "Queso" in txt:
                slist["Huevos/Lácteos"]["Huevos / Lácteos Proteicos"] = slist["Huevos/Lácteos"].get("Huevos / Lácteos Proteicos", 0) + (2*np)
            if "Calabacín" in txt or "Patata" in txt or "Arroz" in txt or "Avena" in txt:
                slist["Verduras/Granos"]["Verduras y Granos Variados"] = slist["Verduras/Granos"].get("Verduras y Granos Variados", 0) + (200*np)
    ca, cb = st.columns([1, 1])
    with ca:
        st.markdown("### 🥩 Carnes y Pescados")
        for k, v in slist["Carnes/Pescados"].items(): st.checkbox(f"{k}: ~{v/1000:.2f} kg")
        st.markdown("### 🍳 Huevos y Lácteos")
        for k, v in slist["Huevos/Lácteos"].items(): st.checkbox(f"{k}: ~{v} unidades/raciones")
    with cb:
        st.markdown("### 🥦 Verduras y Despensa")
        for k, v in slist["Verduras/Granos"].items(): st.checkbox(f"{k}: ~{v/1000:.2f} kg")
elif nav == "🤖 Importador IA YouTube":
    st.title("🤖 Importador IA de YouTube")
    yurl = st.text_input("Enlace de YouTube:")
    if st.button("🚀 Procesar Vídeo"):
        if yurl:
            nid = len(st.session_state.recipes_db) + 1
            nrec = {"id": nid, "nombre": f"Receta Importada #{nid}", "categoria": "Comidas", "tipo": "Fit", "origen": "YouTube", "equipamiento": "Thermomix / AirFryer", "tiempo": 20, "dificultad": "Fácil", "kcal": 450, "prot": 40, "gras": 12, "hc": 45, "ingredientes": "Pollo 180g, Verduras 200g, AOVE 10g", "pasos": "1. Procesado automático por IA. 2. Cocinar 15 min en AirFryer."}
            st.session_state.recipes_db.append(nrec)
            st.success("¡Receta añadida a la biblioteca!")
            st.json(nrec)
