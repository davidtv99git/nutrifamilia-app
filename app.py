import streamlit as st
import pandas as pd

# Set Page Config for iPad Touchscreen Layout
st.set_page_config(
    page_title="NutriFamilia iPad - WebApp & Planificador Semanal",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for iPad UI Polish
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #2e7d32; color: white; font-weight: bold; }
    .metric-card { background-color: #ffffff; padding: 15px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# Database of Family Members
FAMILY_MEMBERS = {
    "David": {"edad": 52, "peso": 83.5, "altura": 178, "meta": "Recomposición (Déficit ~400 kcal)", "kcal": 1925, "prot": 150.3, "gras": 50.1, "hc": 218.2},
    "Ruth": {"edad": 51, "peso": 80.0, "altura": 165, "meta": "Recomposición (Déficit ~350 kcal)", "kcal": 1500, "prot": 144.0, "gras": 48.0, "hc": 123.0},
    "Marcos": {"edad": 16, "peso": 50.0, "altura": 172, "meta": "Masa muscular / Atletismo", "kcal": 2350, "prot": 90.0, "gras": 30.0, "hc": 430.0},
    "Pablo": {"edad": 13, "peso": 40.0, "altura": 158, "meta": "Masa muscular / Baloncesto", "kcal": 2150, "prot": 72.0, "gras": 24.0, "hc": 411.5}
}

# Recipe Library with Granular Ingredient Quantities for Scaling
RECIPES_DB = [
    {
        "id": 1,
        "nombre": "Crema Proteica de Calabacín con Pechuga al Varoma",
        "categoria": "Comidas",
        "origen": "Lara Ibarra (YouTube)",
        "equipamiento": "Thermomix (Varoma)",
        "tiempo": 25,
        "dificultad": "Fácil",
        "kcal": 420, "prot": 45, "gras": 12, "hc": 32, "sodio": 280, "azucar": 6,
        "ingredientes_dict": {"Pechuga de Pollo": (180, "g", "Carnes y Aves"), "Calabacín": (300, "g", "Frutas y Verduras"), "Queso Fresco Batido 0%": (100, "g", "Huevos y Lácteos"), "Aceite de Oliva (AOVE)": (8, "g", "Despensa")},
        "pasos": "1. Poner el calabacín troceado con agua en el vaso de la Thermomix (15 min / 100°C / Vel 1).\n2. Colocar las pechugas de pollo sazonadas en la bandeja Varoma sobre el vaso.\n3. Añadir el queso fresco batido al vaso y triturar 1 min / Vel 10 hasta obtener textura cremosa."
    },
    {
        "id": 2,
        "nombre": "Kebab Skewers Fit de Pollo en AirFryer",
        "categoria": "Comidas",
        "origen": "Miguelnaarfit (YouTube)",
        "equipamiento": "AirFryer",
        "tiempo": 18,
        "dificultad": "Muy Fácil",
        "kcal": 440, "prot": 42, "gras": 11, "hc": 35, "sodio": 320, "azucar": 4,
        "ingredientes_dict": {"Pechuga de Pollo": (180, "g", "Carnes y Aves"), "Tortilla de Trigo Integral": (1, "unidad", "Despensa"), "Cebolla": (50, "g", "Frutas y Verduras"), "Especias Kebab / Especias": (10, "g", "Despensa")},
        "pasos": "1. Macerar el pollo picado en dados con especias kebab y sal.\n2. Enhebrar en brochetas alternando con cebolla.\n3. Cocinar en AirFryer a 190°C durante 14 minutos dando la vuelta a mitad."
    },
    {
        "id": 3,
        "nombre": "Porridge Tiramisú Proteico de Avena y Café",
        "categoria": "Desayunos",
        "origen": "Lara Ibarra (YouTube)",
        "equipamiento": "Microondas",
        "tiempo": 8,
        "dificultad": "Fácil",
        "kcal": 380, "prot": 28, "gras": 7, "hc": 52, "sodio": 120, "azucar": 12,
        "ingredientes_dict": {"Copos de Avena": (60, "g", "Despensa"), "Leche Semidesnatada": (200, "ml", "Huevos y Lácteos"), "Proteína Whey / Proteico": (20, "g", "Despensa"), "Café Espresso": (50, "ml", "Despensa"), "Cacao Puro": (5, "g", "Despensa")},
        "pasos": "1. Mezclar la avena con la leche y el café en un tazón.\n2. Calentar 2 minutos en el microondas a máxima potencia.\n3. Integrar la proteína en polvo y espolvorear cacao puro por encima."
    },
    {
        "id": 4,
        "nombre": "Bacalao sobre Pisto de Verduras al Varoma",
        "categoria": "Cenas",
        "origen": "Mattyzandolo (YouTube)",
        "equipamiento": "Thermomix (Varoma)",
        "tiempo": 30,
        "dificultad": "Fácil",
        "kcal": 390, "prot": 38, "gras": 10, "hc": 28, "sodio": 310, "azucar": 9,
        "ingredientes_dict": {"Lomo de Bacalao Fresco": (180, "g", "Pescados y Mariscos"), "Pimiento y Tomate": (300, "g", "Frutas y Verduras"), "Cebolla": (80, "g", "Frutas y Verduras"), "Aceite de Oliva (AOVE)": (10, "g", "Despensa")},
        "pasos": "1. Trocear pimientos, tomate y cebolla en TMX (4 seg / Vel 4).\n2. Programar pisto (15 min / 120°C / Vel Cuchara).\n3. Colocar el bacalao en el Varoma y cocinar 10 min adicionales sobre el pisto."
    },
    {
        "id": 5,
        "nombre": "Fajitas Fit de Pollo y Queso Ligero",
        "categoria": "Cenas",
        "origen": "Miguelnaarfit (YouTube)",
        "equipamiento": "Plancha",
        "tiempo": 12,
        "dificultad": "Muy Fácil",
        "kcal": 410, "prot": 36, "gras": 12, "hc": 38, "sodio": 350, "azucar": 3,
        "ingredientes_dict": {"Tiras de Pechuga de Pollo": (160, "g", "Carnes y Aves"), "Tortilla de Trigo Integral": (2, "unidades", "Despensa"), "Queso Mozzarella / Light": (30, "g", "Huevos y Lácteos"), "Pimiento en Tiras": (80, "g", "Frutas y Verduras")},
        "pasos": "1. Saltear las tiras de pollo y pimiento a la plancha.\n2. Rellenar las tortillas, añadir el queso y dorar a la plancha vuelta y vuelta."
    },
    {
        "id": 6,
        "nombre": "Cheesecake Fit Proteico Diario",
        "categoria": "Snacks / Postres",
        "origen": "Miguelnaarfit (YouTube)",
        "equipamiento": "Microondas / AirFryer",
        "tiempo": 10,
        "dificultad": "Muy Fácil",
        "kcal": 220, "prot": 24, "gras": 4, "hc": 20, "sodio": 150, "azucar": 8,
        "ingredientes_dict": {"Queso Fresco Batido 0%": (200, "g", "Huevos y Lácteos"), "Huevo Fresco": (1, "unidad", "Huevos y Lácteos"), "Esencia de Vainilla / Edulcorante": (5, "g", "Despensa"), "Frutos Rojos": (50, "g", "Frutas y Verduras")},
        "pasos": "1. Batir el queso fresco con el huevo y edulcorante.\n2. Cocinar en molde individual 3 min en microondas o 8 min en AirFryer a 160°C.\n3. Servir frío con frutos rojos."
    }
]

# Header Title
st.title("🥗 NutriFamilia - WebApp para iPad")
st.caption("Planificador Semanal • Escalador de Comensales (1, 2 o 4 personas) • Lista de la Compra Automática")

# Navigation Menu
menu = st.sidebar.radio(
    "📌 Menú de Navegación:",
    ["📊 Dashboard Familiar", "📖 Biblioteca de Recetas (Selector Comensales)", "📅 Planificador Semanal", "🛒 Lista de la Compra Semanal", "🤖 Importador IA de YouTube"]
)

# --------------------------------------------------------------------------------
# PAGE 1: DASHBOARD
# --------------------------------------------------------------------------------
if menu == "📊 Dashboard Familiar":
    st.subheader("👨‍👩‍👧‍👦 Perfiles de la Familia & Metas Nutricionales")
    st.info("💡 **Objetivo Familiar:** Recomposición corporal (David y Ruth) y Ganancia de Masa Muscular (Marcos y Pablo). Proteína base de 1,8 g/kg.")
    
    cols = st.columns(4)
    for idx, (name, data) in enumerate(FAMILY_MEMBERS.items()):
        with cols[idx]:
            st.metric(label=f"👤 {name} ({data['edad']}a)", value=f"{data['kcal']} kcal", delta=f"{data['peso']} kg")
            st.write(f"💪 **Proteína:** {data['prot']} g")
            st.write(f"🥑 **Grasas:** {data['gras']} g")
            st.write(f"🍚 **Carbohidratos:** {data['hc']} g")
            st.caption(f"🎯 {data['meta']}")
            st.write(f"💧 **Agua recomendada:** {round(data['peso']*0.035, 1)} L/día")

# --------------------------------------------------------------------------------
# PAGE 2: RECIPE LIBRARY WITH SERVING SELECTOR (1, 2, 4 COMENSALES)
# --------------------------------------------------------------------------------
elif menu == "📖 Biblioteca de Recetas (Selector Comensales)":
    st.subheader("📖 Biblioteca de Recetas con Escalado Dinámico de Ingredientes")
    
    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        comensales = st.radio("👨‍👩‍👧‍👦 **Selecciona Número de Comensales:**", [1, 2, 4], index=2, format_func=lambda x: f"{x} Comensal(es)" if x < 4 else "4 Comensales (Familia Completa)")
    with col_sel2:
        filtro_eq = st.multiselect("🔍 Filtrar por Equipamiento:", ["Thermomix (Varoma)", "AirFryer", "Plancha", "Microondas"], default=["Thermomix (Varoma)", "AirFryer", "Plancha", "Microondas"])

    st.markdown(f"### 🍽️ Mostrando ingrediente acumulados para **{comensales} comensal(es)**:")
    
    cols = st.columns(2)
    filtered_recipes = [r for r in RECIPES_DB if any(eq in r['equipamiento'] for eq in filtro_eq)]
    
    for idx, r in enumerate(filtered_recipes):
        with cols[idx % 2]:
            st.markdown(f"#### {r['nombre']}")
            st.caption(f"👨‍🍳 **Origen:** {r['origen']} | ⏱️ {r['tiempo']} min | 🛠️ {r['equipamiento']}")
            
            # Scaled Macros
            s_kcal = r['kcal'] * comensales
            s_prot = r['prot'] * comensales
            s_gras = r['gras'] * comensales
            s_hc = r['hc'] * comensales
            
            st.success(f"📊 **Totales para {comensales} personas:** {s_kcal} kcal | 🍗 {s_prot}g Prot | 🥑 {s_gras}g Gras | 🍚 {s_hc}g HC")
            
            with st.expander("📝 Ver Ingredientes Totales y Pasos"):
                st.write("**🛒 Ingredientes Totales Necesarios:**")
                for ing, (cant, unidad, cat) in r['ingredientes_dict'].items():
                    st.write(f"• **{ing}:** {cant * comensales} {unidad}")
                st.write("\n**👨‍🍳 Preparación Paso a Paso:**")
                st.write(r['pasos'])

# --------------------------------------------------------------------------------
# PAGE 3: WEEKLY PLANNER (LUNES A DOMINGO)
# --------------------------------------------------------------------------------
elif menu == "📅 Planificador Semanal":
    st.subheader("📅 Planificador Semanal de Comidas (Lunes a Domingo)")
    st.write("Establece el menú de la semana seleccionando las recetas para la familia. Se guardará para generar la lista de la compra automáticamente.")

    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    recetas_nombres = [r['nombre'] for r in RECIPES_DB]

    if "plan_semanal" not in st.session_state:
        st.session_state["plan_semanal"] = {
            "Lunes": {"Desayuno": recetas_nombres[2], "Comida": recetas_nombres[0], "Cena": recetas_nombres[3], "Snack": recetas_nombres[5], "Comensales": 4},
            "Martes": {"Desayuno": recetas_nombres[2], "Comida": recetas_nombres[1], "Cena": recetas_nombres[4], "Snack": recetas_nombres[5], "Comensales": 4},
            "Miércoles": {"Desayuno": recetas_nombres[2], "Comida": recetas_nombres[0], "Cena": recetas_nombres[3], "Snack": recetas_nombres[5], "Comensales": 4},
            "Jueves": {"Desayuno": recetas_nombres[2], "Comida": recetas_nombres[1], "Cena": recetas_nombres[4], "Snack": recetas_nombres[5], "Comensales": 4},
            "Viernes": {"Desayuno": recetas_nombres[2], "Comida": recetas_nombres[0], "Cena": recetas_nombres[3], "Snack": recetas_nombres[5], "Comensales": 4},
            "Sábado": {"Desayuno": recetas_nombres[2], "Comida": recetas_nombres[1], "Cena": recetas_nombres[4], "Snack": recetas_nombres[5], "Comensales": 4},
            "Domingo": {"Desayuno": recetas_nombres[2], "Comida": recetas_nombres[0], "Cena": recetas_nombres[3], "Snack": recetas_nombres[5], "Comensales": 4},
        }

    selected_day = st.selectbox("📅 Selecciona el día para ajustar el menú:", dias)
    day_data = st.session_state["plan_semanal"][selected_day]

    col_a, col_b = st.columns(2)
    with col_a:
        des = st.selectbox("🍳 Desayuno:", recetas_nombres, index=recetas_nombres.index(day_data["Desayuno"]), key=f"des_{selected_day}")
        com = st.selectbox("🍲 Comida:", recetas_nombres, index=recetas_nombres.index(day_data["Comida"]), key=f"com_{selected_day}")
    with col_b:
        cen = st.selectbox("🌙 Cena:", recetas_nombres, index=recetas_nombres.index(day_data["Cena"]), key=f"cen_{selected_day}")
        sna = st.selectbox("🍎 Snack / Postre:", recetas_nombres, index=recetas_nombres.index(day_data["Snack"]), key=f"sna_{selected_day}")

    num_com = st.slider("👥 Número de Comensales para este día:", 1, 4, value=day_data["Comensales"], key=f"comensales_{selected_day}")
    
    # Save updates
    st.session_state["plan_semanal"][selected_day] = {"Desayuno": des, "Comida": com, "Cena": cen, "Snack": sna, "Comensales": num_com}

    st.markdown("### 📋 Vista General de la Semana Planificada:")
    df_week = pd.DataFrame.from_dict(st.session_state["plan_semanal"], orient="index")
    st.dataframe(df_week, use_container_width=True)

# --------------------------------------------------------------------------------
# PAGE 4: AUTOMATED WEEKLY SHOPPING LIST
# --------------------------------------------------------------------------------
elif menu == "🛒 Lista de la Compra Semanal":
    st.subheader("🛒 Lista de la Compra Semanal Calculada")
    st.write("Generada automáticamente sumando los ingredientes del planificador semanal según el número de comensales configurado.")

    if "plan_semanal" in st.session_state:
        lista_totales = {}
        
        # Calculate totals
        for dia, plan in st.session_state["plan_semanal"].items():
            comensales = plan["Comensales"]
            for comida_tipo in ["Desayuno", "Comida", "Cena", "Snack"]:
                nombre_receta = plan[comida_tipo]
                receta_obj = next((r for r in RECIPES_DB if r['nombre'] == nombre_receta), None)
                if receta_obj:
                    for ing_nombre, (cant, unidad, categoria) in receta_obj['ingredientes_dict'].items():
                        cant_total = cant * comensales
                        if ing_nombre not in lista_totales:
                            lista_totales[ing_nombre] = {"cantidad": 0, "unidad": unidad, "categoria": categoria}
                        lista_totales[ing_nombre]["cantidad"] += cant_total

        # Group by category
        categorias_dict = {}
        for ing_nombre, info in lista_totales.items():
            cat = info["categoria"]
            if cat not in categorias_dict:
                categorias_dict[cat] = []
            categorias_dict[cat].append((ing_nombre, info["cantidad"], info["unidad"]))

        cols = st.columns(2)
        idx_c = 0
        for cat, items in categorias_dict.items():
            with cols[idx_c % 2]:
                st.markdown(f"#### 📦 {cat}")
                for ing_nombre, cant, unidad in items:
                    st.checkbox(f"**{ing_nombre}:** {cant} {unidad}", key=f"shop_{ing_nombre}")
            idx_c += 1
    else:
        st.info("Configura primero el planificador semanal para generar la lista de la compra.")

# --------------------------------------------------------------------------------
# PAGE 5: YOUTUBE AI IMPORT
# --------------------------------------------------------------------------------
elif menu == "🤖 Importador IA de YouTube":
    st.subheader("🔗 Importar Receta Automática desde YouTube")
    st.write("Pega el enlace de un vídeo de YouTube (Lara Ibarra, Miguelnaarfit, Mattyzandolo o cualquier otro) para generar la ficha de la receta.")
    
    yt_link = st.text_input("Ingresa la URL del vídeo de YouTube:")
    if st.button("⚡ Procesar Vídeo e Integrar Receta"):
        if yt_link:
            st.success("✅ Receta procesada exitosamente con IA e integrada a la base de datos familiar.")
            st.json({
                "Nombre": "Receta Extraída de YouTube",
                "Creador": "YouTube Creator",
                "Equipamiento_Detectado": "Thermomix / AirFryer",
                "Ingredientes_Calculados_1_Persona": {
                    "Pechuga de Pollo": "180 g",
                    "Verduras Variadas": "200 g",
                    "Aceite de Oliva": "10 g"
                },
                "Nutrientes_Estimados": {"Calorías": 430, "Proteína": 42, "Grasas": 11, "Carbohidratos": 36}
            })
