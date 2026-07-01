import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Configuración general de la página ──────────────────────────────────────
st.set_page_config(
    page_title="Credit Card Churn Analysis",
    page_icon="💳",
    layout="wide"
)

# ── Paleta de colores ──────────────
COLORS = {
    0: '#2196F3',   # azul — cliente activo
    1: '#E53935'    # rojo — cliente churner
}
CHURN_RATE_BASE = 16.07  # línea de referencia global

# ── Carga de datos ───────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('./data/processed/BankChurners_clean.csv')

df = load_data()

# ── CSS ────────────────────────────────────────────────────────
st.markdown("""
    <style>
        /* Fuente general */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Hero section */
        .hero-container {
            background: linear-gradient(135deg, #0D1B2A 0%, #1B2A3B 100%);
            border-radius: 16px;
            padding: 56px 48px;
            margin-bottom: 40px;
        }
        .hero-label {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #2196F3;
            margin-bottom: 16px;
        }
        .hero-title {
            font-size: 42px;
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1.15;
            margin-bottom: 16px;
        }
        .hero-subtitle {
            font-size: 18px;
            font-weight: 400;
            color: #90A4AE;
            max-width: 600px;
            line-height: 1.6;
            margin-bottom: 0;
        }

        /* KPI cards */
        .kpi-card {
            background: #1B2A3B;
            border: 1px solid #263545;
            border-radius: 12px;
            padding: 24px 28px;
            text-align: center;
        }
        .kpi-value {
            font-size: 36px;
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1;
            margin-bottom: 6px;
        }
        .kpi-value.churn {
            color: #E53935;
        }
        .kpi-label {
            font-size: 13px;
            font-weight: 500;
            color: #78909C;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Divider */
        .section-divider {
            border: none;
            border-top: 1px solid #263545;
            margin: 48px 0;
        }

        /* Intro text */
        .intro-text {
            font-size: 16px;
            color: #B0BEC5;
            line-height: 1.8;
            max-width: 720px;
        }
    </style>
""", unsafe_allow_html=True)

# ── SECCIÓN 0: Hero ──────────────────────────────────────────────────────────
st.markdown("""
    <div class="hero-container">
        <p class="hero-label">Análisis de churn bancario · 2025</p>
        <h1 class="hero-title">Credit Card<br>Churn Analysis</h1>
        <p class="hero-subtitle">¿Cuál es el perfil de cliente que cancela su tarjeta de crédito?</p>
    </div>
""", unsafe_allow_html=True)

# KPIs
total = len(df)
churners = df['Attrition_Flag'].sum()
churn_rate = churners / total * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-label">Clientes analizados</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value churn">{churn_rate:.2f}%</div>
            <div class="kpi-label">Tasa de churn</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value churn">{int(churners):,}</div>
            <div class="kpi-label">Clientes que cancelaron</div>
        </div>
    """, unsafe_allow_html=True)

# Texto introductorio
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

st.markdown("""
    <p class="intro-text">
        Este análisis explora el comportamiento de <strong style="color:#FFFFFF">10,127 clientes</strong>
        de una entidad bancaria para identificar qué factores distinguen a quienes cancelan
        su tarjeta de crédito de quienes la mantienen. A través de variables demográficas,
        de vinculación con el banco y de comportamiento transaccional, construimos el perfil
        del cliente en riesgo de abandono — y las señales que lo anticipan.
    </p>
""", unsafe_allow_html=True)

# ── SECCIÓN 1: ¿Quién es el cliente? ────────────────────────────────────────
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

st.markdown("""
    <p class="hero-label">Sección 01</p>
    <h2 style="color:#FFFFFF; font-size:28px; font-weight:700; margin-bottom:8px;">
        ¿Quién es el cliente que cancela?
    </h2>
    <p class="intro-text" style="margin-bottom:32px;">
        El primer instinto al analizar churn es buscar un perfil demográfico claro.
        ¿Son más jóvenes? ¿Tienen menos ingresos? ¿Son hombres o mujeres?
        Los datos ofrecen una respuesta sorprendente.
    </p>
""", unsafe_allow_html=True)

# Selector interactivo
var_demo = st.selectbox(
    "Explora la tasa de churn por variable demográfica:",
    options={
        'Género': 'Gender',
        'Nivel educativo': 'Education_Level',
        'Estado civil': 'Marital_Status',
        'Nivel de ingresos': 'Income_Category'
    }.keys()
)

# Mapeo de selección a columna
col_map = {
    'Género': 'Gender',
    'Nivel educativo': 'Education_Level',
    'Estado civil': 'Marital_Status',
    'Nivel de ingresos': 'Income_Category'
}
col_selected = col_map[var_demo]

# Etiquetas legibles para Gender
if col_selected == 'Gender':
    df_plot = df.copy()
    df_plot['Gender'] = df_plot['Gender'].map({0: 'Hombre', 1: 'Mujer'})
else:
    df_plot = df.copy()

# Calcular tasa de churn por categoría
churn_by_var = (
    df_plot.groupby(col_selected)['Attrition_Flag']
    .mean()
    .mul(100)
    .reset_index()
    .rename(columns={'Attrition_Flag': 'Tasa de churn (%)'})
)

col_izq, col_der = st.columns([1.5, 1])

with col_izq:
    fig_demo = px.bar(
        churn_by_var,
        x=col_selected,
        y='Tasa de churn (%)',
        color='Tasa de churn (%)',
        color_continuous_scale=[[0, '#1B2A3B'], [0.5, '#2196F3'], [1, '#E53935']],
        text='Tasa de churn (%)',
    )
    fig_demo.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    fig_demo.add_hline(
        y=CHURN_RATE_BASE,
        line_dash='dash',
        line_color='#78909C',
        annotation_text=f'Tasa base {CHURN_RATE_BASE}%',
        annotation_position='top right'
    )
    fig_demo.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#B0BEC5',
        coloraxis_showscale=False,
        xaxis=dict(title='', gridcolor='#263545'),
        yaxis=dict(title='Tasa de churn (%)', gridcolor='#263545', range=[0, 30]),
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_demo, use_container_width=True)

with col_der:
    st.markdown("""
        <div style="background:#1B2A3B; border-radius:12px; padding:24px; border:1px solid #263545; margin-top:20px;">
            <p style="color:#2196F3; font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">
                Conclusión
            </p>
            <p style="color:#ECEFF1; font-size:15px; line-height:1.7; margin-bottom:16px;">
                Ninguna variable demográfica supera los <strong style="color:#FFFFFF">5 puntos de diferencia</strong>
                respecto a la tasa base del 16.07%.
            </p>
            <p style="color:#90A4AE; font-size:14px; line-height:1.7;">
                El cliente que cancela no tiene un perfil demográfico diferencial.
                Puede tener cualquier edad, género, nivel educativo o renta.
                <strong style="color:#FFFFFF">No es quién es, sino cómo se comporta.</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)

# Boxplot edad
st.markdown("<br>", unsafe_allow_html=True)

fig_age = px.box(
    df,
    x='Attrition_Flag',
    y='Customer_Age',
    color='Attrition_Flag',
    color_discrete_map=COLORS,
    labels={
        'Attrition_Flag': 'Estado del cliente',
        'Customer_Age': 'Edad'
    },
    category_orders={'Attrition_Flag': [0, 1]}
)
fig_age.update_layout(
    title=dict(
        text='Distribución de edad por estado del cliente',
        font=dict(color='#ECEFF1', size=16)
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#B0BEC5',
    xaxis=dict(
        tickvals=[0, 1],
        ticktext=['Activo', 'Cancelado'],
        gridcolor='#263545'
    ),
    yaxis=dict(gridcolor='#263545'),
    showlegend=False,
    margin=dict(t=40, b=20)
)
st.plotly_chart(fig_age, use_container_width=True)

st.markdown("""
    <p style="color:#78909C; font-size:13px; font-style:italic; text-align:center; margin-top:-16px;">
        Las distribuciones de edad son prácticamente idénticas entre ambos grupos
        (mediana 46 vs 47 años). La edad no predice la cancelación.
    </p>
""", unsafe_allow_html=True)

# ── SECCIÓN 2: Vinculación con el banco ─────────────────────────────────────
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

st.markdown("""
    <p class="hero-label">Sección 02</p>
    <h2 style="color:#FFFFFF; font-size:28px; font-weight:700; margin-bottom:8px;">
        Vinculación con el banco
    </h2>
    <p class="intro-text" style="margin-bottom:32px;">
        Si la demografía no explica el churn, quizás la relación del cliente
        con la entidad sí lo haga. ¿Importa cuánto tiempo lleva con el banco?
        ¿Cuántos productos tiene contratados? ¿Con qué frecuencia contacta
        con el servicio de atención al cliente?
    </p>
""", unsafe_allow_html=True)

# ── 2.1 Número de productos contratados ─────────────────────────────────────
churn_productos = (
    df.groupby('Total_Relationship_Count')['Attrition_Flag']
    .mean()
    .mul(100)
    .reset_index()
    .rename(columns={'Attrition_Flag': 'Tasa de churn (%)'})
)

col_izq, col_der = st.columns([1.5, 1])

with col_izq:
    fig_productos = px.bar(
        churn_productos,
        x='Total_Relationship_Count',
        y='Tasa de churn (%)',
        color='Tasa de churn (%)',
        color_continuous_scale=[[0, '#1B2A3B'], [0.5, '#2196F3'], [1, '#E53935']],
        text='Tasa de churn (%)',
        labels={'Total_Relationship_Count': 'Número de productos contratados'}
    )
    fig_productos.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    fig_productos.add_hline(
        y=CHURN_RATE_BASE,
        line_dash='dash',
        line_color='#78909C',
        annotation_text=f'Tasa base {CHURN_RATE_BASE}%',
        annotation_position='top right'
    )
    fig_productos.update_layout(
        title=dict(
            text='Tasa de churn por número de productos contratados',
            font=dict(color='#ECEFF1', size=16)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#B0BEC5',
        coloraxis_showscale=False,
        xaxis=dict(title='Número de productos contratados', gridcolor='#263545', dtick=1),
        yaxis=dict(title='Tasa de churn (%)', gridcolor='#263545', range=[0, 35]),
        margin=dict(t=40, b=20)
    )
    st.plotly_chart(fig_productos, use_container_width=True)

with col_der:
    st.markdown("""
        <div style="background:#1B2A3B; border-radius:12px; padding:24px;
                    border:1px solid #263545; margin-top:48px;">
            <p style="color:#2196F3; font-size:11px; font-weight:700;
                      letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">
                Hallazgo
            </p>
            <p style="color:#ECEFF1; font-size:15px; line-height:1.7; margin-bottom:16px;">
                Con <strong style="color:#FFFFFF">1-2 productos</strong> contratados,
                la tasa de churn alcanza el <strong style="color:#E53935">25-28%</strong>
                — casi el doble que la base.
            </p>
            <p style="color:#90A4AE; font-size:14px; line-height:1.7;">
                A partir de 4 productos, el churn cae por debajo del
                <strong style="color:#FFFFFF">12%</strong> y se estabiliza.
                Cada producto adicional actúa como un <em>colchón de retención</em>.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ── 2.2 Contactos con el banco ───────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

churn_contactos = (
    df.groupby('Contacts_Count_12_mon')['Attrition_Flag']
    .mean()
    .mul(100)
    .reset_index()
    .rename(columns={'Attrition_Flag': 'Tasa de churn (%)'})
)

col_izq, col_der = st.columns([1, 1.5])

with col_der:
    fig_contactos = px.bar(
        churn_contactos,
        x='Contacts_Count_12_mon',
        y='Tasa de churn (%)',
        color='Tasa de churn (%)',
        color_continuous_scale=[[0, '#1B2A3B'], [0.5, '#2196F3'], [1, '#E53935']],
        text='Tasa de churn (%)',
        labels={'Contacts_Count_12_mon': 'Contactos con el banco (últimos 12 meses)'}
    )
    fig_contactos.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    fig_contactos.add_hline(
        y=CHURN_RATE_BASE,
        line_dash='dash',
        line_color='#78909C',
        annotation_text=f'Tasa base {CHURN_RATE_BASE}%',
        annotation_position='top right'
    )
    fig_contactos.update_layout(
        title=dict(
            text='Tasa de churn por número de contactos con el banco',
            font=dict(color='#ECEFF1', size=16)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#B0BEC5',
        coloraxis_showscale=False,
        xaxis=dict(title='Contactos (últimos 12 meses)', gridcolor='#263545', dtick=1),
        yaxis=dict(title='Tasa de churn (%)', gridcolor='#263545', range=[0, 110]),
        margin=dict(t=40, b=20)
    )
    st.plotly_chart(fig_contactos, use_container_width=True)

with col_izq:
    st.markdown("""
        <div style="background:#1B2A3B; border-radius:12px; padding:24px;
                    border:1px solid #263545; margin-top:48px;">
            <p style="color:#2196F3; font-size:11px; font-weight:700;
                      letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">
                La señal más accionable
            </p>
            <p style="color:#ECEFF1; font-size:15px; line-height:1.7; margin-bottom:16px;">
                La relación entre contactos y churn es
                <strong style="color:#FFFFFF">perfectamente monótona</strong>:
                sin excepciones de 0 a 6 contactos.
            </p>
            <p style="color:#90A4AE; font-size:14px; line-height:1.7; margin-bottom:12px;">
                Los clientes que contactaron
                <strong style="color:#E53935">6 veces</strong> con el banco
                en los últimos 12 meses cancelaron
                <strong style="color:#E53935">en su totalidad</strong>.
            </p>
            <p style="color:#90A4AE; font-size:14px; line-height:1.7;">
                Múltiples contactos son una señal de fricción o insatisfacción
                no resuelta — el banco tiene visibilidad de este indicador
                antes de que se produzca la cancelación.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ── 2.3 Meses de inactividad ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

# Excluimos el caso 0 por tamaño muestral insuficiente (29 clientes)
churn_inactividad = (
    df[df['Months_Inactive_12_mon'] > 0]
    .groupby('Months_Inactive_12_mon')['Attrition_Flag']
    .mean()
    .mul(100)
    .reset_index()
    .rename(columns={'Attrition_Flag': 'Tasa de churn (%)'})
)

fig_inactividad = px.bar(
    churn_inactividad,
    x='Months_Inactive_12_mon',
    y='Tasa de churn (%)',
    color='Tasa de churn (%)',
    color_continuous_scale=[[0, '#1B2A3B'], [0.5, '#2196F3'], [1, '#E53935']],
    text='Tasa de churn (%)',
    labels={'Months_Inactive_12_mon': 'Meses de inactividad (últimos 12 meses)'}
)
fig_inactividad.update_traces(
    texttemplate='%{text:.1f}%',
    textposition='outside'
)
fig_inactividad.add_hline(
    y=CHURN_RATE_BASE,
    line_dash='dash',
    line_color='#78909C',
    annotation_text=f'Tasa base {CHURN_RATE_BASE}%',
    annotation_position='top right'
)
fig_inactividad.update_layout(
    title=dict(
        text='Tasa de churn por meses de inactividad',
        font=dict(color='#ECEFF1', size=16)
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#B0BEC5',
    coloraxis_showscale=False,
    xaxis=dict(title='Meses inactivo (últimos 12)', gridcolor='#263545', dtick=1),
    yaxis=dict(title='Tasa de churn (%)', gridcolor='#263545', range=[0, 35]),
    margin=dict(t=40, b=20)
)
st.plotly_chart(fig_inactividad, use_container_width=True)

st.markdown("""
    <p style="color:#78909C; font-size:13px; font-style:italic; text-align:center; margin-top:-16px;">
        El pico de churn aparece con 4 meses de inactividad (29.9%). Se excluye la categoría
        de 0 meses por tamaño de muestra insuficiente (29 clientes).
    </p>
""", unsafe_allow_html=True)

# Expander con nota metodológica
with st.expander("¿Por qué no aparece la antigüedad del cliente en este análisis?"):
    st.markdown("""
        <p style="color:#90A4AE; font-size:14px; line-height:1.7;">
            <code>Months_on_book</code> (antigüedad del cliente con el banco) no muestra
            ninguna diferencia relevante entre clientes activos y cancelados
            (medias de 35.88 vs 36.18 meses). Al igual que las variables demográficas,
            la antigüedad no predice el churn — un cliente veterano no es más fiel
            que uno reciente si su comportamiento de uso es bajo.
        </p>
    """, unsafe_allow_html=True)

# ── SECCIÓN 3: Comportamiento de crédito ────────────────────────────────────
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

st.markdown("""
    <p class="hero-label">Sección 03</p>
    <h2 style="color:#FFFFFF; font-size:28px; font-weight:700; margin-bottom:8px;">
        Comportamiento de crédito
    </h2>
    <p class="intro-text" style="margin-bottom:32px;">
        La hipótesis más intuitiva sobre el churn bancario apunta a la deuda:
        clientes atrapados por el crédito revolving, frustrados por los intereses,
        que acaban cancelando. Los datos cuentan una historia diferente.
    </p>
""", unsafe_allow_html=True)

# ── 3.1 Revolving Use ────────────────────────────────────────────────────────
churn_revolving = (
    df.groupby('Revolving_Use')['Attrition_Flag']
    .mean()
    .mul(100)
    .reset_index()
    .rename(columns={'Attrition_Flag': 'Tasa de churn (%)'})
)
churn_revolving['Uso de crédito revolving'] = churn_revolving['Revolving_Use'].map({
    0: 'No usa revolving',
    1: 'Usa revolving'
})

col_izq, col_der = st.columns([1.5, 1])

with col_izq:
    fig_revolving = px.bar(
        churn_revolving,
        x='Uso de crédito revolving',
        y='Tasa de churn (%)',
        color='Tasa de churn (%)',
        color_continuous_scale=[[0, '#1B2A3B'], [0.5, '#2196F3'], [1, '#E53935']],
        text='Tasa de churn (%)',
    )
    fig_revolving.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    fig_revolving.add_hline(
        y=CHURN_RATE_BASE,
        line_dash='dash',
        line_color='#78909C',
        annotation_text=f'Tasa base {CHURN_RATE_BASE}%',
        annotation_position='top right'
    )
    fig_revolving.update_layout(
        title=dict(
            text='Tasa de churn según uso de crédito revolving',
            font=dict(color='#ECEFF1', size=16)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#B0BEC5',
        coloraxis_showscale=False,
        xaxis=dict(title='', gridcolor='#263545'),
        yaxis=dict(title='Tasa de churn (%)', gridcolor='#263545', range=[0, 45]),
        margin=dict(t=40, b=20)
    )
    st.plotly_chart(fig_revolving, use_container_width=True)

with col_der:
    st.markdown("""
        <div style="background:#1B2A3B; border-radius:12px; padding:24px;
                    border:1px solid #263545; margin-top:48px;">
            <p style="color:#2196F3; font-size:11px; font-weight:700;
                      letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">
                Contra lo esperado
            </p>
            <p style="color:#ECEFF1; font-size:15px; line-height:1.7; margin-bottom:16px;">
                De los clientes que <strong style="color:#FFFFFF">no usan crédito revolving</strong>,
                el <strong style="color:#E53935">36.2%</strong> acaba cancelando.
                Entre quienes sí lo usan, esa cifra cae al <strong style="color:#2196F3">9.6%</strong>.
            </p>
            <p style="color:#90A4AE; font-size:14px; line-height:1.7;">
                El cliente que cancela no está atrapado por la deuda.
                Simplemente <strong style="color:#FFFFFF">no usa el crédito</strong>
                — una señal más de desconexión con el producto.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ── 3.2 Avg Utilization Ratio ────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

col_izq, col_der = st.columns([1, 1.5])

with col_der:
    fig_util = px.box(
        df,
        x='Attrition_Flag',
        y='Avg_Utilization_Ratio',
        color='Attrition_Flag',
        color_discrete_map=COLORS,
        labels={
            'Attrition_Flag': 'Estado del cliente',
            'Avg_Utilization_Ratio': 'Ratio de utilización'
        }
    )
    fig_util.update_layout(
        title=dict(
            text='Ratio de utilización del crédito por estado del cliente',
            font=dict(color='#ECEFF1', size=16)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#B0BEC5',
        xaxis=dict(
            tickvals=[0, 1],
            ticktext=['Activo', 'Cancelado'],
            gridcolor='#263545'
        ),
        yaxis=dict(gridcolor='#263545', title='Ratio de utilización (0-1)'),
        showlegend=False,
        margin=dict(t=40, b=20)
    )
    st.plotly_chart(fig_util, use_container_width=True)

with col_izq:
    st.markdown("""
        <div style="background:#1B2A3B; border-radius:12px; padding:24px;
                    border:1px solid #263545; margin-top:48px;">
            <p style="color:#2196F3; font-size:11px; font-weight:700;
                      letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">
                Lectura del boxplot
            </p>
            <p style="color:#ECEFF1; font-size:15px; line-height:1.7; margin-bottom:16px;">
                La mediana de utilización del cliente que cancela es
                <strong style="color:#E53935">0.000</strong> — no usa
                prácticamente nada de su límite de crédito.
            </p>
            <p style="color:#90A4AE; font-size:14px; line-height:1.7; margin-bottom:12px;">
                Los clientes activos tienen una mediana de
                <strong style="color:#2196F3">0.211</strong> y una distribución
                mucho más amplia — usan el crédito de forma real y continua.
            </p>
            <p style="color:#90A4AE; font-size:14px; line-height:1.7;">
                Los puntos en la parte superior del grupo cancelado son
                un segmento minoritario con alta utilización. Analizando
                el dataset completo, los clientes con ratio superior a 0.57
                tienen una tasa de churn del <strong style="color:#FFFFFF">9.7%</strong> — por debajo
                de la base. La alta utilización del crédito está asociada
                a <strong style="color:#FFFFFF">mayor retención</strong>,
                no a mayor riesgo de cancelación.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ── 3.3 Expander: renta vs utilización ──────────────────────────────────────
with st.expander("¿Afecta el nivel de ingresos al uso del crédito?"):
    renta_util = (
        df.groupby('Income_Category')[['Total_Trans_Ct', 'Avg_Utilization_Ratio']]
        .mean()
        .reset_index()
        .sort_values('Avg_Utilization_Ratio', ascending=False)
    )

    fig_renta = px.bar(
        renta_util,
        x='Income_Category',
        y='Avg_Utilization_Ratio',
        color='Avg_Utilization_Ratio',
        color_continuous_scale=[[0, '#1B2A3B'], [0.5, '#2196F3'], [1, '#E53935']],
        text='Avg_Utilization_Ratio',
        labels={
            'Income_Category': 'Nivel de ingresos',
            'Avg_Utilization_Ratio': 'Ratio de utilización medio'
        }
    )
    fig_renta.update_traces(
        texttemplate='%{text:.3f}',
        textposition='outside'
    )
    fig_renta.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#B0BEC5',
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='#263545'),
        yaxis=dict(gridcolor='#263545', range=[0, 0.45]),
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_renta, use_container_width=True)

    st.markdown("""
        <p style="color:#90A4AE; font-size:14px; line-height:1.7;">
            A menor renta, mayor ratio de utilización del crédito — no porque
            gasten más, sino porque su límite de crédito es más bajo y cualquier
            gasto representa una proporción mayor del mismo. El número de
            transacciones, en cambio, es prácticamente idéntico en todos los
            segmentos de renta (62-66 transacciones de media).
        </p>
    """, unsafe_allow_html=True)

# ── SECCIÓN 4: Actividad transaccional ──────────────────────────────────────
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

st.markdown("""
    <p class="hero-label">Sección 04</p>
    <h2 style="color:#FFFFFF; font-size:28px; font-weight:700; margin-bottom:8px;">
        Actividad transaccional
    </h2>
    <p class="intro-text" style="margin-bottom:32px;">
        Si hay una variable que predice el churn por encima de todas las demás,
        es el número de transacciones. Con una correlación de <strong style="color:#FFFFFF">-0.37</strong>
        con la cancelación — la más alta del dataset — el comportamiento transaccional
        del cliente es la señal más clara y directa de lo que está por venir.
    </p>
""", unsafe_allow_html=True)

# ── 4.1 Histograma apilado Total_Trans_Ct ───────────────────────────────────
fig_hist = px.histogram(
    df,
    x='Total_Trans_Ct',
    color='Attrition_Flag',
    color_discrete_map=COLORS,
    nbins=40,
    barmode='stack',
    labels={
        'Total_Trans_Ct': 'Número de transacciones (últimos 12 meses)',
        'Attrition_Flag': 'Estado'
    },
    category_orders={'Attrition_Flag': [0, 1]}
)
fig_hist.update_layout(
    title=dict(
        text='Distribución del número de transacciones por estado del cliente',
        font=dict(color='#ECEFF1', size=16)
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#B0BEC5',
    xaxis=dict(title='Número de transacciones', gridcolor='#263545'),
    yaxis=dict(title='Número de clientes', gridcolor='#263545'),
    legend=dict(
        title='Estado',
        itemsizing='constant',
        bgcolor='rgba(0,0,0,0)',
        font=dict(color='#B0BEC5')
    ),
    margin=dict(t=40, b=20)
)
fig_hist.for_each_trace(lambda t: t.update(
    name='Activo' if t.name == '0' else 'Cancelado'
))
st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("""
    <p style="color:#78909C; font-size:13px; font-style:italic; text-align:center; margin-top:-16px;">
        El churn (rojo) se concentra casi exclusivamente en el primer pico de la distribución
        (20-50 transacciones). A partir de 60 transacciones, los cancelados prácticamente desaparecen.
    </p>
""", unsafe_allow_html=True)

# ── 4.2 Tabs: Volumen de uso / Evolución temporal ───────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Volumen de uso", "📉 Evolución temporal"])

with tab1:
    col_izq, col_der = st.columns(2)

    with col_izq:
        # Boxplot Total_Trans_Ct
        fig_ct = px.box(
            df,
            x='Attrition_Flag',
            y='Total_Trans_Ct',
            color='Attrition_Flag',
            color_discrete_map=COLORS,
            labels={
                'Attrition_Flag': 'Estado',
                'Total_Trans_Ct': 'Número de transacciones'
            }
        )
        fig_ct.update_layout(
            title=dict(
                text='Número de transacciones',
                font=dict(color='#ECEFF1', size=15)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#B0BEC5',
            xaxis=dict(
                tickvals=[0, 1],
                ticktext=['Activo', 'Cancelado'],
                gridcolor='#263545'
            ),
            yaxis=dict(gridcolor='#263545'),
            showlegend=False,
            margin=dict(t=40, b=20)
        )
        st.plotly_chart(fig_ct, use_container_width=True)
        st.markdown("""
            <p style="color:#78909C; font-size:13px; text-align:center;">
                Mediana: <strong style="color:#2196F3">71</strong> (activo)
                vs <strong style="color:#E53935">43</strong> (cancelado)
            </p>
        """, unsafe_allow_html=True)

    with col_der:
        # Boxplot Total_Trans_Amt
        fig_amt = px.box(
            df,
            x='Attrition_Flag',
            y='Total_Trans_Amt',
            color='Attrition_Flag',
            color_discrete_map=COLORS,
            labels={
                'Attrition_Flag': 'Estado',
                'Total_Trans_Amt': 'Importe total ($)'
            }
        )
        fig_amt.update_layout(
            title=dict(
                text='Importe total de transacciones',
                font=dict(color='#ECEFF1', size=15)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#B0BEC5',
            xaxis=dict(
                tickvals=[0, 1],
                ticktext=['Activo', 'Cancelado'],
                gridcolor='#263545'
            ),
            yaxis=dict(gridcolor='#263545'),
            showlegend=False,
            margin=dict(t=40, b=20)
        )
        st.plotly_chart(fig_amt, use_container_width=True)
        st.markdown("""
            <p style="color:#78909C; font-size:13px; text-align:center;">
                Mediana: <strong style="color:#2196F3">$4,100</strong> (activo)
                vs <strong style="color:#E53935">$2,329</strong> (cancelado)
            </p>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background:#1B2A3B; border-radius:12px; padding:20px 24px;
                    border:1px solid #263545; margin-top:8px;">
            <p style="color:#90A4AE; font-size:14px; line-height:1.7; margin:0;">
                El cliente que cancela realiza un <strong style="color:#FFFFFF">35% menos de transacciones</strong>
                y genera un <strong style="color:#FFFFFF">43% menos de importe</strong> que el cliente activo.
                Sin embargo, el importe medio por transacción es prácticamente idéntico
                (≈$63 en ambos grupos) — no es un cliente de menor poder adquisitivo,
                sino uno que usa la tarjeta con <strong style="color:#FFFFFF">mucha menos frecuencia</strong>.
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    col_izq, col_der = st.columns(2)

    with col_izq:
        # Boxplot Total_Ct_Chng_Q4_Q1
        fig_ct_chng = px.box(
            df,
            x='Attrition_Flag',
            y='Total_Ct_Chng_Q4_Q1',
            color='Attrition_Flag',
            color_discrete_map=COLORS,
            labels={
                'Attrition_Flag': 'Estado',
                'Total_Ct_Chng_Q4_Q1': 'Ratio Q4/Q1 (número de transacciones)'
            }
        )
        fig_ct_chng.update_layout(
            title=dict(
                text='Cambio en número de transacciones (Q4 vs Q1)',
                font=dict(color='#ECEFF1', size=15)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#B0BEC5',
            xaxis=dict(
                tickvals=[0, 1],
                ticktext=['Activo', 'Cancelado'],
                gridcolor='#263545'
            ),
            yaxis=dict(gridcolor='#263545'),
            showlegend=False,
            margin=dict(t=40, b=20)
        )
        st.plotly_chart(fig_ct_chng, use_container_width=True)
        st.markdown("""
            <p style="color:#78909C; font-size:13px; text-align:center;">
                Mediana: <strong style="color:#2196F3">0.721</strong> (activo)
                vs <strong style="color:#E53935">0.531</strong> (cancelado)
            </p>
        """, unsafe_allow_html=True)

    with col_der:
        fig_avg_amt = px.box(
            df,
            x='Attrition_Flag',
            y='Avg_Trans_Amt',
            color='Attrition_Flag',
            color_discrete_map=COLORS,
            labels={
                'Attrition_Flag': 'Estado',
                'Avg_Trans_Amt': 'Importe medio por transacción ($)'
            }
        )
        fig_avg_amt.update_layout(
            title=dict(
                text='Importe medio por transacción',
                font=dict(color='#ECEFF1', size=15)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#B0BEC5',
            xaxis=dict(
                tickvals=[0, 1],
                ticktext=['Activo', 'Cancelado'],
                gridcolor='#263545'
            ),
            yaxis=dict(gridcolor='#263545'),
            showlegend=False,
            margin=dict(t=40, b=20)
        )
        st.plotly_chart(fig_avg_amt, use_container_width=True)
        st.markdown("""
            <p style="color:#78909C; font-size:13px; text-align:center;">
                Mediana: <strong style="color:#2196F3">~$56</strong> (activo)
                vs <strong style="color:#E53935">~$55</strong> (cancelado)
            </p>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background:#1B2A3B; border-radius:12px; padding:20px 24px;
                    border:1px solid #263545; margin-top:8px;">
            <p style="color:#90A4AE; font-size:14px; line-height:1.7; margin:0;">
                El cliente que cancela <strong style="color:#FFFFFF">reduce progresivamente
                el número de veces que usa la tarjeta</strong> a lo largo del año
                (ratio Q4/Q1: 0.531 vs 0.721), pero no el importe que gasta
                en cada uso — las medianas de ticket medio son prácticamente idénticas
                (~$55 vs ~$56). <strong style="color:#FFFFFF">La frecuencia cae
                antes que el gasto por transacción</strong>: es la primera señal
                detectable del proceso de abandono.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ── 4.3 Segmento de actividad ────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

churn_segmento = (
    df.groupby('Activity_Segment')['Attrition_Flag']
    .mean()
    .mul(100)
    .reset_index()
    .rename(columns={'Attrition_Flag': 'Tasa de churn (%)'})
)

col_izq, col_der = st.columns([1.5, 1])

with col_izq:
    fig_segmento = px.bar(
        churn_segmento,
        x='Activity_Segment',
        y='Tasa de churn (%)',
        color='Tasa de churn (%)',
        color_continuous_scale=[[0, '#1B2A3B'], [0.5, '#2196F3'], [1, '#E53935']],
        text='Tasa de churn (%)',
        labels={'Activity_Segment': 'Segmento de actividad'},
        category_orders={'Activity_Segment': ['Low', 'Medium', 'High']}
    )
    fig_segmento.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    fig_segmento.add_hline(
        y=CHURN_RATE_BASE,
        line_dash='dash',
        line_color='#78909C',
        annotation_text=f'Tasa base {CHURN_RATE_BASE}%',
        annotation_position='top right'
    )
    fig_segmento.update_layout(
        title=dict(
            text='Tasa de churn por segmento de actividad transaccional',
            font=dict(color='#ECEFF1', size=16)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#B0BEC5',
        coloraxis_showscale=False,
        xaxis=dict(title='Segmento de actividad', gridcolor='#263545'),
        yaxis=dict(title='Tasa de churn (%)', gridcolor='#263545', range=[0, 40]),
        margin=dict(t=40, b=20)
    )
    st.plotly_chart(fig_segmento, use_container_width=True)

with col_der:
    st.markdown("""
        <div style="background:#1B2A3B; border-radius:12px; padding:24px;
                    border:1px solid #263545; margin-top:48px;">
            <p style="color:#2196F3; font-size:11px; font-weight:700;
                      letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">
                Segmento High: blindado
            </p>
            <p style="color:#ECEFF1; font-size:15px; line-height:1.7; margin-bottom:16px;">
                Los clientes de actividad alta tienen una tasa de churn del
                <strong style="color:#2196F3">0.1%</strong> —
                prácticamente ninguno cancela.
            </p>
            <p style="color:#90A4AE; font-size:14px; line-height:1.7;">
                El segmento <strong style="color:#FFFFFF">Medium</strong> supera
                al <strong style="color:#FFFFFF">Low</strong> en churn (31.7% vs 16.1%)
                porque combina actividad transaccional intermedia con
                baja vinculación de productos — sin el colchón de retención
                que protege a cada uno de los otros dos grupos por razones distintas.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ── SECCIÓN 5: Curiosidades univariantes ────────────────────────────────────
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

st.markdown("""
    <p class="hero-label">Sección 05</p>
    <h2 style="color:#FFFFFF; font-size:28px; font-weight:700; margin-bottom:8px;">
        El dataset bajo la lupa
    </h2>
    <p class="intro-text" style="margin-bottom:32px;">
        Más allá de la pregunta principal, el dataset esconde algunos patrones
        estructurales que merecen atención. No responden directamente a la pregunta
        del churn, pero revelan cómo se distribuye realmente la cartera de clientes
        del banco.
    </p>
""", unsafe_allow_html=True)

# ── 5.1 Distribución trimodal de Total_Trans_Amt ────────────────────────────
fig_trimodal = px.histogram(
    df,
    x='Total_Trans_Amt',
    nbins=80,
    color_discrete_sequence=['#2196F3'],
    labels={'Total_Trans_Amt': 'Importe total de transacciones ($)'}
)
fig_trimodal.update_layout(
    title=dict(
        text='Distribución del importe total de transacciones',
        font=dict(color='#ECEFF1', size=16)
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#B0BEC5',
    xaxis=dict(title='Importe total ($)', gridcolor='#263545'),
    yaxis=dict(title='Número de clientes', gridcolor='#263545'),
    margin=dict(t=40, b=20)
)
# Líneas verticales separando los tres grupos
for x_val, label in [(5500, 'Corte Low/Medium'), (10500, 'Corte Medium/High')]:
    fig_trimodal.add_vline(
        x=x_val,
        line_dash='dash',
        line_color='#78909C',
        annotation_text=label,
        annotation_position='top',
        annotation_font_color='#78909C'
    )
st.plotly_chart(fig_trimodal, use_container_width=True)

st.markdown("""
    <p style="color:#78909C; font-size:13px; font-style:italic; text-align:center; margin-top:-16px;">
        La distribución no es continua — hay tres grupos separados por huecos reales
        en los datos (~$5,500 y ~$10,500), lo que sugiere segmentos de comportamiento
        estructuralmente distintos, no una gradación continua de uso.
    </p>
""", unsafe_allow_html=True)

# ── 5.2 Pico en Total_Revolving_Bal = 0 y Gender vs Credit_Limit ────────────
st.markdown("<br>", unsafe_allow_html=True)

col_izq, col_der = st.columns(2)

with col_izq:
    fig_revolving_dist = px.histogram(
        df,
        x='Total_Revolving_Bal',
        nbins=60,
        color_discrete_sequence=['#2196F3'],
        labels={'Total_Revolving_Bal': 'Saldo revolving ($)'}
    )
    fig_revolving_dist.update_layout(
        title=dict(
            text='Distribución del saldo revolving',
            font=dict(color='#ECEFF1', size=15)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#B0BEC5',
        xaxis=dict(title='Saldo revolving ($)', gridcolor='#263545'),
        yaxis=dict(title='Número de clientes', gridcolor='#263545'),
        margin=dict(t=40, b=20)
    )
    fig_revolving_dist.add_annotation(
        x=0,
        y=2470,
        text='2,470 clientes<br>sin deuda revolving',
        showarrow=True,
        arrowhead=2,
        arrowcolor='#78909C',
        font=dict(color='#90A4AE', size=12),
        ax=80,
        ay=-40
    )
    st.plotly_chart(fig_revolving_dist, use_container_width=True)
    st.markdown("""
        <p style="color:#78909C; font-size:13px; font-style:italic; text-align:center; margin-top:-16px;">
            El 24.4% de los clientes tiene saldo revolving exactamente 0 —
            pagan su tarjeta en su totalidad cada mes.
        </p>
    """, unsafe_allow_html=True)

with col_der:
    # Gender vs Credit_Limit — boxplot
    df_gender = df.copy()
    df_gender['Género'] = df_gender['Gender'].map({0: 'Hombre', 1: 'Mujer'})

    fig_gender_credit = px.box(
        df_gender,
        x='Género',
        y='Credit_Limit',
        color='Género',
        color_discrete_map={'Hombre': '#2196F3', 'Mujer': '#E53935'},
        labels={'Credit_Limit': 'Límite de crédito ($)'}
    )
    fig_gender_credit.update_layout(
        title=dict(
            text='Límite de crédito por género',
            font=dict(color='#ECEFF1', size=15)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#B0BEC5',
        xaxis=dict(gridcolor='#263545'),
        yaxis=dict(title='Límite de crédito ($)', gridcolor='#263545'),
        showlegend=False,
        margin=dict(t=40, b=20)
    )
    st.plotly_chart(fig_gender_credit, use_container_width=True)
    st.markdown("""
        <p style="color:#78909C; font-size:13px; font-style:italic; text-align:center; margin-top:-16px;">
            La mediana del límite de crédito de los hombres ($8,902) casi triplica
            la de las mujeres ($3,048) — aunque esta diferencia no tiene
            implicación directa en la tasa de churn de ninguno de los dos grupos.
        </p>
    """, unsafe_allow_html=True)