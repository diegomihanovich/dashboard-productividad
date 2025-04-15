import pandas as pd
import streamlit as st
import plotly.express as px

# Cargar datos
df = pd.read_excel("Produccion_Alfombra_FXL.xlsx", sheet_name="Hoja 1")
df.columns = df.columns.str.strip()
df["Fecha"] = pd.to_datetime(df["Fecha"], errors='coerce')
df["m lineales"] = pd.to_numeric(df["m lineales"], errors='coerce')

# Campos útiles
df["Mes/Año"] = df["Fecha"].dt.to_period("M").astype(str)

# Título
st.title("📊 Dashboard de Productividad de Alfombras")

# Filtros
col1, col2, col3 = st.columns(3)
mes_seleccionado = col1.selectbox("📅 Elegí un mes:", sorted(df["Mes/Año"].dropna().unique()))
articulo = col2.selectbox("🧶 Artículo:", ["Todos"] + sorted(df["Articulo"].dropna().unique()))
vendedor = col3.selectbox("👷 Operario/Vendedor:", ["Todos"] + sorted(df["Vendedor"].dropna().unique()))

# Filtrado
df_filtrado = df[df["Mes/Año"] == mes_seleccionado]
if articulo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Articulo"] == articulo]
if vendedor != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Vendedor"] == vendedor]

# KPIs
st.subheader("🔢 Métricas clave")
col4, col5, col6 = st.columns(3)
col4.metric("Total metros tejidos", f"{df_filtrado['m lineales'].sum():,.0f} m")
col5.metric("Promedio diario", f"{df_filtrado.groupby('Fecha')['m lineales'].sum().mean():,.1f} m/día")
col6.metric("Cantidad de rollos", f"{df_filtrado['nº de rollo'].nunique()}")

# Gráfico de evolución diaria
st.subheader("📈 Evolución diaria")
fig = px.line(df_filtrado.groupby("Fecha")["m lineales"].sum().reset_index(), x="Fecha", y="m lineales",
              title="Metros tejidos por día")
st.plotly_chart(fig, use_container_width=True)

# Gráfico por artículo
st.subheader("📦 Producción por artículo")
fig2 = px.bar(df_filtrado.groupby("Articulo")["m lineales"].sum().reset_index(), 
              x="Articulo", y="m lineales")
st.plotly_chart(fig2, use_container_width=True)

# Gráfico por operario
st.subheader("👷 Producción por operario")
fig3 = px.bar(df_filtrado.groupby("Vendedor")["m lineales"].sum().reset_index(), 
              x="Vendedor", y="m lineales")
st.plotly_chart(fig3, use_container_width=True)
