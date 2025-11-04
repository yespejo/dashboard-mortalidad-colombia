from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import plotly.utils
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Load real data from CSV files
def load_mortality_data():
    try:
        # Load all CSV files
        data_path = 'data/'
        
        # Load deaths data
        deaths_df = pd.read_csv(os.path.join(data_path, 'ListMuertes.csv'))
        
        # Load geographical data
        divipola_df = pd.read_csv(os.path.join(data_path, 'DiviPola.csv'))
        
        # Load death codes
        death_codes_df = pd.read_csv(os.path.join(data_path, 'CodMuerte.csv'))
        
        # Load age groups
        age_groups_df = pd.read_csv(os.path.join(data_path, 'Grupos.csv'))
        
        # Merge deaths with geographical data
        deaths_geo = deaths_df.merge(
            divipola_df[['COD_DANE', 'DEPARTAMENTO', 'MUNICIPIO']], 
            on='COD_DANE', 
            how='left'
        )
        
        # Merge with death codes
        deaths_complete = deaths_geo.merge(
            death_codes_df[['CODIGO_CIE_10_3', 'CODIGO_MORTALIDAD']],
            left_on='COD_MUERTE',
            right_on='CODIGO_CIE_10_3',
            how='left'
        )
        
        # Function to assign age category based on GRUPO_EDAD1 and age ranges
        def assign_age_category(grupo_edad, age_groups_df):
            for _, row in age_groups_df.iterrows():
                if pd.notna(grupo_edad) and row['GRUPO_MINIMO'] <= grupo_edad <= row['GRUPO_MAXIMO']:
                    return row['CATEGORIA']
            return 'Sin categoría'
        
        # Apply age categorization
        deaths_complete['CATEGORIA_EDAD'] = deaths_complete['GRUPO_EDAD1'].apply(
            lambda x: assign_age_category(x, age_groups_df)
        )
        
        return {
            'deaths': deaths_complete,
            'divipola': divipola_df,
            'death_codes': death_codes_df,
            'age_groups': age_groups_df
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Get processed data
def get_mortality_data():
    data = load_mortality_data()
    if data is None:
        return None
    
    deaths_df = data['deaths']
    
    # Month names in Spanish
    month_names = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    return {
        'deaths_df': deaths_df,
        'month_names': month_names,
        'departments': deaths_df['DEPARTAMENTO'].dropna().unique().tolist(),
        'municipalities': deaths_df['MUNICIPIO'].dropna().unique().tolist()
    }

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard de Mortalidad</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background-color: #f5f5f5;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .nav-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .nav-card {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
                text-decoration: none;
                color: inherit;
            }
            .nav-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.2);
            }
            .nav-card h3 {
                color: #333;
                margin-top: 0;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            .nav-card p {
                color: #666;
                line-height: 1.6;
            }
            .icon {
                font-size: 2em;
                margin-bottom: 10px;
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Dashboard de Mortalidad</h1>
                <p>Análisis integral de datos de mortalidad en Colombia - Herramienta de visualización demográfica y regional</p>
            </div>
            
            <div class="nav-grid">
                <a href="/mapa" class="nav-card">
                    <span class="icon">🗺️</span>
                    <h3>Mapa de Mortalidad</h3>
                    <p>Distribución total de muertes por departamento en Colombia para 2019</p>
                </a>
                
                <a href="/lineas" class="nav-card">
                    <span class="icon">📈</span>
                    <h3>Tendencia Mensual</h3>
                    <p>Gráfico de líneas del total de muertes por mes mostrando variaciones anuales</p>
                </a>
                
                <a href="/violencia" class="nav-card">
                    <span class="icon">🚨</span>
                    <h3>Ciudades Más Violentas</h3>
                    <p>Top 5 ciudades con mayor número de homicidios (códigos X95 y agresiones)</p>
                </a>
                
                <a href="/seguras" class="nav-card">
                    <span class="icon">🕊️</span>
                    <h3>Ciudades Más Seguras</h3>
                    <p>Gráfico circular de las 10 ciudades con menor índice de mortalidad</p>
                </a>
                
                <a href="/causas" class="nav-card">
                    <span class="icon">📋</span>
                    <h3>Principales Causas</h3>
                    <p>Tabla de las 10 principales causas de muerte con códigos y totales</p>
                </a>
                
                <a href="/genero" class="nav-card">
                    <span class="icon">⚖️</span>
                    <h3>Análisis por Género</h3>
                    <p>Gráfico de barras apiladas comparando muertes por sexo en cada departamento</p>
                </a>
                
                <a href="/edades" class="nav-card">
                    <span class="icon">👥</span>
                    <h3>Distribución por Edades</h3>
                    <p>Histograma de mortalidad por grupos de edad según ciclo de vida</p>
                </a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/mapa')
def mapa_mortalidad():
    data = get_mortality_data()
    if data is None:
        return "Error: No se pudieron cargar los datos"
    
    deaths_df = data['deaths_df']
    
    # Count deaths by department (handle missing values)
    dept_deaths = deaths_df[deaths_df['DEPARTAMENTO'].notna()].groupby('DEPARTAMENTO').size().reset_index(name='Total_Muertes')
    dept_deaths = dept_deaths.sort_values('Total_Muertes', ascending=False)
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=dept_deaths['DEPARTAMENTO'],
            y=dept_deaths['Total_Muertes'],
            marker_color='darkred',
            text=dept_deaths['Total_Muertes'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Distribución Real de Muertes por Departamento - Colombia 2019',
        xaxis_title='Departamentos',
        yaxis_title='Número de Muertes',
        template='plotly_white',
        height=600,
        xaxis={'tickangle': 45}
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Get total deaths for summary
    total_deaths = len(deaths_df)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mapa de Mortalidad - Colombia 2019</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .back-btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }}
            .stats {{ background: #e8f4fd; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Volver al Dashboard</a>
            <div class="stats">
                <strong>📊 Resumen:</strong> Total de defunciones registradas: {total_deaths:,} casos
            </div>
            <div id="chart"></div>
            <p><strong>Nota:</strong> Este gráfico muestra la distribución real de muertes por departamento en Colombia para el año 2019 basado en los datos oficiales. Los departamentos se ordenan de mayor a menor número de casos.</p>
        </div>
        <script>
            var graphs = {graphJSON};
            Plotly.plot('chart', graphs, {{}});
        </script>
    </body>
    </html>
    '''

@app.route('/lineas')
def tendencia_mensual():
    data = get_mortality_data()
    if data is None:
        return "Error: No se pudieron cargar los datos"
    
    deaths_df = data['deaths_df']
    month_names = data['month_names']
    
    # Count deaths by month (handle missing values)
    monthly_deaths = deaths_df[deaths_df['MES'].notna()].groupby('MES').size().reset_index(name='Total_Muertes')
    monthly_deaths = monthly_deaths.sort_values('MES')
    
    # Map month numbers to names
    monthly_deaths['Mes_Nombre'] = monthly_deaths['MES'].map(month_names)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_deaths['Mes_Nombre'],
        y=monthly_deaths['Total_Muertes'],
        mode='lines+markers',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8),
        name='Muertes Mensuales'
    ))
    
    fig.update_layout(
        title='Tendencia Mensual Real de Mortalidad - Colombia 2019',
        xaxis_title='Mes',
        yaxis_title='Número de Muertes',
        template='plotly_white',
        height=500
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Calculate statistics
    max_month = monthly_deaths.loc[monthly_deaths['Total_Muertes'].idxmax()]
    min_month = monthly_deaths.loc[monthly_deaths['Total_Muertes'].idxmin()]
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tendencia Mensual - Colombia 2019</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .back-btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }}
            .stats {{ background: #e8f4fd; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Volver al Dashboard</a>
            <div class="stats">
                <strong>📊 Estadísticas:</strong><br>
                Mes con mayor mortalidad: {max_month['Mes_Nombre']} ({max_month['Total_Muertes']:,} casos)<br>
                Mes con menor mortalidad: {min_month['Mes_Nombre']} ({min_month['Total_Muertes']:,} casos)
            </div>
            <div id="chart"></div>
            <p><strong>Análisis:</strong> El gráfico muestra las variaciones mensuales reales en la mortalidad durante 2019 basado en los datos oficiales. Los patrones observados pueden estar relacionados con factores climáticos, epidemiológicos o sociales específicos del país.</p>
        </div>
        <script>
            var graphs = {graphJSON};
            Plotly.plot('chart', graphs, {{}});
        </script>
    </body>
    </html>
    '''

@app.route('/violencia')
def ciudades_violentas():
    data = get_mortality_data()
    if data is None:
        return "Error: No se pudieron cargar los datos"
    
    deaths_df = data['deaths_df']
    
    # Filter homicides (MANERA_MUERTE = 'Homicidio')
    homicides = deaths_df[deaths_df['MANERA_MUERTE'] == 'Homicidio']
    
    # Count homicides by municipality (handle missing values)
    city_homicides = homicides[homicides['MUNICIPIO'].notna()].groupby('MUNICIPIO').size().reset_index(name='Total_Homicidios')
    city_homicides = city_homicides.sort_values('Total_Homicidios', ascending=False).head(10)
    
    fig = go.Figure(data=[
        go.Bar(
            x=city_homicides['MUNICIPIO'],
            y=city_homicides['Total_Homicidios'],
            marker_color=['#c0392b', '#e74c3c', '#ec7063', '#f1948a', '#f5b7b1', '#fadbd8', '#f2d7d5', '#eaeded', '#d5dbdb', '#aeb6bf'],
            text=city_homicides['Total_Homicidios'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Top 10 Municipios con Mayor Número de Homicidios - Colombia 2019<br><sub>Datos reales basados en registros oficiales</sub>',
        xaxis_title='Municipio',
        yaxis_title='Número de Homicidios',
        template='plotly_white',
        height=500,
        xaxis={'tickangle': 45}
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Get statistics
    total_homicides = len(homicides)
    top_city = city_homicides.iloc[0]
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Municipios Más Violentos - Colombia 2019</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .back-btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }}
            .alert {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin-top: 20px; }}
            .stats {{ background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Volver al Dashboard</a>
            <div class="stats">
                <strong>📊 Estadísticas de Violencia:</strong><br>
                Total de homicidios registrados: {total_homicides:,} casos<br>
                Municipio con mayor violencia: {top_city['MUNICIPIO']} ({top_city['Total_Homicidios']:,} homicidios)
            </div>
            <div id="chart"></div>
            <div class="alert">
                <strong>⚠️ Datos de Violencia:</strong> Este análisis muestra los municipios con mayor número de homicidios registrados en 2019 según los datos oficiales. Los casos están clasificados como "Homicidio" en el campo MANERA_MUERTE.
            </div>
        </div>
        <script>
            var graphs = {graphJSON};
            Plotly.plot('chart', graphs, {{}});
        </script>
    </body>
    </html>
    '''

@app.route('/seguras')
def ciudades_seguras():
    data = get_mortality_data()
    if data is None:
        return "Error: No se pudieron cargar los datos"
    
    deaths_df = data['deaths_df']
    
    # Count deaths by municipality and get the ones with lowest counts (handle missing values)
    city_deaths = deaths_df[deaths_df['MUNICIPIO'].notna()].groupby('MUNICIPIO').size().reset_index(name='Total_Muertes')
    city_deaths = city_deaths.sort_values('Total_Muertes', ascending=True).head(10)
    
    fig = go.Figure(data=[go.Pie(
        labels=city_deaths['MUNICIPIO'],
        values=city_deaths['Total_Muertes'],
        hole=0.4,
        marker_colors=px.colors.qualitative.Set3
    )])
    
    fig.update_layout(
        title='Top 10 Municipios con Menor Número de Defunciones - Colombia 2019<br><sub>Datos reales basados en registros oficiales</sub>',
        template='plotly_white',
        height=600
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Get statistics
    safest_city = city_deaths.iloc[0]
    total_cities = len(city_deaths)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Municipios Más Seguros - Colombia 2019</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .back-btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }}
            .info {{ background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin-top: 20px; }}
            .stats {{ background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Volver al Dashboard</a>
            <div class="stats">
                <strong>📊 Estadísticas de Seguridad:</strong><br>
                Municipio con menor mortalidad: {safest_city['MUNICIPIO']} ({safest_city['Total_Muertes']:,} casos)<br>
                Total de municipios analizados: {total_cities}
            </div>
            <div id="chart"></div>
            <div class="info">
                <strong>✅ Municipios Seguros:</strong> Este gráfico circular muestra los 10 municipios con menor número de defunciones registradas en 2019 según los datos oficiales. Estos municipios presentan condiciones favorables de seguridad y salud pública.
            </div>
        </div>
        <script>
            var graphs = {graphJSON};
            Plotly.plot('chart', graphs, {{}});
        </script>
    </body>
    </html>
    '''

@app.route('/causas')
def principales_causas():
    data = get_mortality_data()
    if data is None:
        return "Error: No se pudieron cargar los datos"
    
    deaths_df = data['deaths_df']
    
    # Count deaths by cause (COD_MUERTE) and description
    cause_counts = deaths_df.groupby(['COD_MUERTE', 'CODIGO_MORTALIDAD']).size().reset_index(name='Total_Casos')
    cause_counts = cause_counts.sort_values('Total_Casos', ascending=False).head(15)
    
    # Clean up the data for display
    cause_counts['Descripción'] = cause_counts['CODIGO_MORTALIDAD'].fillna('Sin descripción')
    
    # Create DataFrame for the table
    df = cause_counts[['COD_MUERTE', 'Descripción', 'Total_Casos']].copy()
    df.columns = ['Código CIE-10', 'Descripción de la Causa', 'Total de Casos']
    
    # Convert DataFrame to HTML with styling
    table_html = df.to_html(
        classes='table table-striped',
        table_id='causas-table',
        index=False,
        escape=False
    )
    
    # Get statistics
    total_causes = len(cause_counts)
    top_cause = cause_counts.iloc[0]
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Principales Causas de Muerte - Colombia 2019</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .back-btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }}
            .stats {{ background: #e8f4fd; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            table {{ 
                border-collapse: collapse; 
                width: 100%; 
                margin-top: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            th {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: bold;
            }}
            td {{ 
                border: 1px solid #ddd; 
                padding: 12px; 
                text-align: left;
            }}
            tr:nth-child(even) {{ background-color: #f8f9fa; }}
            tr:hover {{ background-color: #e3f2fd; }}
            .rank {{ font-weight: bold; color: #667eea; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Volver al Dashboard</a>
            <div class="stats">
                <strong>📊 Estadísticas de Causas:</strong><br>
                Principal causa de muerte: {top_cause['COD_MUERTE']} - {top_cause['Descripción']} ({top_cause['Total_Casos']:,} casos)<br>
                Total de causas diferentes analizadas: {total_causes}
            </div>
            <h1>📋 Top 15 Principales Causas de Muerte en Colombia - 2019</h1>
            <p>Listado real ordenado de mayor a menor según el total de casos registrados, incluyendo códigos CIE-10 oficiales.</p>
            {table_html}
            <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                <strong>📊 Análisis:</strong> Esta tabla muestra las principales causas de muerte registradas en Colombia durante 2019 según los datos oficiales. Los códigos CIE-10 permiten una clasificación internacional estandarizada de las causas de mortalidad.
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/genero')
def analisis_genero():
    data = get_mortality_data()
    if data is None:
        return "Error: No se pudieron cargar los datos"
    
    deaths_df = data['deaths_df']
    
    # Count deaths by department and gender (handle missing values)
    gender_dept = deaths_df[(deaths_df['DEPARTAMENTO'].notna()) & (deaths_df['SEXO'].notna())].groupby(['DEPARTAMENTO', 'SEXO']).size().reset_index(name='Total_Muertes')
    
    # Get top 15 departments by total deaths
    top_depts = deaths_df[deaths_df['DEPARTAMENTO'].notna()].groupby('DEPARTAMENTO').size().reset_index(name='Total').sort_values('Total', ascending=False).head(15)['DEPARTAMENTO'].tolist()
    
    # Filter data for top departments
    gender_dept_filtered = gender_dept[gender_dept['DEPARTAMENTO'].isin(top_depts)]
    
    # Separate male and female data
    male_data = gender_dept_filtered[gender_dept_filtered['SEXO'] == 1]
    female_data = gender_dept_filtered[gender_dept_filtered['SEXO'] == 2]
    
    # Merge to ensure all departments have both genders (fill with 0 if missing)
    dept_df = pd.DataFrame({'DEPARTAMENTO': top_depts})
    male_merged = dept_df.merge(male_data[['DEPARTAMENTO', 'Total_Muertes']], on='DEPARTAMENTO', how='left').fillna(0)
    female_merged = dept_df.merge(female_data[['DEPARTAMENTO', 'Total_Muertes']], on='DEPARTAMENTO', how='left').fillna(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Hombres',
        x=male_merged['DEPARTAMENTO'],
        y=male_merged['Total_Muertes'],
        marker_color='#3498db'
    ))
    
    fig.add_trace(go.Bar(
        name='Mujeres',
        x=female_merged['DEPARTAMENTO'],
        y=female_merged['Total_Muertes'],
        marker_color='#e91e63'
    ))
    
    fig.update_layout(
        title='Comparación Real de Mortalidad por Género y Departamento - Colombia 2019',
        xaxis_title='Departamento',
        yaxis_title='Número de Muertes',
        barmode='stack',
        template='plotly_white',
        height=600,
        xaxis={'tickangle': 45}
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Calculate statistics
    total_male = deaths_df[deaths_df['SEXO'] == 1].shape[0]
    total_female = deaths_df[deaths_df['SEXO'] == 2].shape[0]
    male_percentage = (total_male / (total_male + total_female)) * 100
    female_percentage = (total_female / (total_male + total_female)) * 100
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Análisis por Género - Colombia 2019</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .back-btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }}
            .analysis {{ background: #e8f4fd; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin-top: 20px; }}
            .stats {{ background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Volver al Dashboard</a>
            <div class="stats">
                <strong>📊 Estadísticas por Género:</strong><br>
                Muertes masculinas: {total_male:,} casos ({male_percentage:.1f}%)<br>
                Muertes femeninas: {total_female:,} casos ({female_percentage:.1f}%)<br>
                Ratio Hombre/Mujer: {total_male/total_female:.2f}
            </div>
            <div id="chart"></div>
            <div class="analysis">
                <strong>⚖️ Análisis de Género:</strong> El gráfico de barras apiladas muestra las diferencias reales en mortalidad entre hombres y mujeres por departamento basado en los datos oficiales de 2019. Los patrones observados reflejan diferencias demográficas, sociales y de exposición a riesgos entre géneros.
            </div>
        </div>
        <script>
            var graphs = {graphJSON};
            Plotly.plot('chart', graphs, {{}});
        </script>
    </body>
    </html>
    '''

@app.route('/edades')
def distribucion_edades():
    data = get_mortality_data()
    if data is None:
        return "Error: No se pudieron cargar los datos"
    
    deaths_df = data['deaths_df']
    
    # Get the age groups data
    data_obj = load_mortality_data()
    age_groups_df = data_obj['age_groups'] if data_obj else pd.DataFrame()
    
    if age_groups_df.empty:
        return "Error: No se pudieron cargar los grupos de edad"
    
    # Count deaths by manually checking GRUPO_EDAD1 against ranges
    age_counts = []
    
    for _, age_group in age_groups_df.iterrows():
        categoria = age_group['CATEGORIA']
        grupo_min = age_group['GRUPO_MINIMO']
        grupo_max = age_group['GRUPO_MAXIMO']
        rango_edad = age_group['RANGO_EDAD']
        
        # Count records where GRUPO_EDAD1 is between GRUPO_MINIMO and GRUPO_MAXIMO
        count = len(deaths_df[
            (deaths_df['GRUPO_EDAD1'].notna()) & 
            (deaths_df['GRUPO_EDAD1'] >= grupo_min) & 
            (deaths_df['GRUPO_EDAD1'] <= grupo_max)
        ])
        
        age_counts.append({
            'CATEGORIA_EDAD': categoria,
            'Total_Muertes': count,
            'RANGO_EDAD': rango_edad,
            'GRUPO_MINIMO': grupo_min,
            'GRUPO_MAXIMO': grupo_max
        })
    
    # Convert to DataFrame and sort by the original order in age_groups_df
    age_counts_df = pd.DataFrame(age_counts)
    
    # Create labels with range information
    age_counts_df['Label'] = age_counts_df['CATEGORIA_EDAD'] + ' (' + age_counts_df['RANGO_EDAD'] + ')'
    
    fig = go.Figure(data=[
        go.Bar(
            x=age_counts_df['Label'],
            y=age_counts_df['Total_Muertes'],
            marker_color='#9b59b6',
            text=age_counts_df['Total_Muertes'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Distribución Real de Mortalidad por Grupos de Edad - Colombia 2019<br><sub>Conteo directo de registros por rangos GRUPO_EDAD1</sub>',
        xaxis_title='Grupo de Edad',
        yaxis_title='Número de Muertes',
        template='plotly_white',
        height=500,
        xaxis={'tickangle': 45}
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Calculate statistics
    total_by_age = age_counts_df['Total_Muertes'].sum()
    max_age_group = age_counts_df.loc[age_counts_df['Total_Muertes'].idxmax()]
    min_age_group = age_counts_df.loc[age_counts_df['Total_Muertes'].idxmin()]
    
    # Additional verification info
    total_records = len(deaths_df)
    records_with_age = len(deaths_df[deaths_df['GRUPO_EDAD1'].notna()])
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Distribución por Edades - Colombia 2019</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .back-btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }}
            .insights {{ background: #f3e5f5; border: 1px solid #ce93d8; padding: 15px; border-radius: 5px; margin-top: 20px; }}
            .stats {{ background: #e8f4fd; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .verification {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Volver al Dashboard</a>
            <div class="stats">
                <strong>📊 Estadísticas por Edad:</strong><br>
                Total de muertes analizadas: {total_by_age:,} casos<br>
                Grupo con mayor mortalidad: {max_age_group['CATEGORIA_EDAD']} ({max_age_group['Total_Muertes']:,} casos)<br>
                Grupo con menor mortalidad: {min_age_group['CATEGORIA_EDAD']} ({min_age_group['Total_Muertes']:,} casos)
            </div>
            <div id="chart"></div>
            <div class="verification">
                <strong>🔍 Verificación de Conteo:</strong><br>
                Total de registros en ListMuertes.csv: {total_records:,}<br>
                Registros con GRUPO_EDAD1 válido: {records_with_age:,}<br>
                Registros contabilizados en gráfico: {total_by_age:,}<br>
                Método: Conteo directo donde GRUPO_EDAD1 está entre GRUPO_MINIMO y GRUPO_MAXIMO
            </div>
            <div class="insights">
                <strong>👥 Patrones Demográficos Reales:</strong> El histograma muestra la distribución real de muertes por grupos de edad según los datos oficiales de 2019. Los patrones observados reflejan la estructura demográfica del país y los factores de riesgo asociados a cada etapa del ciclo de vida.
            </div>
        </div>
        <script>
            var graphs = {graphJSON};
            Plotly.plot('chart', graphs, {{}});
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
