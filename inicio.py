import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def main():
    # Page configuration
    st.set_page_config(
        page_title="Análisis de Ventas Northwind", 
        page_icon="📊", 
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-title {
        color: #2C3E50;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    .project-intro {
        background-color: #F0F2F6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Title
    st.markdown('<h1 class="main-title">📊 Análisis de Ventas Northwind</h1>', unsafe_allow_html=True)
    
    # Project Introduction
    st.markdown('<div class="project-intro">', unsafe_allow_html=True)
    st.markdown("""
    ## Introducción al Proyecto

    ### Objetivo
    Realizar un análisis detallado de las tendencias de ventas de la empresa Northwind utilizando técnicas avanzadas de visualización y análisis de datos.

    ### Contexto
    Este proyecto fue desarrollado como parte del curso de **Taller de Programación** bajo la supervisión del profesor Nayib Vargas, con el propósito de aplicar conocimientos de análisis de datos y programación.

    ### Metodología
    - **Herramientas utilizadas:** Python, Streamlit, Plotly
    - **Base de datos:** Northwind
    - **Técnicas de análisis:** Visualización de ventas, análisis por categorías y países
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Database connection
    @st.cache_resource
    def get_database_connection():
        return sqlite3.connect("data/Northwind_small.sqlite")

    # Load sales data
    def load_sales_data(conn):
        query = """
        SELECT 
            c.Country, 
            ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalSales,
            ROUND(AVG(od.UnitPrice), 2) AS AveragePrice,
            COUNT(DISTINCT o.Id) AS TotalOrders
        FROM [Order] o
        JOIN Customer c ON o.CustomerId = c.Id
        JOIN OrderDetail od ON o.Id = od.OrderId
        GROUP BY c.Country
        ORDER BY TotalSales DESC
        """
        return pd.read_sql_query(query, conn)

    # Load product category data
    def load_category_data(conn):
        query = """
        SELECT 
            cat.CategoryName, 
            ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS CategorySales,
            COUNT(DISTINCT p.Id) AS ProductCount
        FROM OrderDetail od
        JOIN Product p ON od.ProductId = p.Id
        JOIN Category cat ON p.CategoryId = cat.Id
        GROUP BY cat.CategoryName
        ORDER BY CategorySales DESC
        """
        return pd.read_sql_query(query, conn)

    # Establish database connection
    conn = get_database_connection()

    # Load data
    sales_data = load_sales_data(conn)
    category_data = load_category_data(conn)

    # Create columns for visualizations
    col1, col2 = st.columns(2)

    # Sales by Country
    with col1:
        st.subheader("Ventas por País")
        fig_sales = px.bar(
            sales_data, 
            x='Country', 
            y='TotalSales', 
            title='Distribución de Ventas Totales por País',
            labels={'TotalSales': 'Ventas Totales', 'Country': 'País'},
            color='TotalSales',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_sales, use_container_width=True)

    # Sales by Category
    with col2:
        st.subheader("Ventas por Categoría")
        fig_category = px.pie(
            category_data, 
            values='CategorySales', 
            names='CategoryName',
            title='Distribución de Ventas por Categoría de Producto',
            hole=0.3
        )
        st.plotly_chart(fig_category, use_container_width=True)

    # Detailed Metrics
    st.subheader("Resumen de Métricas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Países", len(sales_data))
    
    with col2:
        st.metric("Total de Categorías", len(category_data))
    
    with col3:
        st.metric("Ventas Totales", f"${sales_data['TotalSales'].sum():,.2f}")

    # Detailed Data Tables
    st.subheader("Detalle de Ventas por País")
    st.dataframe(sales_data, use_container_width=True)

    # Footer and Acknowledgments
    st.markdown("---")
    st.markdown("""
    ### Agradecimientos
    Un especial agradecimiento al profesor Nayib Vargas por su guía y apoyo durante el desarrollo de este proyecto.

    **Desarrollado por: Dunia Picado Navarro**
    *Taller de Programación - 2024*
    """)

if __name__ == "__main__":
    main()